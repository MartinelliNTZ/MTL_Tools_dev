# Guia de Debug do Logcat Crash

## 📋 Resumo das Correções Implementadas

### 1. Logging Extensivo Adicionado
Foram adicionados **try/catch com logging completo** em todos os pontos críticos:

#### **log_sort_filter_proxy_model.py**
- ✅ Validação rigorosa de índices em `lessThan()`
- ✅ Logging de cada passo da comparação
- ✅ Tratamento de erros com fallback seguro
- ✅ Contador de erros (`_lessThan_error_count`)

#### **log_table_model.py**
- ✅ Logging em `set_entries()` com contagem de entradas
- ✅ Logging em `append_entries()` com range de linhas
- ✅ Logging completo em `data()` com contexto de erro
- ✅ Counters: `_set_entries_error_count`, `_data_error_count`

#### **logcat_dialog.py**
- ✅ Logging em `_apply_filters()` com detalhes de cada etapa
- ✅ Logging em `_load_session()` com rastreamento de watcher
- ✅ Logging em `_on_file_changed()` com contagem de novas entradas
- ✅ Logging em `_on_search_text_changed()` com debounce

---

## 🔍 Como Analisar os Logs

### Arquivo de Log
```
C:\Users\marti\AppData\Roaming\QGIS\QGIS3\profiles\Martinelli_rs\python\plugins\MTL_Tools\log\
```

Procure por arquivos com padrão: `mtl_tools_YYYYMMDD_HHMMSS_pidXXXX.log`

### Estrutura dos Logs
Cada linha é um JSON com campos:
```json
{
  "ts": "2026-02-27T21:56:28",
  "level": "ERROR",
  "plugin": "MTL Tools",
  "plugin_version": "1.3.0",
  "session_id": "...",
  "pid": 9264,
  "thread": "MainThread",
  "tool": "logcat",
  "class": "LogSortFilterProxyModel",
  "msg": "Erro em lessThan",
  "data": {
    "error_type": "IndexError",
    "left_row": 100,
    "right_row": 150,
    "entries_len": 95
  }
}
```

---

## 🎯 Passos para Reproduzir e Debugar

### 1. Abrir Logcat
```
QGIS → Plugins → MTL Tools → Logcat
```

### 2. Digitar na Barra de Pesquisa
```
Escreva qualquer texto: "test", "error", etc.
Observe se o crash ocorre
```

### 3. Verificar Logs Imediatamente
```
1. Feche QGIS
2. Abra o arquivo de log mais recente
3. Procure por "ERROR" ou "CRITICAL"
4. Identifique o padrão do erro
```

---

## 📊 Padrões de Erro Esperados

### Padrão 1: Índices Inválidos em lessThan
```json
{
  "level": "DEBUG",
  "class": "LogSortFilterProxyModel",
  "msg": "Índices inválidos em lessThan",
  "data": {
    "left_valid": false,
    "right_valid": true
  }
}
```
**Ação**: Isso é OK - o proxy model está se sincronizando. Não é um crash.

### Padrão 2: Fora do Range em lessThan
```json
{
  "level": "DEBUG",
  "class": "LogSortFilterProxyModel",
  "msg": "Índices fora do range em lessThan",
  "data": {
    "entries_len": 100,
    "left_row": 105,
    "right_row": 110
  }
}
```
**Ação**: O proxy tentou acessar linhas que não existem. Isso é tratado graciosamente.

### Padrão 3: Erro em _apply_filters
```json
{
  "level": "ERROR",
  "class": "LogcatDialog",
  "msg": "Erro em _apply_filters: ...",
  "data": {
    "error_type": "RuntimeError",
    "all_entries_count": 5000
  }
}
```
**Ação**: Identifique o tipo específico e busque logs anteriores para contexto.

### Padrão 4: Crash Catastrófico
Se você vir:
```json
{
  "level": "CRITICAL",
  "class": "LogSortFilterProxyModel",
  "msg": "Erro CRÍTICO não esperado em lessThan"
}
```
**Ação**: Este é um erro não esperado. Capture a mensagem completa e o tipo de erro.

---

## 🛠️ Diagnóstico de Crash C++

Se QGIS crashear (crash_id fornecido), os logs podem não ser escritos. Nesse caso:

### 1. Verificar Eventos Recentes
```
Busque no log:
- "_on_search_text_changed disparado"
- "_apply_filters começando"
- "Índices fora do range"
```

### 2. Reproduzir com GDB (Se possível)
```bash
gdb qgis
(gdb) run
```

### 3. Habilitar Mais Logging
Se necessário, você pode aumentar o nível de logging em:
- `LogUtilsNew.init()` → alterar nível padrão para DEBUG

---

## 📈 Métricas nos Logs

Procure por estas linhas para entender o comportamento:

### Contadores de Erro
```
"_set_entries_error_count": 0  # Número de vezes que set_entries falhou
"_data_error_count": 0         # Número de vezes que data() falhou
"_lessThan_error_count": 0     # Número de vezes que lessThan falhou
```

### Fluxo Normal (Esperado)
```
[INFO] LogcatDialog inicialização completa
[DEBUG] _apply_filters começando
[DEBUG] _apply_filters completa com sucesso
[DEBUG] _on_search_text_changed disparado
[DEBUG] Debounce timer iniciado (300ms)
```

---

## 🚨 Ações Recomendadas

### Se Você Ver Muitos Logs DEBUG
Isso é normal durante digitação intensa. Os logs mostram cada passo.

### Se Você Ver Erros de Índice
Verifique se há mensagens de `layoutChanged` que causam desincronização.

### Se Você Ver RuntimeError
Procure por contexto que leveou ao erro (mensagem anterior).

### Se QGIS Crashear Sem Logs
O crash é C++ puro. Neste caso:
1. Reduza o número de entradas de log (delete arquivos antigos)
2. Use QGIS 3.34 em vez de 3.16 (Qt 5.11 tem bugs conhecidos)
3. Reporte com stack trace e arquivo de log anterior

---

## 📝 Exemplos de Análise

### Exemplo 1: Busca Rápida Causando Erro
```
[DEBUG] _on_search_text_changed disparado
[DEBUG] Debounce timer iniciado (300ms)
[DEBUG] _on_search_debounce_timeout
[DEBUG] _apply_filters começando
[DEBUG] Texto de busca: 'err'
[DEBUG] Aplicando filtros em 50000 entradas
[ERROR] Erro em set_entries: RuntimeError
```
**Diagnóstico**: 50000 entradas é muito. Implementar paginação.

### Exemplo 2: Proxy Model Desincronizado
```
[DEBUG] set_entries chamado com 100 entradas
[DEBUG] layoutChanged emitido com sucesso
[DEBUG] Índices fora do range em lessThan
[DEBUG] entries_len=100, left_row=105
```
**Diagnóstico**: O proxy ainda tentou acessar índice 105, mas foi tratado.

---

## ✅ Verificação de Sucesso

Você saberá que o problema foi resolvido quando:

1. ✅ Pode digitar rapidamente na barra de pesquisa sem crash
2. ✅ QGIS não fecha/crash ao filtrar logs
3. ✅ Logs mostram fluxo normal de DEBUG sem ERRORs
4. ✅ Performance é boa mesmo com 50000+ entradas

---

## 📞 Próximos Passos

1. **Abra Logcat**
2. **Reproduza o problema**
3. **Capture o arquivo de log**
4. **Analise usando este guia**
5. **Reporte padrão de erro encontrado**

**Arquivo de log será salvo automaticamente** em:
```
MTL_Tools/log/mtl_tools_*.log
```
