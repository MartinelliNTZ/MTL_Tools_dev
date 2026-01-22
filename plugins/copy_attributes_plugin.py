# -*- coding: utf-8 -*-

import os
from qgis.PyQt.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidgetItem
)
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QIcon
from qgis.core import QgsVectorLayer, QgsWkbTypes, QgsMapLayerProxyModel
from qgis.gui import QgsMapLayerComboBox

from ..utils.vector_utils import VectorUtils
from ..utils.tool_keys import ToolKey
from ..utils.log_utils import LogUtilsOld
from ..utils.qgis_messagem_util import QgisMessageUtil
from ..utils.ui_widget_utils import UiWidgetUtils
from ..utils.preferences import load_tool_prefs, save_tool_prefs
from .base_plugin import BasePluginMTL


class CopyAttributes(BasePluginMTL):
    TOOL_KEY = ToolKey.COPY_ATTRIBUTES

    def __init__(self, iface):
        super().__init__(iface.mainWindow())
        self.iface = iface
        icon_path = os.path.join(os.path.dirname(__file__), "..", "resources","icons", "copy_attributes.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        self.PLUGIN_NAME = "Copiar Atributos"
        self._build_ui()
        self._load_prefs()

    # =========================
    # UI
    # =========================
    def _build_ui(self):
        super()._build_ui()       
        layout = QVBoxLayout(self)
        
        self.instructions_file = os.path.join(
            os.path.dirname(__file__),
            "..","resources", "instructions",
            "copy_attributes_help.md"
        )

        # CAMADA DESTINO
        tgt_layout, self.cmb_target, _ = UiWidgetUtils.create_layer_input(
            "Camada destino:",
            QgsMapLayerProxyModel.VectorLayer, enable_selected_checkbox=False
        )
        layout.addLayout(tgt_layout)

        # CAMADA ORIGEM
        src_layout, self.cmb_source, _ = UiWidgetUtils.create_layer_input(
            "Camada origem:",
            QgsMapLayerProxyModel.VectorLayer, enable_selected_checkbox=False
        )
        layout.addLayout(src_layout)

        # ATRIBUTOS
        (
            attr_layout,
            self.chk_all,
            self.lst_fields,
            _,
            _, _
        ) = UiWidgetUtils.create_attribute_selector(
            title="Atributos da camada origem"
        )

        layout.addLayout(attr_layout)

        # BOTÕES
        layout.addLayout(
            UiWidgetUtils.create_run_close_buttons(
                self._run,
                self.close,
                info_callback=lambda: self.show_info_dialog(
            "📘 Instruções – Copiar Atributos"
        )
            )
        )

        # SIGNALS
        self.cmb_source.layerChanged.connect(self._populate_fields)

        # AUTO SETUP
        self._auto_select_layers()
        self._populate_fields()

    # =========================
    # UI HELPERS
    # =========================
    def _auto_select_layers(self):
        layer = self.iface.activeLayer()
        if isinstance(layer, QgsVectorLayer):
            self.cmb_target.setLayer(layer)

    def _populate_fields(self):
        self.lst_fields.clear()

        layer = self.cmb_source.currentLayer()
        if not isinstance(layer, QgsVectorLayer):
            return

        for field in layer.fields():
            item = QListWidgetItem(field.name())
            item.setCheckState(Qt.Checked)
            self.lst_fields.addItem(item)
            
    def _load_prefs(self):
        prefs = load_tool_prefs(self.TOOL_KEY)
        self.chk_all.setChecked(prefs.get("chk_all", False))
        

    def _save_prefs(self):       
        data = {}
        data['chk_all'] = bool(self.chk_all.isChecked())
        save_tool_prefs(self.TOOL_KEY, data)
    # =========================
    # CONTROLLER
    # =========================
    def _run(self):
        target = self.cmb_target.currentLayer()
        source = self.cmb_source.currentLayer()

        if not isinstance(target, QgsVectorLayer):
            return

        if not isinstance(source, QgsVectorLayer):
            return

        if not self.ensure_editable(target):
            return

        fields = None
        if not self.chk_all.isChecked():
            fields = [
                self.lst_fields.item(i).text()
                for i in range(self.lst_fields.count())
                if self.lst_fields.item(i).checkState() == Qt.Checked
            ]

        LogUtilsOld.log(self.TOOL_KEY, "Iniciando cópia de atributos")

        def conflict_resolver(field_name):
            return QgisMessageUtil.ask_field_conflict(
                self.iface, field_name
            )

        ok = VectorUtils.copy_attributes(
            target_layer=target,
            source_layer=source,
            field_names=fields,
            conflict_resolver=conflict_resolver
        )

        if ok:
            QgisMessageUtil.bar_success(
                self.iface,
                "Atributos copiados (alterações não salvas)"
            )
        self._save_prefs()

def run_copy_attributes(iface):
    dlg = CopyAttributes(iface)
    dlg.setModal(False)
    dlg.show()
    return dlg
