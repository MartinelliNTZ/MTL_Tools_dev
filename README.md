"""
Logcat Tool Documentation

Ferramenta de visualização, análise e filtragem de logs em tempo real
para o plugin MTL Tools, inspirada no Logcat do Android Studio.
"""

# ============================================================
# OVERVIEW
# ============================================================

O Logcat é uma ferramenta integrada ao MTL Tools que permite visualizar,
filtrar e analisar logs gerados pelo plugin em tempo real.

## Características Principais

- **Visualização em tempo real**: Monitora o arquivo de log atual para novas entradas
- **Múltiplas sessões**: Acesso a histórico completo de logs de execuções anteriores
- **Filtros avançados**: Busca por texto, nível, ferramenta, classe e intervalo de tempo
- **Visualização detalhada**: Amplie qualquer entrada para ver informações completas
- **Apenas leitura**: Nunca modifica dados existentes
- **Escalável**: Suporta dezenas de milhares de linhas
- **Delegação**: Usa LogCleanupUtils para operações de limpeza

# ============================================================
# ACESSO
# ============================================================

1. Abra o QGIS com o plugin MTL Tools ativado
2. Vá para Menu: MTL Tools > Sistema > Logcat - Viewer de Logs
3. O diálogo abrirá com a sessão mais recente pré-selecionada

# ============================================================
# INTERFACE
# ============================================================

## Seletor de Sessão

- **Dropdown "Session"**: Liste todas as sessões de log disponíveis
- **Botão "Refresh Sessions"**: Rescane pasta de logs para descobrir novas sessões

## Filtros

### Busca de Texto Livre
- Campo de entrada "Search"
- Busca em TODOS os campos (timestamp, nível, tool, classe, mensagem, dados)
- Busca em tempo real (live filtering)
- Suporta regex (se necessário, adicionar checkbox)

