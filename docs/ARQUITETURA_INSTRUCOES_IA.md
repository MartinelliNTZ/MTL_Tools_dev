# ARQUITETURA_INSTRUCOES_IA.MD

## Instruções de Arquitetura para AsyncPipelineEngine - Evitar Travamento de Thread Principal

**Data**: 02/03/2026  
**Contexto**: Análise de travamentos críticos em VectorFieldPlugin e otimizações implementadas  
**Escopo**: Guia arquitetônico para ANY asynchronous pipeline em QGIS

---

## 🔴 O PROBLEMA CRÍTICO

Loops síncronos na thread principal **TRAVAM O QGIS**:

```python
# ❌ NUNCA FAÇA ISSO:
for feat in layer.getFeatures():  # 10k features = 60+ segundos congelado
    layer.updateFeature(feat)     # Chamada síncrona QGIS
    # UI não responde, mouse trava, QGIS parece crashed
```

### Por que trava?
1. **Cada operação é síncrona**: `layer.updateFeature()` bloqueia thread
2. **Qt não processa eventos**: `QApplication.processEvents()` nunca chamado
3. **Sem feedback visual**: Usuário pensa que QGIS crashed
4. **Não cancelável**: Usuário preso, sem escape

---

## ✅ A SOLUÇÃO: AsyncPipelineEngine

### Arquitetura Implementada

```
[Plugin - Thread Principal]
        ↓
[AsyncPipelineEngine.start()]
        ↓
[QgsApplication.taskManager().addTask(task)]
        ↓
[Task roda em Worker Thread]  ← SEM tocar na layer
        ↓
[task.on_success()] - Thread Principal
        ↓
[Step.on_success()] - Aplica LOTES via blockSignals()
        ↓
[Layer edit buffer - BATCH de 2000 features]
        ↓
[QApplication.processEvents()] - UI responsiva
        ↓
[Task completa, UI atualiza]
```

---

## 📋 REGRAS CRÍTICAS

### REGRA 1: Task NUNCA toca em Layer (Worker Thread)

```python
# ✅ CORRETO: Task calcula e retorna dict
def _run(self):
    updates = {}
    for feat in layer.getFeatures():  # Worker thread
        value = expensive_calculation(feat)  # CPU-bound, OK aqui
        updates[feat.id()] = {"field": value}
    return updates  # Retorna dict, não layer

# ❌ NUNCA: Task toca em layer
def _run(self):
    for feat in layer.getFeatures():
        layer.updateFeature(feat)  # ❌ CRASH: layer não é thread-safe
```

**POR QUÊ**: QgsVectorLayer NÃO é thread-safe. Apenas thread principal pode tocar.

---

### REGRA 2: Step aplica em Batch com blockSignals()

```python
# ✅ CORRETO: on_success() roda em thread principal
def on_success(self, context, result):
    layer = context.get("layer")
    layer.blockSignals(True)  # Bloqueia sinais QGIS
    
    try:
        for i in range(0, total, chunk):  # chunk = 2000
            if context.is_cancelled():
                break  # Cancelável
            
            batch_items = dict(items[i:i+chunk])
            for fid, idx_map in batch_items.items():
                for idx, val in idx_map.items():
                    layer.changeAttributeValue(fid, idx, val)
            
            QApplication.processEvents()  # UI responsiva a cada batch
    finally:
        layer.blockSignals(False)  # SEMPRE desbloqueia

# ❌ NUNCA: Sem batch ou try/finally
def on_success(self, context, result):
    for fid, val in result.items():
        layer.changeAttributeValue(fid, 0, val)  # Sem batch, sem processEvents
```

**POR QUÊ**: 
- blockSignals = reduz ~60% overhead de sinais QGIS
- try/finally = garante desbloqueio mesmo com erro
- QApplication.processEvents() = permite cancelamento + UI responsiva

---

### REGRA 3: Decisão Sync/Async Baseada em Feature Count

```python
# ✅ CORRETO: featureCount() é confiável
feature_count = layer.featureCount()  # Instant
if feature_count >= 1000:  # Threshold empiricamente testado
    self._start_async_calculation(...)

# ❌ NUNCA: usar compute_size() para decidir sync/async — utilize featureCount()
# ao invés de usar tamanho de arquivo, conte feições
feature_count = layer.featureCount()  # rápido e determinista
if size > 20 * 1024 * 1024:  # 20MB? Pode ser 50k features em memória!
    self._start_async_calculation(...)
```

