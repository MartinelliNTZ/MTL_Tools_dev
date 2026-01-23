"""
LOGCAT - API PÚBLICA

Documentação da API pública para desenvolvedores que desejam
integrar ou estender funcionalidades do Logcat.
"""

# ============================================================
# API DE DOMÍNIO (Backend)
# ============================================================

## LogEntry (plugins.logcat.core.model.log_entry)

Modelo de uma entrada de log.

### Importação
```python
from plugins.logcat.core.model.log_entry import LogEntry
```

### Métodos Públicos

#### from_json_line(line: str, line_number: int = 0) -> Optional[LogEntry]
Parse uma linha JSON JSONL em LogEntry.
Retorna None se inválido.

```python
entry = LogEntry.from_json_line('{"ts": "...", "level": "INFO", ...}', 1)
if entry:
    print(entry.level)
```

#### get_timestamp_dt() -> Optional[datetime]
Retorna timestamp como datetime object.

```python
dt = entry.get_timestamp_dt()
if dt:
    print(f"Hora: {dt.hour}:{dt.minute}")
```

#### get_short_message(max_length: int = 100) -> str
Retorna mensagem truncada para tabela.

```python
msg = entry.get_short_message(50)  # Máx 50 caracteres
```

#### get_full_message() -> str
Retorna mensagem completa com traceback se houver.

```python
msg = entry.get_full_message()  # Pode ser muito longo
print(msg)
```

#### get_full_details() -> str
Retorna todos os detalhes para cópia/debug.

```python
details = entry.get_full_details()
clipboard.setText(details)
```

### Atributos Públicos
- ts: str                    # Timestamp ISO
- level: str                 # DEBUG, INFO, WARNING, ERROR, CRITICAL
- plugin: str                # Nome do plugin
- plugin_version: str        # Versão
- session_id: str            # UUID da sessão
- pid: int                   # Process ID
- thread: str                # Nome da thread
- tool: str                  # Chave da ferramenta
- class_name: str            # Nome da classe
- msg: str                   # Mensagem
- data: Dict                 # Dados adicionais (JSON)


## LogSession (plugins.logcat.core.model.log_session)

Modelo de uma sessão (arquivo de log).

### Importação
```python
from plugins.logcat.core.model.log_session import LogSession
```

### Métodos Públicos

#### exists() -> bool
Verifica se arquivo ainda existe.

#### get_file_size() -> int
Retorna tamanho em bytes.

#### get_modification_time() -> Optional[datetime]
Retorna tempo da última modificação.

### Atributos Públicos
- log_file_path: Path       # Path do arquivo
- name: str                 # Nome amigável
- display_name: str         # Para UI
- session_id: Optional[str] # UUID da sessão (lido do primeiro evento)


## LogSessionManager (plugins.logcat.core.model.log_session_manager)

Gerenciador de sessões disponíveis.

### Importação
```python
from plugins.logcat.core.model.log_session_manager import LogSessionManager
```

### Construtor
```python
manager = LogSessionManager(Path("/raiz/log"))
```

### Métodos Públicos

#### refresh() -> None
Rescane pasta para descobrir novas sessões.

```python
manager.refresh()
sessions = manager.get_sessions()
```

#### get_sessions() -> List[LogSession]
Retorna todas as sessões (mais recentes primeiro).

```python
sessions = manager.get_sessions()
for session in sessions:
    print(session.display_name)
```

#### get_latest_session() -> Optional[LogSession]
Retorna sessão mais recente.

```python
latest = manager.get_latest_session()
if latest:
    print(f"Última: {latest.name}")
```

#### get_session_by_name(name: str) -> Optional[LogSession]
Procura sessão pelo nome de arquivo.

```python
session = manager.get_session_by_name("mtl_tools_20260122_112852_pid122308.log")
```

#### count() -> int
Número de sessões disponíveis.

```python
total = manager.count()
```


## LogLoader (plugins.logcat.core.io.log_loader)

Carregador incremental de logs.

### Importação
```python
from plugins.logcat.core.io.log_loader import LogLoader
```

### Construtor
```python
loader = LogLoader(Path("/path/to/file.log"))
```

### Métodos Públicos

#### load_all() -> List[LogEntry]
Carrega TODAS as entradas (reinicializa offset).

```python
entries = loader.load_all()
```

#### load_incremental() -> List[LogEntry]
Carrega apenas NOVAS entradas desde última leitura.

```python
new_entries = loader.load_incremental()
```

#### reset() -> None
Reinicializa para reler desde início.

```python
loader.reset()
```

#### get_position() -> int
Retorna byte offset atual.

```python
pos = loader.get_position()
```

#### get_line_count() -> int
Retorna número de linhas vistas.

```python
count = loader.get_line_count()
```


## LogFileWatcher (plugins.logcat.core.io.log_file_watcher)

Monitorador de arquivo em tempo real.

### Importação
```python
from plugins.logcat.core.io.log_file_watcher import LogFileWatcher
```

### Construtor
```python
def on_change():
    print("Arquivo mudou!")

watcher = LogFileWatcher(
    log_file_path=Path("/path/to/file.log"),
    on_change=on_change,
    check_interval=0.5
)
```

