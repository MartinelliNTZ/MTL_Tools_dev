# Análise: Problemas de Travamento da Thread Principal - VectorFieldPlugin

## Resumo Executivo
A aplicação contém **CRÍTICOS** problemas de travamento de thread, especialmente no caminho **SÍNCRONO**. O caminho assíncrono também tem vulnerabilidades. As operações de cálculo são executadas iterativamente sem batching, causando múltiplas chamadas ao QGIS na thread principal.

---

## 🔴 PROBLEMA CRÍTICO #1: Caminho Síncrono - Loops Iterativos BLOQUEADORES

### Localização
- [vector_field_plugin.py](vector_field_plugin.py#L197-L255) - `_execute_sync_calculation()`
- [VectorLayerAttributes.py](utils/vector/VectorLayerAttributes.py#L203-L225) - `update_point_xy_coordinates()`
- [VectorLayerMetrics.py](utils/vector/VectorLayerMetrics.py#L77-L138) - `calculate_line_length()` e `calculate_polygon_area()`

### O Problema

```python
# ❌ BLOQUEADOR: loop iterativo na thread principal
for feat in layer.getFeatures():
    geom = feat.geometry()
    if geom and not geom.isEmpty():
        p = geom.asPoint()
        feat[field_map["x"]] = round(p.x(), precision)
        feat[field_map["y"]] = round(p.y(), precision)
        layer.updateFeature(feat)  # ⚠️ Atualização individual
```

### Por que é Crítico?

1. **Múltiplas chamadas ao QGIS**: Cada `layer.updateFeature()` é uma chamada **síncrona** ao núcleo QGIS
2. **Sem batching**: 1M features = 1M chamadas individuais bloqueadoras
3. **SEM feedback visual**: Usuário vê UI congelada sem progress bar
4. **Complexidade O(n)**: Camadas com 10k-100k+ features ficam completamente travadas
5. **Cálculos elipsoidais custosos**: `d.measureLength(geom)` e `d.measureArea(geom)` envolvem transformações matemáticas pesadas

### Impacto Observável
- **1k features**: ~1-5 segundos de travamento
- **10k features**: ~10-60 segundos de travamento (UI não responde a cliques)
- **100k+ features**: QGIS pode aparentar "congelado" ou "não responde"

---

## 🔴 PROBLEMA CRÍTICO #2: Lógica de Decisão Sync/Async Deficiente

### Localização
[vector_field_plugin.py](vector_field_plugin.py#L82-L116)

### O Problema

```python
size = ProjectUtils.compute_size(layer)  # Retorna tamanho do arquivo
threshold = self.settings_preferences.get('async_threshold_bytes', 20 * 1024 * 1024)

# ❌ FALHA: compute_size não reflete adequadamente a complexidade
if is_memory or size > threshold:
    self._start_async_calculation(...)  # Assíncrono
else:
    self._execute_sync_calculation(...)  # BLOQUEADOR!
```

### Falhas da Lógica

1. **`compute_size()` é não-confiável para memory layers**:
   ```python
   if src.startswith("memory:"):
       feat_count = obj.featureCount()
       return feat_count * 200  # ⚠️ Estimativa MUITO aproximada
   ```
   - 1M features em memória = ~200 MB estimado
   - Mas se feature count = 0 ou inaccurado, retorna 0
   - Camada é tratada como síncrana **MESMO COM CENTENAS DE MIL FEATURES**

2. **Não leva em conta complexidade do cálculo**:
   - Polígono com 10k vértices = cálculo elipsoidal **MUITO** custoso
   - Arquivo pequeno (2 MB) + geometrias complexas = travamento garantido

3. **Threshold fixo inadequado**:
   - 20 MB é arbitrary
   - Não considera CPU, velocidade de I/O, complexidade geométrica

### Cenários de Travamento

| Cenário | Tamanho | Feature Count | Resultado |
|---------|---------|---------------|-----------|
| Memory layer com 50k pontos | 10 MB | 50k | **SÍNCRONO** ❌ |
| ShapeFile 5MB com polígonos complexos | 5 MB | 100 | **SÍNCRONO** ❌ |
| GeoPackage 500k features (estimado 100MB) | 100+ MB | 500k | **ASSÍNCRONO** ✓ |

---

## 🟠 PROBLEMA GRAVE #3: Modo de Atualização de Campos - Sem Batch

### Localização
[PointFieldsStep.py](core/engine_tasks/PointFieldsStep.py#L90-L130) e análogos

### O Problema

```python
# ❌ Atualização uma-por-uma na thread principal
for fid, vals in updates.items():
    provider.changeAttributeValue(fid, field_idx, value)
```

Mesmo no caminho assíncrono, as atualizações são iterativas, não em batch.

### Impacto

- **Commits parciais no BD**: Cada `changeAttributeValue()` pode fazer round-trip ao BD
- **Sem transação**: Sem `beginEditCommand()/endEditCommand()` em batch

### Solução Necessária

```python
# ✓ Correta: atualização em batch
all_changes = {}
for fid, vals in updates.items():
    all_changes[fid] = {field_idx: value}

# Uma única operação
provider.changeAttributeValues(all_changes)
```

---

## 🟠 PROBLEMA GRAVE #4: Chamadas a `layer.startEditing()` Durante Cálculo

### Localização
- [VectorLayerMetrics.py](utils/vector/VectorLayerMetrics.py#L105-L107)
- [VectorLayerAttributes.py](utils/vector/VectorLayerAttributes.py#L185-L187)

### O Problema

```python
if not layer.isEditable():
    layer.startEditing()  # ⚠️ Transação cria buffer em memória
```

Isso é chamado **DURANTE** o loop de cálculo, não antes. Causas:

1. **Buffer de edição não otimizado** para grandes volumes
2. **Rastreamento de mudanças** por QGIS em tempo real
3. **Signals emitidos** para cada atualização (se não bloqueados)

---

## 🟡 PROBLEMA MODERADO #5: Memory Leaks Potenciais

### Localização
[vector_field_plugin.py](vector_field_plugin.py#L130-L160)

### O Problema

```python
context.set("layer", layer)  # ✓ OK: referência mantida
# MAS: Se assíncrono é cancelado, contexto mantém referência viva
# Se layer é deletada fora, referência em context fica órfã
```

### Não é Travamento, mas:
- Referências circularmente vinculadas entre `engine`, `context`, `layer`
- Sem limpeza explícita em cancelamento
- Em chamadas repetidas, pode acumular objetos na memória

---

## 🟡 PROBLEMA MODERADO #6: Lógica de Modo Alterado - Cascata de Callbacks

### Localização
[vector_field_plugin.py](vector_field_plugin.py#L228-L245)

### O Problema

```python
def _resolve_calculation_mode(self, layer, requested_mode):
    if requested_mode != "Cartesiana" or VectorLayerProjection.is_geographic_crs(layer):
        return requested_mode, False
    
    # ❌ Alerta é mostrado, então modo é alterado
    QgisMessageUtil.bar_warning(self.iface, msg)
    return "Ambos", True
```

### Falta de Sincronização

1. Aviso é **assíncrono** (não modal)
2. Código continua executando
3. Usuário pode clicar em outro lugar enquanto aviso está sendo processado
4. Sem confirmação explícita: usuário pode não perceber que modo foi alterado

---

## 📊 Análise Comparativa: Sync vs Async

| Aspecto | Síncrono ❌ | Assíncrono ✓ |
|--------|-----------|------------|
| Travamento | SIM (até 2-5+ minutos para 500k features) | NÃO (progress bar visível) |
| Feature Count que trava | 10k+ | Nenhum (mantém UI responsiva) |
| Feedback Usuário | Nenhum | Progress bar em tempo real |
| Cancelabilidade | Não | SIM (user pode cancelar) |
| Atualização em Batch | NÃO | Parcialmente (ainda iterativo) |
| Memory Usage | Incrementa gradualmente | Pico inicial + estável |

---

## ⚠️ Conclusão: Hierarquia de Riscos

### 🔴 CRÍTICO (Causa Travamento Garantido)
1. **Loops síncronos sem batching** - Múltiplas operações QGIS iterativas
2. **Lógica de threshold inadequada** - Memory layers com muitos features rodam síncronamente
3. **Falta de cancelabilidade** no caminho síncrono

### 🟠 GRAVE (Trava em Cenários Comuns)
1. **Atualização de campos iterativa** - Mesmo em assíncrono
2. **`startEditing()` durante loop** - Buffer não otimizado
3. **Sem progress feedback** no síncrono

### 🟡 MODERADO (Problemas Estruturais)
1. **Memory leaks potenciais** em contextos
2. **Modo alterado silenciosamente** sem confirmação
3. **Sem transação explícita** em batch updates

---

## 🎯 Recomendações de Otimização (Priorizadas)

### Imediato (Bloqueador)
```
1. Forçar assíncrono SEMPRE
2. Implementar batching real: provider.changeAttributeValues()
3. Threshold baseado em feature_count, não file size
```

### Curto Prazo
```
4. Mover startEditing() FORA do loop
5. Bloquear signals QGIS durante atualização em batch
6. Adicionar feedback visual (progress bar) no síncrono
7. Implementar cancelamento no síncrono
```

### Médio Prazo
```
8. Limpar contexto e referências após finalização
9. Modal confirmation para modo alterado
10. Caching de cálculos (LRU cache para features repetidas)
11. Paralelização de cálculos em worker threads
```

---

## Referências de Código Crítico

- Sync loop bloqueador: [L203-L225 VectorLayerAttributes.py]
- Decisão sync/async: [L82-L116 vector_field_plugin.py]
- Atualização iterativa: [L90-L130 PointFieldsStep.py]

