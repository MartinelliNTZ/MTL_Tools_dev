# -*- coding: utf-8 -*-

import os
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QIcon
from qgis.core import QgsVectorLayer, QgsWkbTypes, QgsMapLayerProxyModel

from ..utils.ToolKeys import ToolKey
from ..core.config.LogUtilsNew import LogUtilsNew
from ..utils.QgisMessageUtil import QgisMessageUtil
from ..core.ui.WidgetFactory import WidgetFactory
from ..utils.preferences import load_tool_prefs, save_tool_prefs
from ..utils.vector.VectorLayerAttributes import VectorLayerAttributes
from .BasePlugin import BasePluginMTL


class CopyAttributes(BasePluginMTL):
    TOOL_KEY = ToolKey.COPY_ATTRIBUTES

    def __init__(self, iface):
        super().__init__(iface.mainWindow())
        self.iface = iface
        self.init(ToolKey.COPY_ATTRIBUTES, "CopyAttributes", min_width=320, min_height=450)

    # =========================
    # UI
    # =========================
    def _build_ui(self, **kwargs):
        super()._build_ui("Copiar Atributos de Vetor","copy_attributes.ico","copy_attributes_help.md", **kwargs)       
              
        self.logger.info("Construindo interface da ferramenta")


        # CAMADA DESTINO
        tgt_layout, self.target_layer_input = WidgetFactory.create_layer_input(
            label_text="Camada de Destino:",
            filters=[QgsMapLayerProxyModel.VectorLayer],
            parent=self
        )
        self.logger.debug("Componente de camada de target adicionado")        
        # CAMADA ORIGEM
        src_layout, self.source_layer_input = WidgetFactory.create_layer_input(
            label_text="Camada de Origem:",
            filters=[QgsMapLayerProxyModel.VectorLayer],
            parent=self
        )        
        self.source_layer_input.layerChanged.connect(self._populate_fields)

        self.logger.debug("Componente de camada de origem adicionado")    



        # ATRIBUTOS
        attr_layout, self.attr_widget = WidgetFactory.create_attribute_selector(
            parent=self,
            title="Atributos da camada origem"       )


        # BOTÕES
        buttons_layout, self.action_buttons = WidgetFactory.create_bottom_action_buttons(
            parent=self,            run_callback=self.execute_tool,
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
    def execute_tool(self):
        self._save_prefs()
        self.logger.info("Execução iniciada")

        source = self.source_layer_input.current_layer()
        target = self.target_layer_input.current_layer()

        if not isinstance(source, QgsVectorLayer):
            QgisMessageUtil.bar_warning(self.iface, "Camada de origem inválida")
            self.logger.warning("Camada de origem inválida")
            return

        if not isinstance(target, QgsVectorLayer):
            QgisMessageUtil.bar_warning(self.iface, "Camada de destino inválida")
            self.logger.warning("Camada de destino inválida")
            return

        if not self.ensure_editable(target):
            self.logger.warning("Camada de destino não editável")
            return

        fields = None
        if not self.attr_widget.use_all_fields():
            fields = self.attr_widget.get_selected_fields()

            if not fields:
                QgisMessageUtil.bar_warning(self.iface, "Nenhum atributo selecionado")
                self.logger.warning("Execução abortada: nenhum atributo selecionado")
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
            self.logger.info("Cópia de atributos finalizada com sucesso")
        else:
            self.logger.error("Falha na cópia de atributos")

def run_copy_attributes(iface):
    dlg = CopyAttributes(iface)
    dlg.setModal(False)
    dlg.show()
    return dlg