### Métodos Públicos

#### start() -> None
Inicia monitoramento em thread separada.

```python
watcher.start()
```

#### stop() -> None
Para monitoramento.

```python
watcher.stop()
```

#### is_watching() -> bool
Retorna True se está monitorando.

```python
if watcher.is_watching():
    print("Monitorando...")
```


## LogFilterEngine (plugins.logcat.core.filter.log_filter_engine)

Motor de filtros.

### Importação
```python
from plugins.logcat.core.filter.log_filter_engine import LogFilterEngine
```

### Construtor
```python
engine = LogFilterEngine()
```

### Métodos Públicos

#### set_text_filter(text: str, use_regex: bool = False) -> None
Define filtro de texto livre.

```python
engine.set_text_filter("error", use_regex=False)
engine.set_text_filter(r"error_\d+", use_regex=True)
```

#### set_level_filter(levels: Set[str]) -> None
Define filtro de níveis.

```python
engine.set_level_filter({"ERROR", "CRITICAL"})
```

#### set_tool_filter(tools: Set[str]) -> None
Define filtro de ferramentas.

```python
engine.set_tool_filter({"system", "vector_field"})
```

#### set_class_filter(classes: Set[str]) -> None
Define filtro de classes.

```python
engine.set_class_filter({"VectorUtils", "LogUtils"})
```

#### set_time_range(start: Optional[datetime] = None, end: Optional[datetime] = None) -> None
Define intervalo de tempo.

```python
from datetime import datetime
start = datetime(2026, 1, 22, 11, 0, 0)
end = datetime(2026, 1, 22, 12, 0, 0)
engine.set_time_range(start, end)
```

#### clear_all() -> None
Limpa todos os filtros.

```python
engine.clear_all()
```

#### apply(entries: List[LogEntry]) -> List[LogEntry]
Aplica todos os filtros.

```python
filtered = engine.apply(all_entries)
```

#### get_unique_levels(entries: List[LogEntry]) -> Set[str]
Retorna níveis únicos.

```python
levels = engine.get_unique_levels(all_entries)
print(levels)  # {'ERROR', 'INFO', 'WARNING', ...}
```

#### get_unique_tools(entries: List[LogEntry]) -> Set[str]
Retorna ferramentas únicas.

```python
tools = engine.get_unique_tools(all_entries)
```

#### get_unique_classes(entries: List[LogEntry]) -> Set[str]
Retorna classes únicas.

```python
classes = engine.get_unique_classes(all_entries)
```


## ClassColorProvider (plugins.logcat.core.color.class_color_provider)

Gerador determinístico de cores para classes.

### Importação
```python
from plugins.logcat.core.color.class_color_provider import ClassColorProvider
```

### Construtor
```python
provider = ClassColorProvider()
```

### Métodos Públicos

#### get_color(class_name: str) -> str
Retorna cor em hex para classe.

```python
color = provider.get_color("VectorUtils")
print(color)  # Ex: "#FF6B4A"
```

#### clear_cache() -> None
Limpa cache de cores.

```python
provider.clear_cache()
```


## ToolKeyColorProvider (plugins.logcat.core.color.tool_key_color_provider)

Mapeador de cores para ferramentas.

### Importação
```python
from plugins.logcat.core.color.tool_key_color_provider import ToolKeyColorProvider
```

### Construtor
```python
provider = ToolKeyColorProvider()
# ou com colors customizadas
custom = {"my_tool": "#ABCDEF"}
provider = ToolKeyColorProvider(custom)
```

### Métodos Públicos

#### get_color(tool_key: str) -> str
Retorna cor para ferramenta.

```python
color = provider.get_color("system")
print(color)  # Ex: "#FF6B6B"
```

#### set_color(tool_key: str, color: str) -> None
Define cor para ferramenta.

```python
provider.set_color("my_tool", "#ABCDEF")
```

#### reset_to_defaults() -> None
Restaura cores padrão.

```python
provider.reset_to_defaults()
```

#### get_all_colors() -> Dict[str, str]
Retorna dicionário completo.

```python
colors = provider.get_all_colors()
```


# ============================================================
# API DE UI (Qt)
# ============================================================

## LogTableModel (plugins.logcat.ui.log_table_model)

Modelo Qt para tabela de logs.

### Importação
```python
from plugins.logcat.ui.log_table_model import LogTableModel
from qgis.PyQt.QtWidgets import QTableView
```

### Construtor e Uso
```python
model = LogTableModel()
table_view = QTableView()
table_view.setModel(model)

# Adicionar dados
model.set_entries(all_entries)

# Ou adicionar incrementalmente
model.append_entries(new_entries)

# Obter entrada para detalhe
entry = model.get_entry(index)
```

### Métodos Públicos

#### set_entries(entries: List[LogEntry]) -> None
Define todas as entradas (re-render completo).

#### append_entries(entries: List[LogEntry]) -> None
Adiciona novas entradas (incremental).

#### clear() -> None
Limpa modelo.

#### rowCount() -> int
Retorna número de linhas.

