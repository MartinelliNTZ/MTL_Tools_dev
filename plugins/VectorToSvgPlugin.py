# -*- coding: utf-8 -*-
import os
import re

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import QgsLayoutExporter, QgsProject
from qgis.PyQt.QtGui import QColor
from qgis.core import QgsMapLayerProxyModel

from .BasePlugin import BasePluginMTL
from ..core.ui.WidgetFactory import WidgetFactory
from ..utils.Preferences import load_tool_prefs, save_tool_prefs
from ..utils.ToolKeys import ToolKey
from ..i18n.TranslationManager import STR


class VectorToSvgPlugin(BasePluginMTL):
    TOOL_KEY = ToolKey.VECTOR_TO_SVG

    def __init__(self, iface):
        super().__init__(iface.mainWindow())
        self.iface = iface
        self.init(
            tool_key=self.TOOL_KEY,
            class_name=self.__class__.__name__,
            load_settings_prefs=False,
            build_ui=True,
        )

    def _build_ui(self, **kwargs):
        super()._build_ui(
            title="Conversor de Vetor para SVG",
            icon_path="cadmus_icon.ico",
            enable_scroll=False,
        )

        layer_layout, self.layer_input = WidgetFactory.create_layer_input(
            "Camada Vetorial",
            QgsMapLayerProxyModel.VectorLayer,
            allow_empty=False,
            enable_selected_checkbox=True,
            parent=self,
            separator_top=False,
            separator_bottom=True,
        )

        fill_layout, self.fill_color_widget = WidgetFactory.create_color_button(
            title="Cor Fundo",
            initial_color=QColor("#ffffff"),
            tooltip="Selecione a cor de preenchimento",
            parent=self,
            separator_top=False,
            separator_bottom=False,
        )

        border_layout, self.border_color_widget = WidgetFactory.create_color_button(
            title="Cor Borda",
            initial_color=QColor("#000000"),
            tooltip="Selecione a cor da borda",
            parent=self,
            separator_top=False,
            separator_bottom=False,
        )

        label_layout, self.label_color_widget = WidgetFactory.create_color_button(
            title="Cor Rotulo",
            initial_color=QColor("#000000"),
            tooltip="Selecione a cor do rotulo",
            parent=self,
            separator_top=False,
            separator_bottom=True,
        )

        options = {
            "transparent_background": "Fundo transparente",
            "show_border": "Mostrar Borda",
            "show_label": "Mostrar Rotulo",
            "for_each_feature": "Gerar SVG para cada feição",
        }
        options_layout, self.options_map = WidgetFactory.create_checkbox_grid(
            options,
            items_per_row=1,
            checked_by_default=False,
            title=None,
            separator_top=False,
            separator_bottom=True,
        )
                # ====== BOTOES ======
        buttons_layout, self.action_buttons = (
            WidgetFactory.create_bottom_action_buttons(
                parent=self,
                run_callback=self.execute_tool,
                close_callback=self.close,
                info_callback=self.show_info_dialog,
                tool_key=self.TOOL_KEY,
            )
        )
        folder_layout, self.folder_selector = WidgetFactory.create_path_selector(
            parent=self,
            title=STR.OUTPUT_FOLDER,
            mode="folder",
            separator_top=False,
            separator_bottom=False,
        )
        self.logger.debug("Path Selector de pasta de saída criado")

        btn_project_layout, self.btn_project = WidgetFactory.create_simple_button(
            text=STR.USE_PROJECT_FOLDER,
            parent=self,
        )
        self.btn_project.clicked.connect(self._set_folder_to_project)
        self.logger.debug("Botão 'Usar pasta do projeto' criado")

        self.layout.add_items(
            [
                layer_layout,
                fill_layout,
                border_layout,
                label_layout,
                options_layout,
                folder_layout,
                btn_project_layout,
                buttons_layout,
            ]
        )

    def _load_prefs(self):
        self.logger.debug("Carregando preferencias do VectorToSvg")
        self.preferences = load_tool_prefs(self.TOOL_KEY)

        layer_id = self.preferences.get("layer_id", "")
        if layer_id:
            layer = QgsProject.instance().mapLayer(layer_id)
            if layer is not None:
                self.layer_input.set_layer(layer)

        self.fill_color_widget.set_color(
            QColor(self.preferences.get("fill_color", "#ffffff"))
        )
        self.border_color_widget.set_color(
            QColor(self.preferences.get("border_color", "#000000"))
        )
        self.label_color_widget.set_color(
            QColor(self.preferences.get("label_color", "#000000"))
        )

        self.options_map["transparent_background"].setChecked(
            self.preferences.get("transparent_background", False)
        )
        self.options_map["show_border"].setChecked(
            self.preferences.get("show_border", False)
        )
        self.options_map["show_label"].setChecked(
            self.preferences.get("show_label", False)
        )

        project_folder = QgsProject.instance().homePath()
        default_folder = os.path.join(project_folder, "svgs")
        output_folder = self.preferences.get("output_folder", default_folder)
        self.folder_selector.set_paths([output_folder])

    def _save_prefs(self):
        self.logger.debug("Salvando preferencias do VectorToSvg")

        current_layer = self.layer_input.current_layer()
        self.preferences["layer_id"] = current_layer.id() if current_layer else ""
        self.preferences["fill_color"] = self.fill_color_widget.get_color().name(
            QColor.HexArgb
        )
        self.preferences["border_color"] = self.border_color_widget.get_color().name(
            QColor.HexArgb
        )
        self.preferences["label_color"] = self.label_color_widget.get_color().name(
            QColor.HexArgb
        )
        self.preferences["transparent_background"] = self.options_map[
            "transparent_background"
        ].isChecked()
        self.preferences["show_border"] = self.options_map["show_border"].isChecked()
        self.preferences["show_label"] = self.options_map["show_label"].isChecked()

        paths = self.folder_selector.get_paths()
        project_folder = QgsProject.instance().homePath()
        self.preferences["output_folder"] = (
            paths[0] if paths else os.path.join(project_folder, "svgs")
        )

        self.preferences["window_width"] = self.width()
        self.preferences["window_height"] = self.height()

        save_tool_prefs(self.TOOL_KEY, self.preferences)

    def execute_tool(self):
        self.logger.debug(
            "VectorToSvgPlugin inicializado apenas com interface. Execucao ainda nao implementada."
        )
    def _set_folder_to_project(self):
        self.logger.debug("Definindo pasta para pasta do projeto")
        project_folder = QgsProject.instance().homePath()
        export_folder = os.path.join(project_folder, "svgs")
        self.folder_selector.set_paths([export_folder])
        self.logger.debug(f"Pasta definida para: {export_folder}")


def run(iface):
    dlg = VectorToSvgPlugin(iface)
    dlg.setModal(False)
    dlg.show()
    return dlg
