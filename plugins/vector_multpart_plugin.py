# tools/vector_multipart_tool.py
# -*- coding: utf-8 -*-

import os
from qgis.PyQt.QtWidgets import QAction
from qgis.core import QgsVectorLayer, QgsWkbTypes, QgsFeedback

from ..utils.vector_utils import VectorUtils
from ..utils.qgis_messagem_util import QgisMessageUtil
from .base_plugin import BasePluginMTL

class VectorMultipartPlugin(BasePluginMTL):

    def __init__(self, iface):
        self.iface = iface
        self.actions = []

    def initGui(self):
        self.create_action(
            "../icons/multipart.png",
            "Converter para Multipart",
            self.run_multpart
        )


    def unload(self):
        for a in self.actions:
            self.iface.removePluginMenu("MTL Tools", a)

    # --------------------------------------------------
    # CONTROLLER
    # --------------------------------------------------
    def run_multpart(self):
        layer = self.iface.activeLayer()

        if not layer or not isinstance(layer, QgsVectorLayer):
            QgisMessageUtil.bar_critical(
                self.iface,
                "Selecione uma camada vetorial"
            )
            return

        layer = self.get_active_vector_layer()
        if not layer or not self.ensure_has_features(layer):
            return


        already_editing = layer.isEditable()

        # 🔔 Confirmação
        if layer.selectedFeatureCount() > 0:
            msg = "Converter apenas as feições SELECIONADAS para multipart?"
        else:
            msg = "Converter TODAS as feições para multipart?"

        if not QgisMessageUtil.confirm(self.iface, msg):
            return

        # 🔓 Inicia edição se não estiver em edição
        if not already_editing:
            layer.startEditing()

        feedback = QgsFeedback()
        
        only_selected = layer.selectedFeatureCount() > 0
        ok = VectorUtils.singleparts_to_multparts(
            layer,
            feedback,
            only_selected=only_selected
        )


        if not ok:
            layer.rollBack()
            QgisMessageUtil.bar_warning(
                self.iface,
                "Operação cancelada pelo usuário"
            )
            return

        # 🔒 Se já estava em edição → NÃO salva
        if already_editing:
            QgisMessageUtil.bar_success(
                self.iface,
                "Geometrias convertidas para multipart (não salvas)"
            )
            return
