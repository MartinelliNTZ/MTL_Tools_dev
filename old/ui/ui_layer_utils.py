# utils/ui/ui_layer_utils.py
# -*- coding: utf-8 -*-

from qgis.core import QgsProject, QgsVectorLayer
from qgis.PyQt.QtWidgets import QComboBox
from qgis.PyQt.QtCore import QObject, QEvent


class _LayerComboEventFilter(QObject):
    def __init__(self, combo: QComboBox, iface):
        super().__init__(combo)
        self.combo = combo
        self.iface = iface

    def eventFilter(self, obj, event):
        # Atualiza lista ao clicar
        if event.type() == QEvent.MouseButtonPress:
            UiLayerUtils.populate_vector_layers(self.combo)

        # Drag enter
        if event.type() == QEvent.DragEnter:
            event.acceptProposedAction()
            return True

        # Drop
        if event.type() == QEvent.Drop:
            layer = self.iface.activeLayer()
            if isinstance(layer, QgsVectorLayer):
                idx = self.combo.findData(layer.id())
                if idx != -1:
                    self.combo.setCurrentIndex(idx)
            event.acceptProposedAction()
            return True

        return False


class UiLayerUtils:
    """
    Utilitários de UI para seleção de camadas vetoriais
    Compatível QGIS 3.16 → 3.40
    """

    @staticmethod
    def populate_vector_layers(combo: QComboBox, keep_current=True):
        current = combo.currentData() if keep_current else None

        combo.blockSignals(True)
        combo.clear()

        for lyr in QgsProject.instance().mapLayers().values():
            if isinstance(lyr, QgsVectorLayer):
                combo.addItem(lyr.name(), lyr.id())

        if current:
            idx = combo.findData(current)
            if idx != -1:
                combo.setCurrentIndex(idx)

        combo.blockSignals(False)

    @staticmethod
    def set_active_layer(combo: QComboBox, iface):
        layer = iface.activeLayer()
        if isinstance(layer, QgsVectorLayer):
            idx = combo.findData(layer.id())
            if idx != -1:
                combo.setCurrentIndex(idx)

    @staticmethod
    def enable_layer_drag_drop(combo: QComboBox, iface):
        combo.setAcceptDrops(True)

        # instala filtro de eventos (forma correta)
        filter_obj = _LayerComboEventFilter(combo, iface)
        combo.installEventFilter(filter_obj)

        # guarda referência (EVITA GC → crash aleatório)
        combo._layer_event_filter = filter_obj
