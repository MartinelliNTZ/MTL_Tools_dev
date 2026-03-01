from qgis.PyQt.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QMessageBox, QCheckBox, QTextEdit, QComboBox, QListWidget, QDoubleSpinBox, QGridLayout, QFrame
)
from qgis.PyQt.QtWidgets import QLayout, QWidget
from qgis.PyQt.QtCore import Qt, QPoint
from qgis.PyQt.QtGui import QCursor
from typing import Optional
from ..styles.Styles import Styles

class MainLayout(QVBoxLayout):
    def __init__(self, parent=None):
        super().__init__(parent)

        # margens externas do dialog (recorte do radius)
        self.setContentsMargins(3, 3, 3, 3)
        self.setSpacing(0)

        # container visual
        self._frame = QFrame(parent)
        self._frame.setObjectName("main_container")
        self._frame.setStyleSheet(Styles.main_application())
        self._frame.setMouseTracking(True)  # Ativa rastreamento no frame

        # layout interno real
        self._inner_layout = QVBoxLayout(self._frame)
        self._inner_layout.setContentsMargins(5, 5, 5, 5)
        self._inner_layout.setSpacing(8)

        # adiciona o frame ao layout principal
        super().addWidget(self._frame)
        
        # Resize handler attributes
        self._resize_border = 10  # pixels
        self._resize_active = False
        self._resize_edge = None
        self._last_pos = None
        self._parent_dialog = parent
        
        # Ativa rastreamento de mouse para atualizar cursor continuamente
        if parent:
            parent.setMouseTracking(True)

    # -------- proxy methods --------
    def addWidget(self, widget, *args, **kwargs):
        self._inner_layout.addWidget(widget, *args, **kwargs)

    def addLayout(self, layout, *args, **kwargs):
        self._inner_layout.addLayout(layout, *args, **kwargs)

    def addStretch(self, *args, **kwargs):
        self._inner_layout.addStretch(*args, **kwargs)

    def addSpacing(self, *args, **kwargs):
        self._inner_layout.addSpacing(*args, **kwargs)
        
    def add_items(self, items):
        """
        Adiciona widgets e/ou layouts ao layout interno,
        respeitando a ordem da lista.

        Parameters
        ----------
        items : iterable
            Lista ou tupla contendo QLayout e/ou QWidget
        """
        if not items:
            return

        for item in items:
            if isinstance(item, QLayout):
                self._inner_layout.addLayout(item)
            elif isinstance(item, QWidget):
                self._inner_layout.addWidget(item)
            else:
                raise TypeError(
                    f"Tipo inválido em MainLayout.add_items: {type(item)}"
                )
    
    def _get_resize_edge(self, pos: QPoint) -> Optional[str]:
        """Detecta qual borda está sendo apontada."""
        if not self._parent_dialog:
            return None
        
        rect = self._parent_dialog.rect()
        if pos.x() < self._resize_border and pos.y() < self._resize_border:
            return "top-left"
        elif pos.x() > rect.width() - self._resize_border and pos.y() < self._resize_border:
            return "top-right"
        elif pos.x() < self._resize_border and pos.y() > rect.height() - self._resize_border:
            return "bottom-left"
        elif pos.x() > rect.width() - self._resize_border and pos.y() > rect.height() - self._resize_border:
            return "bottom-right"
        elif pos.x() < self._resize_border:
            return "left"
        elif pos.x() > rect.width() - self._resize_border:
            return "right"
        elif pos.y() < self._resize_border:
            return "top"
        elif pos.y() > rect.height() - self._resize_border:
            return "bottom"
        return None

    def _update_cursor(self, edge: Optional[str]):
        """Atualiza cursor baseado na borda detectada."""
        cursors = {
            "top": Qt.SizeVerCursor,
            "bottom": Qt.SizeVerCursor,
            "left": Qt.SizeHorCursor,
            "right": Qt.SizeHorCursor,
            "top-left": Qt.SizeFDiagCursor,
            "top-right": Qt.SizeBDiagCursor,
            "bottom-left": Qt.SizeBDiagCursor,
            "bottom-right": Qt.SizeFDiagCursor,
        }
        if self._parent_dialog:
            self._parent_dialog.setCursor(QCursor(cursors.get(edge, Qt.ArrowCursor)))

    def handle_mouse_press(self, event):
        """Inicia resize ao clicar nas bordas."""
        if event.button() == Qt.LeftButton:
            edge = self._get_resize_edge(event.pos())
            if edge:
                self._resize_active = True
                self._resize_edge = edge
                self._last_pos = event.globalPos()
                event.accept()
                return True
        return False

    def handle_mouse_move(self, event):
        """Redimensiona a janela ao arrastar."""
        edge = self._get_resize_edge(event.pos())
        self._update_cursor(edge)
        
        if self._resize_active and self._resize_edge and self._last_pos and self._parent_dialog:
            delta = event.globalPos() - self._last_pos
            new_rect = self._parent_dialog.geometry()
            
            if "top" in self._resize_edge:
                new_rect.setTop(new_rect.top() + delta.y())
            if "bottom" in self._resize_edge:
                new_rect.setBottom(new_rect.bottom() + delta.y())
            if "left" in self._resize_edge:
                new_rect.setLeft(new_rect.left() + delta.x())
            if "right" in self._resize_edge:
                new_rect.setRight(new_rect.right() + delta.x())
            
            # Respeita tamanho mínimo
            if new_rect.width() >= self._parent_dialog.minimumWidth() and new_rect.height() >= self._parent_dialog.minimumHeight():
                self._parent_dialog.setGeometry(new_rect)
                self._last_pos = event.globalPos()

    def handle_mouse_release(self, event):
        """Finaliza resize ao soltar o mouse."""
        if event.button() == Qt.LeftButton and self._resize_active:
            self._resize_active = False
            self._resize_edge = None
            self._last_pos = None
            self._update_cursor(None)
            event.accept()
            return True
        return False