#### columnCount() -> int
Retorna número de colunas.

#### get_entry(index: QModelIndex) -> Optional[LogEntry]
Retorna LogEntry em índice.

#### get_all_entries() -> List[LogEntry]
Retorna todas as entradas.


## LogDetailDialog (plugins.logcat.ui.log_detail_dialog)

Diálogo de visualização detalhada.

### Importação
```python
from plugins.logcat.ui.log_detail_dialog import LogDetailDialog
```

### Construtor e Uso
```python
dialog = LogDetailDialog(entry, parent)
dialog.exec_()
```


## LogcatDialog (plugins.logcat.ui.logcat_dialog)

Diálogo principal (não recomendado para subclassear).

### Importação
```python
from plugins.logcat.ui.logcat_dialog import LogcatDialog
from pathlib import Path
```

### Construtor e Uso
```python
plugin_root = Path(__file__).parent
dialog = LogcatDialog(plugin_root, parent_widget)
dialog.exec_()
```


# ============================================================
# EXEMPLOS DE USO
# ============================================================

## Exemplo 1: Carregar e filtrar logs programaticamente

```python
from pathlib import Path
from plugins.logcat.core.model.log_session_manager import LogSessionManager
from plugins.logcat.core.io.log_loader import LogLoader
from plugins.logcat.core.filter.log_filter_engine import LogFilterEngine

# Descobrir e carregar sessão mais recente
manager = LogSessionManager(Path("raiz/log"))
session = manager.get_latest_session()

if session:
    loader = LogLoader(session.log_file_path)
    entries = loader.load_all()
    
    # Filtrar apenas erros
    engine = LogFilterEngine()
    engine.set_level_filter({"ERROR", "CRITICAL"})
    errors = engine.apply(entries)
    
    for error in errors:
        print(f"{error.ts} | {error.class_name}: {error.msg}")
```

## Exemplo 2: Monitorar logs em tempo real

```python
from plugins.logcat.core.io.log_file_watcher import LogFileWatcher
from plugins.logcat.core.io.log_loader import LogLoader

def on_new_logs():
    new = loader.load_incremental()
    print(f"Novas entradas: {len(new)}")
    for entry in new:
        print(f"  {entry.level}: {entry.msg}")

loader = LogLoader(Path("raiz/log/mtl_tools_*.log"))
watcher = LogFileWatcher(
    log_file_path=Path("raiz/log/mtl_tools_*.log"),
    on_change=on_new_logs,
    check_interval=1.0
)

watcher.start()
# ... rodar QGIS ...
watcher.stop()
```

## Exemplo 3: Cores customizadas

```python
from plugins.logcat.core.color.tool_key_color_provider import ToolKeyColorProvider
from plugins.logcat.core.color.class_color_provider import ClassColorProvider

# Cores de ferramentas
tool_colors = ToolKeyColorProvider()
tool_colors.set_color("my_custom_tool", "#FF00FF")

# Cores de classes
class_colors = ClassColorProvider()
color = class_colors.get_color("MyClass")  # Sempre mesma cor
```

## Exemplo 4: Usar em diálogo customizado

```python
from qgis.PyQt.QtWidgets import QDialog, QVBoxLayout, QTableView, QPushButton
from plugins.logcat.ui.log_table_model import LogTableModel
from plugins.logcat.core.model.log_session_manager import LogSessionManager
from plugins.logcat.core.io.log_loader import LogLoader
from pathlib import Path

class MyLogDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Backend
        manager = LogSessionManager(Path("raiz/log"))
        session = manager.get_latest_session()
        loader = LogLoader(session.log_file_path)
        entries = loader.load_all()
        
        # UI
        model = LogTableModel()
        model.set_entries(entries)
        
        table = QTableView()
        table.setModel(model)
        
        layout = QVBoxLayout()
        layout.addWidget(table)
        self.setLayout(layout)
```

# ============================================================
# BOAS PRÁTICAS
# ============================================================

1. **Sempre verificar None**
   ```python
   session = manager.get_latest_session()
   if session:
       # usar session
   ```

2. **Respeitar thread-safety**
   ```python
   # LogLoader/LogFileWatcher já são thread-safe
   # Mas não copiar reference para múltiplas threads
   ```

3. **Reusar componentes**
   ```python
   # Bom: uma instância por diálogo
   manager = LogSessionManager(...)
   
   # Ruim: criar nova instância a cada operação
   ```

4. **Usar constantes corretas**
   ```python
   # LogUtils.LEVEL_COLORS para níveis
   from core.config.LogUtils import LogUtils
   color = LogUtils.LEVEL_COLORS["ERROR"]
   ```

# ============================================================
# LIMITAÇÕES
# ============================================================

1. **Não salva estado entre execuções**
2. **Suporta apenas formato JSONL**
3. **Monitor tem latência ~0.5-1 segundo**
4. **Cores de classes autogeneradas (não customizáveis por classe)**

# ============================================================
# VERSIONING
# ============================================================

API Versão: 1.0 (Logcat 1.0)
Compatibilidade: QGIS 3.16+
Python: 3.6+

# ============================================================