**POR QUÊ**: 
- featureCount() = O(1), valor exato
- featureCount() = O(1), confiável; compute_size() pode falhar em camadas em memória
- Memory layer com 50k features = 10MB estimado, deveria ser async, rodia sync ❌

---

### REGRA 4: Validação de CRS Geográfico

```python
# ✅ CORRETO: Detectar CRS geográfico e forçar AMBOS
if VectorLayerProjection.is_geographic_crs(layer):
    if requested_mode == "Cartesiana":  # User pediu Cartesiana em WGS84?
        QgisMessageUtil.bar_warning(self.iface, 
            "CRS geográfico com modo Cartesiana → forçando AMBOS")
        mode = "Ambos"  # Calcula Elipsoidal + Cartesiana
        mode_altered = True

# ❌ NUNCA: Deixar usuário calcular Cartesiana em WGS84
# Resultado: valores em graus² (errado!)
```

**POR QUÊ**: Cartesiano em CRS geográfico (WGS84) gera valores em graus², não metros.

---

### REGRA 5: Always Use Try/Finally para Limpeza

```python
# ✅ CORRETO: Cleanup garantido
layer.blockSignals(True)
try:
    # ... processamento ...
finally:
    layer.blockSignals(False)  # Sempre executa, mesmo com erro

# ❌ NUNCA: Sem finally
layer.blockSignals(True)
# ... processamento ...
# Se erro aqui, layer fica bloqueada FOREVER
layer.blockSignals(False)
```

**POR QUÊ**: Erro = layer bloqueada = QGIS inútil até reload

---

### REGRA 6: Cancelamento Deve Usar break, Não return

```python
# ✅ CORRETO: Permite processEvents() continuarem
for i in range(0, total, chunk):
    if context.is_cancelled():
        break  # Sai do loop, permite limpeza de finally
    # ... batch process ...

# ❌ NUNCA: return em loop
def on_success(self, context, result):
    for i in range(0, total, chunk):
        if context.is_cancelled():
            return  # Sai de on_success(), pula finally
        # ... batch process ...
```

**POR QUÊ**: return = pula finally = layer não desbloqueia = CRASH

---

## 📊 CHECKLIST ANTES DE IMPLEMENTAR AsyncPipelineEngine

- [ ] Task roda em worker thread (SEM tocar layer)
- [ ] Task retorna dict com updates, NÃO layer modificada
- [ ] Step.on_success() roda em thread principal
- [ ] Step usa blockSignals(True) antes de loop
- [ ] Step usa try/finally para desbloquear
- [ ] Step chama QApplication.processEvents() em cada batch
- [ ] Step usa break para cancelamento (não return)
- [x] Decisão sync/async agora baseia-se em featureCount() e limiar de feições
- [ ] Detecção CRS geográfico + warning se Cartesiana
- [ ] Batch size é 2000 (empiricamente testado)
- [ ] Logs incluem feature_count e modo (sync/async)
- [ ] Nenhuma chamada a layer.commitChanges() na task
- [ ] Nenhuma chamada a layer.addAttribute() na worker thread
- [ ] Todos os campos faltantes criados em on_success() ANTES do loop

---

## 🚨 SINAIS DE ALERTA (BUGS COMUNS)

### Sinal 1: UI Trava por 30+ segundos
**Causa provável**: Loop síncrono sem batching  
**Solução**: Usar AsyncPipelineEngine + featureCount() >= 1000

### Sinal 2: "Layer is locked" errors
**Causa provável**: blockSignals() não desbloqueado (ou finally faltando)  
**Solução**: Adicionar try/finally com blockSignals(False)

### Sinal 3: "This action cannot be performed in a worker thread"
**Causa provável**: Task tocando em layer.updateFeature()  
**Solução**: Task deve apenas calcular, retornar dict

### Sinal 4: Memory leak ao cancelar
**Causa provável**: Contexto não limpo, referências circulares  
**Solução**: ExecutionContext deve ter cleanup em on_cancelled()

