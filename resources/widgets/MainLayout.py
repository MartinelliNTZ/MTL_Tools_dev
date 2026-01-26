from qgis.PyQt.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QMessageBox, QCheckBox, QTextEdit, QComboBox, QListWidget, QDoubleSpinBox, QGridLayout, QFrame
)
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

        # layout interno real
        self._inner_layout = QVBoxLayout(self._frame)
        self._inner_layout.setContentsMargins(5, 5, 5, 5)
        self._inner_layout.setSpacing(8)

        # adiciona o frame ao layout principal
        super().addWidget(self._frame)

    # -------- proxy methods --------
    def addWidget(self, widget, *args, **kwargs):
        self._inner_layout.addWidget(widget, *args, **kwargs)

    def addLayout(self, layout, *args, **kwargs):
        self._inner_layout.addLayout(layout, *args, **kwargs)

    def addStretch(self, *args, **kwargs):
        self._inner_layout.addStretch(*args, **kwargs)

    def addSpacing(self, *args, **kwargs):
        self._inner_layout.addSpacing(*args, **kwargs)
