# -*- coding: utf-8 -*-

from qgis.PyQt.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox
from qgis.gui import QgsMapLayerComboBox
from qgis.core import QgsVectorLayer, QgsMapLayerProxyModel


class LayerInputWidget(QWidget):

    def __init__(
        self,
        label_text: str,
        filters,
        *,
        allow_empty: bool = True,
        enable_selected_checkbox: bool = True,
        parent=None
    ):
        super().__init__(parent)

        self._state_layer = None

        self._label = QLabel(label_text)
        self._combo = QgsMapLayerComboBox()
        self._combo.setAllowEmptyLayer(allow_empty)

        self._combo.setFilters(self._normalize_filters(filters))

        self._chk_selected = None
        if enable_selected_checkbox:
            self._chk_selected = QCheckBox("Somente feições selecionadas")
            self._chk_selected.setEnabled(False)

        self._build_layout()
        self._bind_events()

    # --------------------------------------------------
    # UI
    # --------------------------------------------------
    def _build_layout(self):
        layout = QVBoxLayout(self)
        layout.addWidget(self._label)
        layout.addWidget(self._combo)

        if self._chk_selected:
            layout.addWidget(self._chk_selected)

    # --------------------------------------------------
    # Bindings
    # --------------------------------------------------
    def _bind_events(self):
        self._combo.layerChanged.connect(self._on_layer_changed)
        self._on_layer_changed()

    def _on_layer_changed(self, *args):
        self._disconnect_old_layer()

        layer = self._combo.currentLayer()
        self._state_layer = layer

        if isinstance(layer, QgsVectorLayer):
            layer.selectionChanged.connect(self._update_selection_state)

        self._update_selection_state()

    def _update_selection_state(self):
        if not self._chk_selected:
            return

        layer = self._state_layer

        if not isinstance(layer, QgsVectorLayer):
            self._chk_selected.setChecked(False)
            self._chk_selected.setEnabled(False)
            return

        count = layer.selectedFeatureCount()
        self._chk_selected.setEnabled(count > 0)

        if count == 0:
            self._chk_selected.setChecked(False)

    def _disconnect_old_layer(self):
        old = self._state_layer
        if isinstance(old, QgsVectorLayer):
            try:
                old.selectionChanged.disconnect(self._update_selection_state)
            except Exception:
                pass

    # --------------------------------------------------
    # API pública
    # --------------------------------------------------
    def current_layer(self):
        return self._combo.currentLayer()

    def only_selected_enabled(self) -> bool:
        return bool(self._chk_selected and self._chk_selected.isChecked())

    def set_layer(self, layer):
        self._combo.setLayer(layer)

    # --------------------------------------------------
    # Utils
    # --------------------------------------------------
    @staticmethod
    def _normalize_filters(filters):
        if isinstance(filters, (list, tuple, set)):
            final = 0
            for f in filters:
                final |= f
            return final
        return filters