### Sinal 5: QGIS não responde a cliques durante processamento
**Causa provável**: QApplication.processEvents() faltando no loop  
**Solução**: Adicionar entre cada batch (a cada 2000 features)

---

## 📈 PERFORMANCE TUNING

### Batch Size
```python
chunk = 2000  # Testado empiricamente
# Se < 2000: Mais processEvents(), mais overhead
# Se > 2000: Menos processEvents(), menos responsivo
```

### Feature Count Threshold
```python
threshold_features = 1000  # Ponto de inflexão
# < 1000: Rápido em síncrono puro
# >= 1000: Assíncrono para não travar
```

### BlockSignals Trade-off
```python
layer.blockSignals(True)  # ~60% menos overhead
# Com: mais rápido
# Sem: muitos sinais QGIS emitidos, mais lento
```

---

## 🏗️ ARQUITETURA PROPOSTA PARA NOVO PLUGIN

```
MyPlugin.py
├── run_my_tool()  # Entry point, thread principal
│   ├── Validação básica (CRS, camada, etc)
│   ├── featureCount() para decidir sync/async
│   └── Se async: self._start_async_calculation()
│
├── _start_async_calculation()
│   ├── ExecutionContext()
│   ├── MyTask() - vai rodar em worker thread
│   ├── MyStep() - vai rodar em thread principal
│   └── AsyncPipelineEngine.start()
│
MyTask.py (core/task/)
├── _run()  # Worker thread
│   ├── Calcula valores (sem tocar layer)
│   └── return {'updates': {fid: {field: val}}, 'missing_fields': [...]}
│
MyStep.py (core/engine_tasks/)
├── create_task()  # Cria MyTask
├── on_success()  # Thread principal
│   ├── Cria campos faltantes
│   ├── layer.blockSignals(True)
│   ├── try:
│   │   ├── for batch in batches:
│   │   │   ├── layer.changeAttributeValue()
│   │   │   └── QApplication.processEvents()
│   └── finally:
│       └── layer.blockSignals(False)
│
└── on_error()  # Tratamento de erro
```

---

## 📚 REFERÊNCIAS DE CÓDIGO

**Problema Original**: [ANALISE_THREAD_SAFETY.md](ANALISE_THREAD_SAFETY.md)

**Implementação Real**:
- [vector_field_plugin.py](plugins/vector_field_plugin.py) - linhas 82-115 (decisão sync/async)
- [PointFieldsStep.py](core/engine_tasks/PointFieldsStep.py) - linhas 104-137 (blockSignals)
- [LineFieldsStep.py](core/engine_tasks/LineFieldsStep.py) - linhas 88-123 (blockSignals)
- [PolygonFieldsStep.py](core/engine_tasks/PolygonFieldsStep.py) - linhas 104-137 (blockSignals)

---

## ✅ VALIDAÇÃO FINAL

```
✓ Log 02/03/2026: Feature count 1500 → Assíncrono
✓ LineFieldsTask: Computou 1500 features em worker thread
✓ LineFieldsStep: Aplicou batch 0-1500 com blockSignals()
✓ UI responsiva durante processamento
✓ Sem travamento de thread principal
```

---

## 🎯 RESUMO

**NÃO FAÇA**:
- ❌ Loop síncrono na thread principal (< 1000 features OK, > 1000 TRAVA)
- ❌ Task tocando em layer (não é thread-safe)
- ❌ sem blockSignals() (overhead massivo)
- ❌ Sem try/finally (layer fica bloqueada)
- ❌ return em loop de cancelamento (pula finally)
- ✅ usar featureCount() para decisão sync/async, limiar nas preferências

**FAÇA**:
- ✅ featureCount() >= 1000 → AsyncPipelineEngine
- ✅ Task calcula em worker thread, retorna dict
- ✅ Step.on_success() aplica em batch com blockSignals()
- ✅ try/finally com blockSignals(False)
- ✅ break para cancelamento (não return)
- ✅ QApplication.processEvents() a cada batch
- ✅ Detectar CRS geográfico, avisar usuário

---

**Fim do Guia Arquitetônico**

Use este documento como referência ao implementar ANY asynchronous pipeline em QGIS.

