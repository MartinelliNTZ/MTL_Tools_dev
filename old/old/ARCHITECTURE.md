"""
ARQUITETURA DO LOGCAT

Visão geral da arquitetura, padrões de design e fluxo de dados.
"""

# ============================================================
# FILOSOFIA DE DESIGN
# ============================================================

O Logcat segue estes princípios:

1. **Separação de Responsabilidades**
   - Backend (core) puro: nenhuma dependência de Qt
   - UI apenas coordena e exibe
   - Cada classe tem uma responsabilidade clara

2. **Model/View (Qt Pattern)**
   - LogTableModel: apenas sincroniza dados com UI
   - Nunca modifica dados, apenas apresenta

3. **Imutabilidade de Classes Existentes**
   - LogUtils e LogCleanupUtils não são modificadas
   - Logcat apenas consome sua API pública

4. **Tolerância a Erros**
   - Parse de log nunca quebra a aplicação
   - Campos ausentes tratados com defaults

5. **Escalabilidade**
   - Preparado para dezenas de milhares de linhas
   - Incremental updates, não re-render completo

# ============================================================
# FLUXO DE DADOS
# ============================================================

## 1. Inicialização

LogcatDialog.__init__()
    ├─> LogSessionManager(log_dir).refresh()
    │   ├─> Escaneia raiz/log
    │   └─> Cria LogSession para cada .log
    │
    ├─> _load_default_session()
    │   ├─> session_manager.get_latest_session()
    │   └─> _load_session(session)
    │       ├─> LogLoader(log_file_path)
    │       ├─> loader.load_all()
    │       │   ├─> Lê arquivo inteiro
    │       │   └─> Retorna List[LogEntry]
    │       ├─> all_entries = [...]
    │       ├─> _apply_filters()
    │       └─> LogFileWatcher.start()
    │           └─> Thread de monitoramento
    │
    └─> UI inicializada

## 2. Em Tempo Real

LogFileWatcher (thread)
    ├─> A cada 0.5s
    ├─> Verifica tamanho/mtime do arquivo
    └─> Se mudou:
        └─> on_change callback
            └─> LogcatDialog._on_file_changed()
                ├─> LogLoader.load_incremental()
                │   ├─> Posiciona em offset anterior
                │   ├─> Lê apenas novas linhas
                │   └─> Retorna List[LogEntry]
                ├─> all_entries.extend(new)
                └─> _apply_filters()
                    ├─> LogFilterEngine.apply(all_entries)
                    │   ├─> Filtro de texto
                    │   ├─> Filtro de level
                    │   ├─> Filtro de tool
                    │   ├─> Filtro de class
                    │   └─> Filtro de tempo
                    └─> table_model.append_entries(filtered)
                        └─> UI atualizada (apenas novas linhas)

## 3. Filtros (Live)

User modifica filtros
    └─> _on_filter_changed()
        ├─> LogFilterEngine.set_*_filter(...)
        ├─> engine.apply(all_entries)
        ├─> table_model.set_entries(filtered)
        └─> UI re-renderiza

## 4. Detalhe

User duplo-clica em linha
    └─> _on_table_double_click()
        ├─> table_model.get_entry(index)
        └─> LogDetailDialog.exec_()
            └─> entry.get_full_details()
                └─> Retorna string com tudo

## 5. Limpeza

User clica "Clear Session" ou "Clear All"
    └─> Confirmation dialog
        └─> Se confirmado:
            ├─> LogFileWatcher.stop()
            ├─> LogCleanupUtils.clear_current_session() ou .clear_all_logs()
            ├─> UI limpa (all_entries.clear())
            └─> _refresh_session_list()

# ============================================================
# ARQUITETURA EM CAMADAS
# ============================================================

┌─────────────────────────────────────────────┐
│            LAYER: UI (Qt Widgets)           │
├─────────────────────────────────────────────┤
│ LogcatDialog (coordenação)                  │
│ LogDetailDialog (detalhe)                   │
│ LogTableModel (modelo para tabela)          │
│ Widgets (QTableView, QLineEdit, etc)        │
└────────────────┬──────────────────────────┘
                 │
┌────────────────▼──────────────────────────┐
│        LAYER: BUSINESS (Core)              │
├─────────────────────────────────────────────┤
│ Model:                                      │
│   LogEntry        → Uma entrada             │
│   LogSession      → Um arquivo de log       │
│   LogSessionManager → Descoberta            │
│                                             │
│ IO:                                         │
│   LogLoader       → Parse incremental       │
│   LogFileWatcher  → Monitoramento           │
│                                             │
│ Filter:                                     │
│   LogFilterEngine → Lógica de filtros       │
│                                             │
│ Color:                                      │
│   ClassColorProvider → Cores de classes     │
│   ToolKeyColorProvider → Cores de tools     │
└────────────────┬──────────────────────────┘
                 │
