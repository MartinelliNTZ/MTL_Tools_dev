# Análise e Correção: Logs de Adição de Itens

## 🔍 Problema Identificado

No arquivo de log observado, vimos:

```json
{"ts": "2026-02-27T22:09:15", "level": "INFO", "class": "LogcatDialog", "msg": "_on_file_changed: 4 novas entradas carregadas"}
{"ts": "2026-02-27T22:09:15", "level": "INFO", "class": "LogcatDialog", "msg": "_on_file_changed: 1 novas entradas carregadas"}
{"ts": "2026-02-27T22:09:16", "level": "INFO", "class": "LogcatDialog", "msg": "_on_file_changed: 1 novas entradas carregadas"}
...infinitamente...
```

### ❌ Problema: Faltam Logs Intermediários

Os logs esperados que **DEVERIAM APARECER** mas não estão:
- `"Usando append_entries para novas linhas"`
- `"append_entries completado com sucesso"`
- Logs detalhados de `beginInsertRows`
- Logs detalhados de `endInsertRows`

**Isso significa**: O código dentro do try/except de `append_entries` ou `blockSignals()` está **falhando silenciosamente** ou **não sendo executado**.

---

## ✅ Correções Implementadas

### 1. Melhor Rastreamento em `_on_file_changed()`
📄 `logcat_dialog.py`

```python
self._logger.debug(f"load_incremental retornou: {len(new_entries) if new_entries else 0} entradas")
self._logger.debug(f"BlockSignals: True")
self.table_view.blockSignals(True)
self._logger.debug(f"Chamando append_entries com {len(new_entries)} entradas")
self.table_model.append_entries(new_entries)
self._logger.debug("Desbloqueando signals")
self.table_view.blockSignals(False)
```

✅ **Agora cada passo é logado individualmente**

---

### 2. Logging Detalhado em `append_entries()`
📄 `log_table_model.py`

```python
self._logger.debug(f"append_entries: Before - entries count: {len(self._entries)}")
self._logger.debug("Chamando beginInsertRows")
self.beginInsertRows(QModelIndex(), start_row, end_row)
self._logger.debug("beginInsertRows chamado com sucesso")

self._logger.debug(f"Estendendo entries list com {entries_count} novos items")
self._entries.extend(entries)
self._logger.debug(f"append_entries: After extend - entries count: {len(self._entries)}")

self._logger.debug("Chamando endInsertRows")
self.endInsertRows()
self._logger.debug("endInsertRows chamado com sucesso")
```

✅ **Rastreamento de cada chamada Qt interna**

---

### 3. Logging em `rowCount()`
📄 `log_table_model.py`

```python
def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
    """Retorna número de linhas."""
    if parent.isValid():
        return 0
    count = len(self._entries)
    # Log apenas a cada 100 chamadas para evitar spam
    if count % 100 == 0 or count < 10:
        self._logger.debug(f"rowCount chamado: {count} linhas")
    return count
```

✅ **Evita spam excessivo enquanto monitora sincronização de rowCount**

---

## 📊 Padrões de Log Esperados (Após Correção)

### ✅ Fluxo Normal de uma Atualização

```json
{"level": "INFO", "msg": "_on_file_changed: 1 novas entradas carregadas"}
{"level": "DEBUG", "msg": "load_incremental retornou: 1 entradas"}
{"level": "DEBUG", "msg": "BlockSignals: True"}
{"level": "DEBUG", "msg": "Chamando append_entries com 1 entradas"}
{"level": "DEBUG", "msg": "append_entries: Before - entries count: 50"}
{"level": "DEBUG", "msg": "Chamando beginInsertRows"}
{"level": "DEBUG", "msg": "beginInsertRows chamado com sucesso"}
{"level": "DEBUG", "msg": "Estendendo entries list com 1 novos items"}
{"level": "DEBUG", "msg": "append_entries: After extend - entries count: 51"}
{"level": "DEBUG", "msg": "Chamando endInsertRows"}
{"level": "DEBUG", "msg": "endInsertRows chamado com sucesso"}
{"level": "DEBUG", "msg": "append_entries: sucesso. Total de entradas agora: 51"}
{"level": "DEBUG", "msg": "Desbloqueando signals"}
{"level": "DEBUG", "msg": "append_entries completado com sucesso"}
```

Se você vê este padrão completo: ✅ **Tudo funciona**

---

### ❌ Padrão de Erro Esperado

Se houver erro, você verá:

```json
{"level": "DEBUG", "msg": "Chamando append_entries com 1 entradas"}
{"level": "DEBUG", "msg": "Erro em beginInsertRows: RuntimeError..."}
{"level": "ERROR", "msg": "Erro em append_entries: RuntimeError...", "data": {"error_type": "RuntimeError"}}
```

**Neste caso**: O erro está em `beginInsertRows()` ou `endInsertRows()` - problema de Qt sincronização.

---

## 🔧 Próximos Passos

1. **Abra Logcat novamente**
2. **Monitore o arquivo de log em tempo real**
3. **Procure pelos logs detalhados de `append_entries`**
4. **Se vir o fluxo completo**: Problema resolvido ✅
5. **Se vir erro específico**: Saberemos exatamente qual função falha ❌

---

## 🎯 Por Que Isso Funciona

| Antes | Depois |
|-------|--------|
| Log único: "_on_file_changed: 1 nova entrada" | 10+ logs detalhados mostrando cada passo |
| Sem visibilidade de erros | Erro exato em `beginInsertRows`, `endInsertRows`, etc. |
| Impossível debugar | Sabemos **exatamente** onde falha |

---

## 📝 Arquivo de Log Esperado

Procure em:
```
C:\Users\marti\AppData\Roaming\QGIS\QGIS3\profiles\Martinelli_rs\python\plugins\MTL_Tools\log\
mtl_tools_YYYYMMDD_HHMMSS_pidXXXX.log
```

E procure por:
```
"msg": "append_entries: Before"
"msg": "beginInsertRows"
"msg": "After extend"
"msg": "endInsertRows"
```

Estes são os **indicadores de sucesso** que você está buscando! 🔍
