from qgis.PyQt.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QMessageBox, QCheckBox, QTextEdit, QComboBox, QListWidget, QDoubleSpinBox, QGridLayout, QFrame
)
from qgis.PyQt.QtWidgets import QLayout, QWidget
from qgis.PyQt.QtCore import Qt, QPoint
from qgis.PyQt.QtGui import QCursor
from typing import Optional
from ..styles.Styles import Styles
from .ScrollWidget import ScrollWidget

class MainLayout(QVBoxLayout):
    """Container layout customizado para plugins MTL Tools com suporte a resize.
    
    ARQUITETURA:
    ============
    1. RESIZE (Separação de Responsabilidades):
       - BasePlugin recebe eventos de mouse do Qt
       - MainLayout executa lógica de resize (_get_resize_edge, _update_cursor)
       - Limpo e reutilizável em qualquer plugin
    
    2. SCROLL (Encapsulamento Automático):
       - MainLayout cria ScrollWidget INTERNAMENTE se enable_scroll=True
       - Plugin NÃO importa ScrollWidget (encapsulado)
       - Plugin NÃO toca em self.scroll_container (não existe)
       - add_items() decide automaticamente para onde vai cada item:
         * Se scroll habilitado: encaminha para scroll
         * Se scroll desabilitado: encaminha para inner_layout
       - Responsabilidade única: MainLayout gerencia scroll, plugin só adiciona itens
    
    Benefícios:
    - Separação de responsabilidades: BasePlugin recebe, MainLayout executa
    - Encapsulamento: scroll é detalhe interno
    - Reutilizável: MainLayout funciona com ou sem scroll
    - Testável: lógica concentrada em uma classe
    - Simples: BasePlugin tem apenas 3 métodos de delegação
    """
    def __init__(self, parent=None, enable_scroll=False):
        super().__init__(parent)

        # margens externas do dialog (recorte do radius)
        self.setContentsMargins(3, 3, 3, 3)
        self.setSpacing(0)

        # container visual
        self._frame = QFrame(parent)
        self._frame.setObjectName("main_container")
        self._frame.setStyleSheet(Styles.main_application())
        self._frame.setMouseTracking(True)  # Ativa rastreamento no frame

        # layout interno real (sempre criado, com ou sem scroll)
        self._inner_layout = QVBoxLayout(self._frame)
        self._inner_layout.setContentsMargins(5, 5, 5, 5)
        # Espaçamento será definido dinamicamente baseado no scroll

        # scroll widget (criado apenas se enable_scroll=True)
        self._scroll = None
        if enable_scroll:
            self._scroll = ScrollWidget(parent)
            self._inner_layout.addWidget(self._scroll)

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

    def addWidget(self, widget, *args, **kwargs):
        """
        Adiciona widget ao layout.
        
        Se scroll está habilitado, adiciona ao scroll.
        Caso contrário, adiciona ao inner_layout.
        """
        if self._scroll is not None:
            # Cria container para o widget se necessário
            container = QWidget()
            layout = QVBoxLayout(container)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.addWidget(widget)
            self._scroll.add_layout_as_content(layout)
        else:
            self._inner_layout.addWidget(widget, *args, **kwargs)

    def addLayout(self, layout, *args, **kwargs):
        """
        Adiciona layout ao layout.
        
        Se scroll está habilitado, adiciona ao scroll.
        Caso contrário, adiciona ao inner_layout.
        """
        if self._scroll is not None:
            self._scroll.add_layout_as_content(layout)
        else:
            self._inner_layout.addLayout(layout, *args, **kwargs)

    def addStretch(self, *args, **kwargs):
        self._inner_layout.addStretch(*args, **kwargs)

    def addSpacing(self, *args, **kwargs):
        self._inner_layout.addSpacing(*args, **kwargs)
        
    def add_items(self, items):
        """
        Adiciona widgets e/ou layouts ao layout.

        Se scroll está habilitado, coleta todos os itens e os adiciona
        ao scroll como um único layout.
        
        Se scroll está desabilitado, adiciona ao inner_layout diretamente.

        Parameters
        ----------
        items : iterable
            Lista ou tupla contendo QLayout e/ou QWidget
        """
        if not items:
            return

        if self._scroll is not None:
            # Scroll habilitado: coleta itens em um layout e adiciona ao scroll
            container_layout = QVBoxLayout()
            container_layout.setContentsMargins(0, 0, 0, 0)
            container_layout.setSpacing(Styles.LAYOUT_V_SPACING)
            
            for item in items:
                if isinstance(item, QLayout):
                    container_layout.addLayout(item)
                elif isinstance(item, QWidget):
                    container_layout.addWidget(item)
                else:
                    raise TypeError(
                        f"Tipo inválido em MainLayout.add_items: {type(item)}"
                    )
            
            # Adiciona ao scroll
            self._scroll.add_layout_as_content(container_layout)
        else:
            # Scroll desabilitado: adiciona diretamente ao inner_layout
            for item in items:
                if isinstance(item, QLayout):
                    self._inner_layout.addLayout(item)
                elif isinstance(item, QWidget):
                    self._inner_layout.addWidget(item)
                else:
                    raise TypeError(
                        f"Tipo inválido em MainLayout.add_items: {type(item)}"
                    )

    def get_size(self) -> tuple:
        """
        Retorna a dimensão atual do layout container (width, height).
        
        Returns
        -------
        tuple
            (width, height) em pixels
        """
        if self._frame:
            return (self._frame.width(), self._frame.height())
        return (0, 0)

    def set_size(self, width: int, height: int):
        """
        Define a dimensão do layout container.
        
        Parameters
        ----------
        width : int
            Largura em pixels
        height : int
            Altura em pixels
        """
        if self._frame:
            self._frame.setMinimumSize(width, height)
            self._frame.resize(width, height)
    
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
        
        # SEMPRE atualiza o cursor baseado na posição atual
        # Mesmo quando não está em resize, isso garante que o cursor resete corretamente
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