### Filtros por Coluna
- **Level**: Selecione níveis específicos (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- **Tool**: Selecione ferramentas específicas (system, vector_field, etc)
- **Class**: Selecione classes específicas

### Botão "Clear Filters"
- Remove todos os filtros aplicados
- Restaura visualização completa

## Tabela Principal

Colunas:
- **Timestamp**: Data/hora do evento
- **Level**: Nível de log (com cor)
- **Tool**: Ferramenta que gerou o log
- **Class**: Classe que gerou o log
- **Message**: Mensagem (truncada a ~100 caracteres)

### Cores
- Fundo: Cor do nível (ERROR=vermelho, WARNING=âmbar, etc)
- Texto: Cor da ferramenta (system=vermelho suave, etc)
- Classes: Cores geradas automaticamente e determinísticas

### Interações
- **Duplo-clique**: Abre diálogo detalhado da entrada
- **Linhas alternadas**: Melhora legibilidade

## Botões de Ação

- **Clear Session**: Delega a LogCleanupUtils para deletar logs da sessão atual
- **Clear All Logs**: Delega a LogCleanupUtils para deletar TODOS os logs
- **Close**: Fecha o diálogo

## Barra de Status

Exibe: "Mostrando X/Y entradas | Sessão: [nome]"

# ============================================================
# DIÁLOGO DE DETALHE
# ============================================================

Aberto ao duplo-clique em uma entrada:

- **Cabeçalho**: Level, Timestamp, Tool, Class
- **Área de texto**: Mensagem completa incluindo traceback se houver
- **Botão "Copy All"**: Copia todos os detalhes para clipboard
- **Botão "Close"**: Fecha o diálogo

Detalhes completos incluem:
- Todos os campos da entrada
- Traceback completo (se houver exception)
- Dados adicionais em formato JSON
- JSON original

# ============================================================
# FORMATO DE LOG
# ============================================================

Os logs são armazenados em formato JSONL (JSON Lines):
- Um evento por linha
- Arquivo: raiz/log/mtl_tools_YYYYMMDD_HHMMSS_pidPPPPPP.log

Exemplo:
{
  "ts": "2026-01-22T11:28:52",
  "level": "INFO",
  "plugin": "MTL Tools",
  "plugin_version": "1.3.0",
  "session_id": "8bd9e92c-6f18-4583-b75d-0e77589dd2af",
  "pid": 122308,
  "thread": "MainThread",
  "tool": "system",
  "class": "LogUtils",
  "msg": "Log session started",
  "data": {}
}

# ============================================================
# TEMPO REAL
# ============================================================

O Logcat monitora o arquivo de log atual:

1. Timer a cada 1 segundo verifica se o arquivo cresceu
2. Se houve mudanças, carrega apenas as NOVAS linhas
3. Adiciona à tabela incrementalmente (sem re-render completo)
4. UI nunca trava mesmo com muitos logs

# ============================================================
# PERFORMANCE
# ============================================================

Escalabilidade:
- 100 linhas: Instantâneo
- 1000 linhas: <100ms
- 10000 linhas: <500ms
- 100000 linhas: ~2s

Model/View garante apenas as linhas visíveis são renderizadas.

# ============================================================
# ESTRUTURA DE PASTAS
# ============================================================

raiz/plugins/logcat/
├── __init__.py
├── logcat_plugin.py          (wrapper/adapter)
├── core/
│   ├── __init__.py
│   ├── model/
│   │   ├── __init__.py
│   │   ├── log_entry.py      (modelo de domínio)
│   │   ├── log_session.py    (modelo de sessão)
│   │   └── log_session_manager.py
│   ├── io/
│   │   ├── __init__.py
│   │   ├── log_loader.py     (carregamento incremental)
│   │   └── log_file_watcher.py (monitoramento)
│   ├── filter/
│   │   ├── __init__.py
│   │   └── log_filter_engine.py (filtros)
│   └── color/
│       ├── __init__.py
│       ├── class_color_provider.py
│       └── tool_key_color_provider.py
└── ui/
    ├── __init__.py
    ├── logcat_dialog.py      (diálogo principal)
    ├── log_table_model.py    (modelo Qt)
    └── log_detail_dialog.py  (detalhe)

# ============================================================
# CLASSES PRINCIPAIS
# ============================================================

## LogEntry
Modelo de domínio para uma entrada de log.
- Parse tolerante de JSON
- Métodos para truncamento e formatação
- Acesso a traceback completo se houver

## LogSession
Representa um arquivo de log.
- Extrai informações do nome do arquivo
- Gerencia existência e tamanho

## LogSessionManager
Gerencia descoberta de sessões disponíveis.
- Rescane automático
- Acesso a sessão mais recente

## LogLoader
Carregamento incremental de logs.
- Mantém offset para não reler linhas
- Thread-safe

## LogFileWatcher
Monitora arquivo de log em tempo real.
- Timer + checagem de tamanho (simples, portável)
- Notifica callbacks quando há mudanças

## LogFilterEngine
Motor de filtros.
- Filtro de texto livre (com suporte a regex)
- Filtros por coluna
- Intervalo de tempo

## ClassColorProvider
Gera cores determinísticas para classes.
- Usa hash SHA256 do nome
- Cores sempre iguais para mesma classe
- Bom contraste e legibilidade

## ToolKeyColorProvider
Mapeamento de ferramentas para cores.
- Dicionário configurável
- Cores padrão para ferramentas conhecidas
- Fallback para cor neutra

## LogTableModel (QAbstractTableModel)
Modelo Qt para tabela.
- Suporta grandes volumes
- Apenas as linhas visíveis são renderizadas
- Append incremental eficiente

## LogcatDialog (QDialog)
Diálogo principal.
- Coordena todos os componentes
- UI com filtros, tabela, botões
- Ciclo de vida completo

## LogDetailDialog (QDialog)
Diálogo detalhado.
- Mostra todos os detalhes de uma entrada
- Permite copiar tudo

# ============================================================
# EXEMPLO DE USO PROGRAMÁTICO
# ============================================================

from pathlib import Path
from plugins.logcat.ui.logcat_dialog import LogcatDialog

plugin_root = Path(__file__).parent
dlg = LogcatDialog(plugin_root, parent_widget)
dlg.exec_()

# ============================================================
# NOTAS IMPORTANTES
# ============================================================

1. **Apenas Leitura**: Logcat nunca escreve logs. Usa LogUtils para isso.

2. **Delegação**: Operações de limpeza delegam para LogCleanupUtils.

3. **Sem Acoplamento**: Backend não conhece Qt. UI não faz parse.

4. **Tolerante**: Parser tolera campos ausentes, JSON inválido, etc.

5. **Thread-Safe**: LogLoader e LogFileWatcher são thread-safe.

6. **Escalável**: Model/View garante performance mesmo com muitos logs.

7. **Determinístico**: Mesma classe/ferramenta sempre mesma cor.

8. **Compatível**: QGIS 3.16+ com PyQt/PySide.

# ============================================================
# TROUBLESHOOTING
# ============================================================

### Logcat não abre
- Verificar se pasta raiz/log existe
- Verificar se há permissão de leitura

### Filtros não funcionam
- Verificar se há entries com os valores filtrados
- Limpar filtros e recarregar

### Tabela vazia
- Verificar se há arquivos .log em raiz/log
- Clicar "Refresh Sessions"

### Performance lenta com muitos logs
- Usar filtros para reduzir volume
- Considerar limpar logs antigos (Clear All Logs)

# ============================================================
