# resources/widgets/AppBarWidget.py
from qgis.PyQt.QtWidgets import QFrame, QLabel, QPushButton, QHBoxLayout
from qgis.PyQt.QtCore import Qt, pyqtSignal, QPoint


class AppBarWidget(QFrame):
    runClicked = pyqtSignal()
    infoClicked = pyqtSignal()
    closeClicked = pyqtSignal()

    def __init__(
        self,
        *,
        title: str,
        show_run: bool = False,
        show_info: bool = False,
        show_close: bool = True,
        parent=None
    ):
        super().__init__(parent)
        self.setObjectName("app_bar")

        self._drag_pos: QPoint = None

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 0, 12, 0)
        layout.setSpacing(8)

        self.lbl_title = QLabel(title)
        self.lbl_title.setObjectName("app_bar_title")
        self.lbl_title.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        layout.addWidget(self.lbl_title)
        layout.addStretch()

        if show_run:
            self.btn_run = QPushButton("Executar")
            self.btn_run.setObjectName("app_bar_btn_run")
            self.btn_run.clicked.connect(self.runClicked.emit)
            layout.addWidget(self.btn_run)

        if show_info:
            self.btn_info = QPushButton("Info")
            self.btn_info.setObjectName("app_bar_btn_info")
            self.btn_info.clicked.connect(self.infoClicked.emit)
            layout.addWidget(self.btn_info)

        if show_close:
            self.btn_close = QPushButton("✕")
            self.btn_close.setObjectName("app_bar_btn_close")

            # 🔑 comportamento padrão
            self.btn_close.clicked.connect(self._on_close_clicked)

            layout.addWidget(self.btn_close)

    # =====================================================
    # FECHAR JANELA
    # =====================================================

    def _on_close_clicked(self):
        self.closeClicked.emit()
        self.window().close()

    # =====================================================
    # DRAG DA JANELA (QT 5)
    # =====================================================

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPos() - self.window().frameGeometry().topLeft()
            event.accept()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._drag_pos and event.buttons() & Qt.LeftButton:
            self.window().move(event.globalPos() - self._drag_pos)
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self._drag_pos = None
        super().mouseReleaseEvent(event)
