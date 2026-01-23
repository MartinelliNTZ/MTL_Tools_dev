"""
Proxy model para tabela de logs com suporte a sort.

Permite ordenar por qualquer coluna em ordem crescente/decrescente.
"""
from qgis.PyQt.QtCore import Qt, QSortFilterProxyModel, QDateTime


class LogSortFilterProxyModel(QSortFilterProxyModel):
    """
    Proxy model que adiciona suporte a sort e filter à tabela de logs.
    """
    
    def __init__(self, parent=None):
        """Inicializa o proxy model."""
        super().__init__(parent)
        # Configurar sort
        self.setSortCaseSensitivity(Qt.CaseInsensitive)
        self.setFilterCaseSensitivity(Qt.CaseInsensitive)
        # Suportar sort por múltiplas colunas
        self.setRecursiveFilteringEnabled(True)
    
    def lessThan(self, source_left, source_right):
        """
        Implementa comparação customizada para sort.
        
        Trata tipos especiais como timestamp e nível.
        """
        col = source_left.column()
        col_name = self.sourceModel().COLUMNS[col][1]
        
        # Tentar obter entries diretamente do modelo
        entry_left = None
        entry_right = None
        
        try:
            if hasattr(self.sourceModel(), '_entries'):
                if 0 <= source_left.row() < len(self.sourceModel()._entries):
                    entry_left = self.sourceModel()._entries[source_left.row()]
                if 0 <= source_right.row() < len(self.sourceModel()._entries):
                    entry_right = self.sourceModel()._entries[source_right.row()]
        except:
            pass
        
        # Se conseguiu ambas as entries, usar lógica customizada
        if entry_left and entry_right:
            # Sort por timestamp (ISO format é ordenável como string)
            if col_name == "ts":
                return (entry_left.ts or "") < (entry_right.ts or "")
            
            # Sort por level (usando ordem lógica)
            if col_name == "level":
                level_order = {"DEBUG": 0, "INFO": 1, "WARNING": 2, "ERROR": 3, "CRITICAL": 4}
                left_val = level_order.get(entry_left.level, 99)
                right_val = level_order.get(entry_right.level, 99)
                return left_val < right_val
        
        # Sort padrão para outros campos
        return super().lessThan(source_left, source_right)
