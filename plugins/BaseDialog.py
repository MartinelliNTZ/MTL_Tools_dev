from qgis.PyQt.QtWidgets import (
    QDialog, QAction,QFileDialog, QLineEdit,QSizeGrip
)

class BaseDialog(QDialog):
    
    """Base para diálogos, com métodos comuns e integração com iface e logger."""
    layout = None
    
    
    
    
    def mousePressEvent(self, event):
        """Delega evento de mouse para detecção de bordas e início de resize do MainLayout."""
        if self.layout and hasattr(self.layout, 'handle_mouse_press'):
            if self.layout.handle_mouse_press(event):
                return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """Delega evento de mouse para atualização de cursor e resize do MainLayout.        """
        if self.layout and hasattr(self.layout, 'handle_mouse_move'):
            self.layout.handle_mouse_move(event)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """Delega evento de mouse para finalização de resize do MainLayout."""
        if self.layout and hasattr(self.layout, 'handle_mouse_release'):
            if self.layout.handle_mouse_release(event):
                return
        super().mouseReleaseEvent(event)
