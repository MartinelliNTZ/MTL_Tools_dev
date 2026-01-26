# -*- coding: utf-8 -*-

import os
from qgis.PyQt.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidgetItem
)
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QIcon
from qgis.core import QgsVectorLayer, QgsWkbTypes, QgsMapLayerProxyModel
from qgis.gui import QgsMapLayerComboBox

from ..utils.tool_keys import ToolKey
from ..core.config.LogUtils import LogUtils
from ..utils.qgis_messagem_util import QgisMessageUtil
from ..core.ui.WidgetFactory import WidgetFactory
from ..utils.preferences import load_tool_prefs, save_tool_prefs
from ..utils.vector.VectorLayerAttributes import VectorLayerAttributes
from .base_plugin import BasePluginMTL


class CopyAttributes(BasePluginMTL):
    TOOL_KEY = ToolKey.COPY_ATTRIBUTES

    def __init__(self, iface):
        super().__init__(iface.mainWindow())
        self.iface = iface

        self._build_ui()
        self._load_prefs()

    # =========================
    # UI
    # =========================
    def _build_ui(self):
        super()._build_ui("Copiar Atributos de Vetor","copy_attributes.ico","copy_attributes_help.md")       
              
        LogUtils.log("Construindo interface da ferramenta", level="INFO", tool=self.TOOL_KEY, class_name="CopyAttributtes")


        # CAMADA DESTINO
        tgt_layout, self.target_layer_input = WidgetFactory.create_layer_input(
            label_text="Camada de Destino:",
            filters=[QgsMapLayerProxyModel.VectorLayer],
            parent=self
        )
        LogUtils.log("Componente de camada de target adicionado", level="DEBUG", tool=self.TOOL_KEY, class_name="CopyAttributtes")        
        # CAMADA ORIGEM
        src_layout, self.source_layer_input = WidgetFactory.create_layer_input(
            label_text="Camada de Origem:",
            filters=[QgsMapLayerProxyModel.VectorLayer],
            parent=self
        )        
        self.source_layer_input.layerChanged.connect(self._populate_fields)

        LogUtils.log("Componente de camada de origem adicionado", level="DEBUG", tool=self.TOOL_KEY, class_name="CopyAttributtes")    



        # ATRIBUTOS
        attr_layout, self.attr_widget = WidgetFactory.create_attribute_selector(
            parent=self,
            title="Atributos da camada origem"       )


        # BOTÕES
        buttons_layout, self.action_buttons = WidgetFactory.create_bottom_action_buttons(
            parent=self,            run_callback=self.on_run,        
            close_callback=self.close, 
            info_callback=self.show_info_dialog,            tool_key=self.TOOL_KEY,        ) 
        

        # SIGNALS
        #self.cmb_source.layerChanged.connect(self._populate_fields)

        # AUTO SETUP
        self.layout.add_items([tgt_layout,src_layout,attr_layout, buttons_layout])        
        self._populate_fields()


    def _populate_fields(self):
        layer = self.source_layer_input.current_layer()
        if not isinstance(layer, QgsVectorLayer):
            self.attr_widget.set_fields([])
            return

        self.attr_widget.set_fields(
            [f.name() for f in layer.fields()]
        )

            
    def _load_prefs(self):
        prefs = load_tool_prefs(self.TOOL_KEY)
        self.attr_widget.set_checked_all(prefs.get("chk_all", False))
        

    def _save_prefs(self):       
        data = {}
        data['chk_all'] = bool(self.attr_widget.use_all_fields())
        save_tool_prefs(self.TOOL_KEY, data)
    # =========================
    # CONTROLLER
    # =========================
    def on_run(self):
        self._save_prefs()
        LogUtils.log(
            "Execução iniciada",
            level="INFO",
            tool=self.TOOL_KEY,
            class_name="CopyAttributes"
        )

        source = self.source_layer_input.current_layer()
        target = self.target_layer_input.current_layer()

        if not isinstance(source, QgsVectorLayer):
            QgisMessageUtil.bar_warning(self.iface, "Camada de origem inválida")
            LogUtils.log("Camada de origem inválida", level="WARNING", tool=self.TOOL_KEY, class_name="CopyAttributes")
            return

        if not isinstance(target, QgsVectorLayer):
            QgisMessageUtil.bar_warning(self.iface, "Camada de destino inválida")
            LogUtils.log("Camada de destino inválida", level="WARNING", tool=self.TOOL_KEY, class_name="CopyAttributes")
            return

        if not self.ensure_editable(target):
            LogUtils.log("Camada de destino não editável", level="WARNING", tool=self.TOOL_KEY, class_name="CopyAttributes")
            return

        fields = None
        if not self.attr_widget.use_all_fields():
            fields = self.attr_widget.get_selected_fields()

            if not fields:
                QgisMessageUtil.bar_warning(self.iface, "Nenhum atributo selecionado")
                LogUtils.log("Execução abortada: nenhum atributo selecionado", level="WARNING", tool=self.TOOL_KEY, class_name="CopyAttributes")
                return



        def conflict_resolver(field_name):
            return QgisMessageUtil.ask_field_conflict(
                self.iface,
                field_name
            )

        ok = VectorLayerAttributes.copy_attributes(
            target_layer=target,
            source_layer=source,
            field_names=fields,
            conflict_resolver=conflict_resolver
        )

        if ok:
            QgisMessageUtil.bar_success(self.iface, "Atributos copiados com sucesso (alterações não salvas)")
            LogUtils.log("Cópia de atributos finalizada com sucesso", level="INFO", tool=self.TOOL_KEY, class_name="CopyAttributes")
        else:
            LogUtils.log("Falha na cópia de atributos", level="ERROR", tool=self.TOOL_KEY, class_name="CopyAttributes")

def run_copy_attributes(iface):
    dlg = CopyAttributes(iface)
    dlg.setModal(False)
    dlg.show()
    return dlg
