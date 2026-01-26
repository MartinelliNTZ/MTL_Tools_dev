from qgis.PyQt.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QMessageBox, QCheckBox, QTextEdit, QComboBox, QListWidget, QDoubleSpinBox, QGridLayout, QFrame
)

class MainLayout(QVBoxLayout):
    def __init__(self, parent=None):
        super().__init__(parent)