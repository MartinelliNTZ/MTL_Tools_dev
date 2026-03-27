# -*- coding: utf-8 -*-
from qgis.PyQt.QtGui import QColor
from qgis.core import QgsMapLayerProxyModel

from .BasePlugin import BasePluginMTL
from ..core.ui.WidgetFactory import WidgetFactory
from ..utils.ToolKeys import ToolKey


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
            enable_selected_checkbox=False,
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
        }
        options_layout, self.options_map = WidgetFactory.create_checkbox_grid(
            options,
            items_per_row=1,
            checked_by_default=False,
            title=None,
            separator_top=False,
            separator_bottom=True,
        )

        self.layout.add_items(
            [
                layer_layout,
                fill_layout,
                border_layout,
                label_layout,
                options_layout,
            ]
        )

    def execute_tool(self):
        self.logger.debug(
            "VectorToSvgPlugin inicializado apenas com interface. Execucao ainda nao implementada."
        )


def run(iface):
    dlg = VectorToSvgPlugin(iface)
    dlg.setModal(False)
    dlg.show()
    return dlg