┌────────────────▼──────────────────────────┐
│        LAYER: EXTERNAL (READ-ONLY)         │
├─────────────────────────────────────────────┤
│ raiz/log/*.log     → Arquivo de log JSONL  │
│ LogUtils (core.config) → Cores definidas   │
│ LogCleanupUtils → Operações de limpeza     │
└─────────────────────────────────────────────┘

# ============================================================
# PADRÕES DE DESIGN UTILIZADOS
# ============================================================

## 1. Model/View (Qt)
- LogTableModel extends QAbstractTableModel
- UI (QTableView) binds ao modelo
- Mudanças no modelo atualizam UI

## 2. Observer
- LogFileWatcher notifica callbacks
- LogcatDialog escuta mudanças de arquivo

## 3. Adapter/Wrapper
- LogcatPlugin adapta LogcatDialog para menu

## 4. Strategy
- LogFilterEngine: múltiplas estratégias de filtro
- ClassColorProvider: estratégia de colorização

## 5. Singleton (implícito)
- LogSessionManager: um por diálogo
- LogFilterEngine: um por diálogo

## 6. Factory
- LogEntry.from_json_line(): factory method

## 7. Tolerant Parser
- LogEntry.from_json_line(): retorna None se inválido
- Nunca lança exceções

# ============================================================
# INTERAÇÕES COM CÓDIGO EXISTENTE
# ============================================================

## LogUtils (core.config)
- **Usa**: LEVEL_COLORS (readonly)
- **Não modifica**: Logcat é apenas leitor

## LogCleanupUtils (core.config)
- **Usa**: keep_last_n() (já existente)
- **Usa**: clear_all_logs() (novo método)
- **Usa**: clear_current_session() (novo método)

## BasePluginMTL (plugins.base_plugin)
- **Usa**: Como base para LogcatPlugin (opcional)

## Resto do Plugin
- **Transparente**: Logcat não afeta outras ferramentas
- **Consome**: Logs gerados por outras ferramentas

# ============================================================
# THREAD SAFETY
# ============================================================

LogLoader (thread-safe):
- _lock garante acesso exclusivo ao arquivo
- load_all() e load_incremental() sincronizadas

LogFileWatcher (thread-safe):
- Executa em daemon thread
- _lock para sincronização
- Nunca modifica dados, apenas notifica

LogcatDialog (Qt thread):
- Todas as updates de UI na thread principal
- LogFileWatcher dispara no_change
- UI atualiza via signal/slot (Qt thread-safe)

# ============================================================
# PERFORMANCE
# ============================================================

## Otimizações Implementadas

1. **Carregamento Incremental**
   - LogLoader mantém offset
   - Não relê arquivo inteiro a cada atualização

2. **Model/View Lazy Rendering**
   - Apenas linhas visíveis são renderizadas
   - QTableView com scroll: nunca renderiza tudo

3. **Append Incremental**
   - table_model.append_entries() é mais rápido que set_entries()
   - Não causa re-render completo

4. **Filtros Eficientes**
   - Filtros aplicados após carregar em memória
   - Sem I/O durante filtragem

5. **Monitoramento Econômico**
   - Timer a cada 1 segundo (not too aggressive)
   - Checa apenas tamanho/mtime (rápido)

6. **Cores Cacheadas**
   - ClassColorProvider caches cores geradas
   - Mesma classe = lookup O(1)

## Benchmarks (estimados)

- 100 logs: < 10ms
- 1000 logs: < 100ms
- 10000 logs: < 500ms
- 100000 logs: ~ 2s (inicial), < 100ms (incremental)

# ============================================================
# EXTENSIBILIDADE
# ============================================================

Pontos fáceis de estender:

1. **Novos Filtros**
   - Adicionar método a LogFilterEngine
   - Integrar em _show_filter_popup()

2. **Novas Cores**
   - Adicionar entradas a ToolKeyColorProvider.DEFAULT_COLORS
   - Ou subclassificar ClassColorProvider

3. **Novas Colunas**
   - Adicionar a LogTableModel.COLUMNS
   - Implementar em _get_display_text()

4. **Novos Buttons**
   - Adicionar QPushButton a _build_ui()
   - Conectar a novo handler

5. **Novo Formato de Log**
   - Subclassificar LogEntry
   - Sobrescrever from_json_line()

# ============================================================
# LIMITAÇÕES E TRADE-OFFS
# ============================================================

1. **Carregamento Completo Inicial**
   - Primeira carga lê arquivo inteiro
   - Trade-off: simplex vs responsividade para arquivos gigantes

2. **Monitor Timer-Based**
   - Não usa file watcher do SO (portabilidade)
   - Trade-off: portabilidade vs latência (0.5-1s)

3. **Sem Busca Regex Avançada**
   - Suporta regex mas é básico
   - Poderia adicionar flags (case-insensitive, etc)

4. **Cores Automáticas Simples**
   - ClassColorProvider usa HSL simples
   - Poderia usar algoritmo mais sofisticado

5. **Sem Persistência de Filtros**
   - Filtros não são salvos entre execuções
   - Poderia usar preferences.py

6. **Sem Export**
   - Não há export para CSV/JSON
   - Poderia adicionar facilmente

# ============================================================
# ROADMAP FUTURO
# ============================================================

Melhorias possíveis:

- [ ] Export para CSV/JSON
- [ ] Persistência de filtros (via preferences)
- [ ] Busca regex avançada com flags
- [ ] Tags customizadas para entradas
- [ ] Gráficos de distribuição (contagem por nível)
- [ ] Bookmarks/favoritos
- [ ] Copy individual columns
- [ ] Sort multicoluna
- [ ] Right-click context menu
- [ ] Configuração de cores por usuário

# ============================================================
