# -*- coding: utf-8 -*-

from qgis.core import QgsMapLayerProxyModel, QgsVectorLayer

from .BasePlugin import BasePluginMTL
from ..core.ui.WidgetFactory import WidgetFactory
from ..i18n.TranslationManager import STR
from ..utils.Preferences import load_tool_prefs, save_tool_prefs
from ..utils.QgisMessageUtil import QgisMessageUtil
from ..utils.ToolKeys import ToolKey
from ..utils.judge.SequentialPointBreakJudge import SequentialPointBreakJudge
from ..utils.vector.VectorLayerAttributes import VectorLayerAttributes


class DividePointsByStripsPlugin(BasePluginMTL):
    TOOL_KEY = ToolKey.DIVIDE_POINTS_BY_STRIPS

    def __init__(self, iface):
        super().__init__(iface.mainWindow())
        self.iface = iface
        self.init(
            tool_key=self.TOOL_KEY,
            class_name=self.__class__.__name__,
            build_ui=True,
        )

    def _build_ui(self, **kwargs):
        super()._build_ui(
            title=STR.DIVIDE_POINTS_BY_STRIPS_TITLE,
            icon_path="vector.ico",
            enable_scroll=True,
        )

        intro_label = WidgetFactory.create_label(
            text=STR.DIVIDE_POINTS_BY_STRIPS_INTRO,
            word_wrap=True,
            parent=self,
        )

        layer_layout, self.layer_input = WidgetFactory.create_layer_input(
            label_text=STR.INPUT_POINTS,
            filters=[QgsMapLayerProxyModel.PointLayer],
            allow_empty=False,
            enable_selected_checkbox=False,
            parent=self,
            separator_top=False,
            separator_bottom=True,
        )
        self.layer_input.layerChanged.connect(self._on_layer_changed)

        operational_container_layout, self.operational_params = (
            WidgetFactory.create_collapsible_parameters(
                parent=self,
                title=STR.OPERATIONAL_PARAMETERS,
                expanded_by_default=True,
                separator_top=False,
                separator_bottom=True,
            )
        )
        id_field_layout, self.id_field_selector = WidgetFactory.create_dropdown_selector(
            title=STR.UNIQUE_SEQUENTIAL_ID_FIELD,
            options_dict={},
            allow_empty=True,
            empty_text=STR.SELECT,
            parent=self,
            separator_top=False,
            separator_bottom=False,
        )
        time_field_layout, self.time_field_selector = (
            WidgetFactory.create_dropdown_selector(
                title=STR.TIMESTAMP_FIELD,
                options_dict={},
                allow_empty=True,
                empty_text=STR.SELECT,
                parent=self,
                separator_top=False,
                separator_bottom=False,
            )
        )
        operational_layout, self.operational_fields = WidgetFactory.create_input_fields_widget(
            fields_dict={
                "frequencia_pontos": {
                    "title": STR.EXPECTED_POINT_FREQUENCY_SECONDS,
                    "type": "int",
                    "default": 1,
                },
                "largura_tiro": {
                    "title": STR.EXPECTED_LATERAL_WIDTH_METERS,
                    "type": "float",
                    "default": 20.0,
                },
            },
            parent=self,
            separator_top=False,
            separator_bottom=False,
        )
        self.operational_params.add_content_layout(id_field_layout)
        self.operational_params.add_content_layout(time_field_layout)
        self.operational_params.add_content_layout(operational_layout)

        sensitivity_layout, self.sensitivity_fields = (
            WidgetFactory.create_input_fields_widget(
                fields_dict={
                    "janela_azimute": {
                        "title": STR.AZIMUTH_MOVING_WINDOW,
                        "type": "int",
                        "default": 10,
                    },
                    "threshold_azimute_leve": {
                        "title": STR.LIGHT_AZIMUTH_DEVIATION_THRESHOLD,
                        "type": "float",
                        "default": 20.0,
                    },
                    "threshold_azimute_grave": {
                        "title": STR.SEVERE_AZIMUTH_DEVIATION_THRESHOLD,
                        "type": "float",
                        "default": 45.0,
                    },
                    "score_minimo_quebra": {
                        "title": STR.MINIMUM_BREAK_SCORE,
                        "type": "int",
                        "default": 3,
                    },
                    "n_minimo_pontos": {
                        "title": STR.MINIMUM_POINT_COUNT,
                        "type": "int",
                        "default": 20,
                    },
                    "tolerancia_tempo": {
                        "title": STR.TIME_TOLERANCE_MULTIPLIER,
                        "type": "float",
                        "default": 3.0,
                    },
                },
                parent=self,
                separator_top=False,
                separator_bottom=False,
            )
        )

        advanced_layout, self.advanced_params = (
            WidgetFactory.create_collapsible_parameters(
                parent=self,
                title=STR.SENSITIVITY_PARAMETERS,
                expanded_by_default=True,
                separator_top=False,
                separator_bottom=True,
            )
        )
        self.advanced_params.add_content_layout(sensitivity_layout)

        buttons_layout, self.action_buttons = (
            WidgetFactory.create_bottom_action_buttons(
                parent=self,
                run_callback=self.execute_tool,
                close_callback=self.close,
                info_callback=self.show_info_dialog,
                tool_key=self.TOOL_KEY,
                separator_top=False,
                separator_bottom=False,
            )
        )

        self.layout.add_items(
            [
                intro_label,
                layer_layout,
                operational_container_layout,
                advanced_layout,
                buttons_layout,
            ]
        )
        self._refresh_field_selectors()

    def _load_prefs(self):
        self.preferences = load_tool_prefs(self.TOOL_KEY)
        self.id_field = self.preferences.get("id_field", "")
        self.time_field = self.preferences.get("time_field", "")
        operational_fields = self.preferences.get("operational_fields", {})
        if (
            "largura_lateral" in operational_fields
            and "largura_tiro" not in operational_fields
        ):
            operational_fields["largura_tiro"] = operational_fields["largura_lateral"]
        self.operational_fields.set_values(operational_fields)
        self.sensitivity_fields.set_values(
            self.preferences.get("sensitivity_fields", {})
        )
        self._refresh_field_selectors()

    def _save_prefs(self):
        self.preferences["id_field"] = self.id_field_selector.get_selected_key() or ""
        self.preferences["time_field"] = (
            self.time_field_selector.get_selected_key() or ""
        )
        self.preferences["operational_fields"] = self.operational_fields.get_values()
        self.preferences["sensitivity_fields"] = self.sensitivity_fields.get_values()
        self.preferences["window_width"] = self.width()
        self.preferences["window_height"] = self.height()
        save_tool_prefs(self.TOOL_KEY, self.preferences)

    def _on_layer_changed(self, _layer):
        self._refresh_field_selectors()

    def _refresh_field_selectors(self):
        layer = self.layer_input.current_layer()
        options = VectorLayerAttributes.get_field_options(layer)

        selected_id = getattr(self, "id_field", "") or self.preferences.get(
            "id_field", ""
        )
        selected_time = getattr(self, "time_field", "") or self.preferences.get(
            "time_field", ""
        )

        self.id_field_selector.set_options(options)
        self.time_field_selector.set_options(options)

        if selected_id:
            self.id_field_selector.set_selected_key(selected_id)
        if selected_time:
            self.time_field_selector.set_selected_key(selected_time)

    def execute_tool(self):
        layer = self.layer_input.current_layer()
        if not isinstance(layer, QgsVectorLayer):
            QgisMessageUtil.bar_warning(
                self.iface, STR.SELECT_POINT_VECTOR_LAYER
            )
            return

        if not layer.isEditable():
            QgisMessageUtil.bar_warning(self.iface, STR.SELECT_EDITABLE_VECTOR_LAYER)
            return

        field_id = self.id_field_selector.get_selected_key()
        field_time = self.time_field_selector.get_selected_key()
        if not field_id or not field_time:
            QgisMessageUtil.bar_warning(self.iface, STR.SELECT_REQUIRED_FIELDS)
            return

        operational_values = self.operational_fields.get_values()
        sensitivity_values = self.sensitivity_fields.get_values()

        self.logger.info(
            "Executando segmentação de tiros em camada de pontos",
            layer=layer.name(),
            source_path=layer.source(),
            id_field=field_id,
            time_field=field_time,
            operational_fields=operational_values,
            sensitivity_fields=sensitivity_values,
        )

        try:
            summary = SequentialPointBreakJudge(
                layer=layer,
                tool_key=self.TOOL_KEY,
            ).judge(
                field_id=field_id,
                field_time=field_time,
                point_frequency_seconds=float(
                    operational_values.get("frequencia_pontos", 1) or 1
                ),
                strip_width_meters=float(
                    operational_values.get("largura_tiro", 20.0) or 20.0
                ),
                azimuth_window=int(
                    sensitivity_values.get("janela_azimute", 10) or 10
                ),
                light_azimuth_threshold=float(
                    sensitivity_values.get("threshold_azimute_leve", 20.0) or 20.0
                ),
                severe_azimuth_threshold=float(
                    sensitivity_values.get("threshold_azimute_grave", 45.0) or 45.0
                ),
                minimum_break_score=int(
                    sensitivity_values.get("score_minimo_quebra", 3) or 3
                ),
                minimum_point_count=int(
                    sensitivity_values.get("n_minimo_pontos", 20) or 20
                ),
                time_tolerance_multiplier=float(
                    sensitivity_values.get("tolerancia_tempo", 3.0) or 3.0
                ),
                conflict_resolver=lambda field_name: QgisMessageUtil.ask_field_conflict(
                    self.iface, field_name
                ),
            )
        except Exception as e:
            self.logger.error(f"Erro na segmentação de tiros: {e}")
            self.logger.exception(e)
            QgisMessageUtil.bar_critical(
                self.iface, f"{STR.ERROR}\n{e}"
            )
            return

        try:
            layer.triggerRepaint()
        except Exception as e:
            self.logger.warning(f"Falha ao atualizar camada após julgamento: {e}")

        QgisMessageUtil.bar_success(
            self.iface,
            STR.SHOT_SEGMENTATION_BUFFER_COMPLETED.format(
                total_points=summary["total_points"],
                total_shots=summary["total_shots"],
                valid_shots=summary["valid_shots"],
                invalid_shots=summary["invalid_shots"],
            ),
            duration=8,
        )


def run(iface):
    dlg = DividePointsByStripsPlugin(iface)
    dlg.setModal(False)
    dlg.show()
    return dlg
