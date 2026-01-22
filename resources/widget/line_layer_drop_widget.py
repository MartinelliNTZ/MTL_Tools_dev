
from qgis.core import QgsProject, QgsVectorLayer, QgsWkbTypes
from qgis.PyQt.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QMessageBox, QCheckBox, QTextEdit, QComboBox, QListWidget
)
from qgis.PyQt.QtCore import QObject, QEvent, Qt
import pickle

class LineLayerDropWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setDragEnabled(False)
        self.setSelectionMode(self.SingleSelection)

    def dragEnterEvent(self, event):
        if self._is_valid_event(event):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if self._is_valid_event(event):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        if not self._is_valid_event(event):
            event.ignore()
            return

        layer = self._get_layer_from_event(event)
        if not layer:
            event.ignore()
            return

        self.clear()
        self.addItem(layer.name())
        self.setToolTip(layer.id())

        event.acceptProposedAction()

    # -------------------------
    # Validações
    # -------------------------

    def _is_valid_event(self, event):
        if not event.mimeData().hasFormat("application/qgis.layertreemodeldata"):
            return False

        layer = self._get_layer_from_event(event)
        if not layer:
            return False

        if not isinstance(layer, QgsVectorLayer):
            return False

        if layer.geometryType() != QgsWkbTypes.LineGeometry:
            return False

        return True

    def _get_layer_from_event(self, event):
        try:
            data = event.mimeData().data("application/qgis.layertreemodeldata")
            layer_ids = pickle.loads(bytes(data))
            if not layer_ids:
                return None

            return QgsProject.instance().mapLayer(layer_ids[0])
        except Exception:
            return None

    # -------------------------
    # API pública
    # -------------------------

    def get_layer(self):
        layer_id = self.toolTip()
        return QgsProject.instance().mapLayer(layer_id) if layer_id else None

