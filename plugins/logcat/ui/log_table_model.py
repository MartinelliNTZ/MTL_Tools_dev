"""
Modelo Qt para tabela de logs.

Implementa QAbstractTableModel para suportar grandes volumes de dados.
Nenhuma lógica de UI aqui - apenas model puro.
"""
from typing import List, Optional
from qgis.PyQt.QtCore import Qt, QAbstractTableModel, QModelIndex, QVariant
from qgis.PyQt.QtGui import QColor
from ..core.model.log_entry import LogEntry
from ..core.color.class_color_provider import ClassColorProvider


class LogTableModel(QAbstractTableModel):
    """
    Modelo Qt para exibição de logs em tabela.
    
    Colunas:
    - Timestamp
    - Level
    - Tool
    - Class
    - Message (truncada)
    """
    
    COLUMNS = [
        ("Timestamp", "ts"),
        ("Level", "level"),
        ("Tool", "tool"),
        ("Class", "class_name"),
        ("Message", "msg"),
    ]
    
    def __init__(self, parent=None):
        """Inicializa o modelo."""
        super().__init__(parent)
        self._entries: List[LogEntry] = []
        # Usar ClassColorProvider para AMBAS as colunas (tool + class)
        # Cores determinísticas e consistentes para cada valor único
        self._color_provider = ClassColorProvider()
    
    def set_entries(self, entries: List[LogEntry]) -> None:
        """
        Define as entradas a exibir.
        Usa layoutChanged em vez de beginResetModel para preservar seleção.
        """
        self._entries = list(entries)
        # Emitir layoutChanged em vez de beginResetModel
        self.layoutChanged.emit()
    
    def append_entries(self, entries: List[LogEntry]) -> None:
        """
        Adiciona novas entradas ao final.
        Mais eficiente que set_entries para atualizações incrementais.
        """
        if not entries:
            return
        
        start_row = len(self._entries)
        end_row = start_row + len(entries) - 1
        
        self.beginInsertRows(QModelIndex(), start_row, end_row)
        self._entries.extend(entries)
        self.endInsertRows()
    
    def clear(self) -> None:
        """Limpa todas as entradas."""
        self.beginResetModel()
        self._entries.clear()
        self.endResetModel()
    
    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """Retorna número de linhas."""
        if parent.isValid():
            return 0
        return len(self._entries)
    
    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """Retorna número de colunas."""
        if parent.isValid():
            return 0
        return len(self.COLUMNS)
    
    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.DisplayRole
    ) -> QVariant:
        """Retorna cabeçalho das colunas."""
        if role != Qt.DisplayRole:
            return QVariant()
        
        if orientation == Qt.Horizontal and 0 <= section < len(self.COLUMNS):
            return QVariant(self.COLUMNS[section][0])
        
        if orientation == Qt.Vertical:
            return QVariant(str(section + 1))
        
        return QVariant()
    
    def data(
        self,
        index: QModelIndex,
        role: int = Qt.DisplayRole
    ) -> QVariant:
        """Retorna dados para uma célula."""
        if not index.isValid() or not (0 <= index.row() < len(self._entries)):
            return QVariant()
        
        entry = self._entries[index.row()]
        col_name = self.COLUMNS[index.column()][1]
        
        # Dados para exibição
        if role == Qt.DisplayRole:
            return QVariant(self._get_display_text(entry, col_name))
        
        # Cor de texto (level - fonte colorida, não fundo)
        if role == Qt.ForegroundRole and col_name == "level":
            color = self._get_level_color(entry.level)
            return QVariant(QColor(color))
        
        # Cor de texto (tool) - usando ClassColorProvider para determinismo
        if role == Qt.ForegroundRole and col_name == "tool":
            color = self._color_provider.get_color(entry.tool)
            return QVariant(QColor(color))
        
        # Cor de texto (class) - usando ClassColorProvider para determinismo
        if role == Qt.ForegroundRole and col_name == "class_name":
            color = self._color_provider.get_color(entry.class_name)
            return QVariant(QColor(color))
        
        # Tooltip com informação completa
        if role == Qt.ToolTipRole:
            return QVariant(entry.get_full_details())
        
        # User role para acesso programático (retornar entry diretamente)
        if role == Qt.UserRole:
            return entry  # Retornar diretamente, não em QVariant
        
        return QVariant()
    
    def _get_display_text(self, entry: LogEntry, col_name: str) -> str:
        """Retorna texto a exibir para uma coluna."""
        if col_name == "ts":
            return entry.ts or "N/A"
        elif col_name == "level":
            return entry.level
        elif col_name == "tool":
            return entry.tool
        elif col_name == "class_name":
            return entry.class_name
        elif col_name == "msg":
            return entry.get_short_message(100)
        return ""
    
    def _get_level_color(self, level: str) -> str:
        """
        Retorna cor para nível de log.
        Importa cores de LogUtils.
        """
        from ....core.config.LogUtils import LogUtils
        return LogUtils.LEVEL_COLORS.get(level, "#FFFFFF")
    
    def get_entry(self, index: QModelIndex) -> Optional[LogEntry]:
        """Retorna a entrada em um índice (para detalhe)."""
        if not index.isValid() or index.row() >= len(self._entries):
            return None
        return self._entries[index.row()]
    
    def get_entry_at(self, row: int) -> Optional[LogEntry]:
        """Retorna a entrada em uma linha específica (por índice inteiro)."""
        if row < 0 or row >= len(self._entries):
            return None
        return self._entries[row]
    
    def get_all_entries(self) -> List[LogEntry]:
        """Retorna todas as entradas."""
        return self._entries.copy()
