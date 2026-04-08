# -*- coding: utf-8 -*-
import os
from qgis.core import QgsProject
from ..plugins.BasePlugin import BasePluginMTL
from ..core.engine_tasks.AsyncPipelineEngine import AsyncPipelineEngine
from ..core.engine_tasks.ExecutionContext import ExecutionContext
from ..core.engine_tasks.MrkParseStep import MrkParseStep
from ..core.engine_tasks.PhotoMetadataStep import PhotoMetadataStep
from ..utils.mrk.PhotoMetadata import PhotoMetadata
from ..utils.vector.VectorLayerGeometry import VectorLayerGeometry
from ..utils.vector.VectorLayerSource import VectorLayerSource
from ..utils.StringManager import StringManager
from ..utils.Preferences import load_tool_prefs, save_tool_prefs
from ..utils.ToolKeys import ToolKey
from ..core.ui.WidgetFactory import WidgetFactory
from ..i18n.TranslationManager import STR
from ..utils.DependenciesManager import DependenciesManager
from ..utils.QgisMessageUtil import QgisMessageUtil
from ..utils.adapter.StringAdapter import StringAdapter
from ..utils.mrk.MetadataFields import MetadataFields


class DroneCordinates(BasePluginMTL):

    TOOL_KEY = ToolKey.DRONE_COORDINATES

    CHECKBOX_OPTIONS = {
        "recursive": STR.RECURSIVE_SEARCH,
        "photos": STR.PHOTOS_METADATA,
    }

    PREF_REQUIRED_FIELDS = "required_fields_selected"
    PREF_CUSTOM_FIELDS = "custom_fields_selected"
    PREF_MRK_FIELDS = "mrk_fields_selected"

    def __init__(self, iface):
        super().__init__(iface.mainWindow())
        self.iface = iface

        # Inicializa a UI e preferÃªncias via BasePluginMTL
        self.init(
            self.TOOL_KEY,
            "Drone Coordinates",
            load_settings_prefs=False,
            build_ui=True,
        )

    def _build_ui(self, **kwargs):
        super()._build_ui(
            title=STR.DRONE_COORDINATES_TITLE,
            icon_path="coord.ico",
            enable_scroll=True,
        )

        # ====== PASTA MRK ======
        folder_layout, self.folder_selector = WidgetFactory.create_path_selector(
            parent=self,
            title=STR.MRK_FOLDER,
            mode="folder",
            separator_bottom=True,
        )

        # ====== OPÃ‡Ã•ES (CollapsibleParametersWidget) ======
        opts_layout, self.opts_collapsible = (
            WidgetFactory.create_collapsible_parameters(
                parent=self,
                title=STR.OPTIONS,
                expanded_by_default=False,
            )
        )

        # Criar checkboxes
        opts_checkbox_layout, self.checkbox_map = WidgetFactory.create_checkbox_grid(
            options_data=self.CHECKBOX_OPTIONS,
            items_per_row=1,
            checked_by_default=False,
            separator_bottom=False,
        )
        self.opts_collapsible.add_content_layout(opts_checkbox_layout)

        # Connect checkbox toggles for dependency checks
        self.chk_photos = self.checkbox_map.get("photos")
        if self.chk_photos:
            self.chk_photos.toggled.connect(self.on_photos_changed)

        # ====== METADATA REQUIRED FIELDS ======
        required_layout, self.required_fields_collapsible = (
            WidgetFactory.create_collapsible_parameters(
                parent=self,
                title="Required Fields",
                expanded_by_default=False,
            )
        )
        required_items = StringAdapter.to_key_label_description(
            MetadataFields.REQUIRED_FIELDS
        )
        req_grid_layout, self.required_fields_grid = WidgetFactory.create_checkbox_grid(
            options_data=required_items,
            items_per_row=2,
            checked_by_default=True,
            return_widget=True,
            separator_bottom=False,
        )
        self.required_fields_collapsible.add_content_layout(req_grid_layout)

        # ====== METADATA CUSTOM FIELDS ======
        custom_layout, self.custom_fields_collapsible = (
            WidgetFactory.create_collapsible_parameters(
                parent=self,
                title="Custom Fields",
                expanded_by_default=False,
            )
        )
        custom_items = StringAdapter.to_key_label_description(MetadataFields.CUSTOM_FIELDS)
        custom_grid_layout, self.custom_fields_grid = WidgetFactory.create_checkbox_grid(
            options_data=custom_items,
            items_per_row=2,
            checked_by_default=False,
            return_widget=True,
            separator_bottom=False,
        )
        self.custom_fields_collapsible.add_content_layout(custom_grid_layout)

        # ====== METADATA MRK FIELDS ======
        mrk_layout, self.mrk_fields_collapsible = (
            WidgetFactory.create_collapsible_parameters(
                parent=self,
                title="MRK Fields",
                expanded_by_default=False,
            )
        )
        mrk_items = StringAdapter.to_key_label_description(MetadataFields.MRK_FIELDS)
        mrk_grid_layout, self.mrk_fields_grid = WidgetFactory.create_checkbox_grid(
            options_data=mrk_items,
            items_per_row=2,
            checked_by_default=True,
            return_widget=True,
            separator_bottom=False,
        )
        self.mrk_fields_collapsible.add_content_layout(mrk_grid_layout)

        # ====== SALVAMENTO (CollapsibleParametersWidget) ======
        save_layout, self.save_collapsible = (
            WidgetFactory.create_collapsible_parameters(
                parent=self,
                title=STR.SAVING,
                expanded_by_default=False,
            )
        )

        save_points_layout, self.save_points_selector = (
            WidgetFactory.create_save_file_selector(
                parent=self,
                file_filter=StringManager.FILTER_VECTOR,
                checkbox_text=STR.SAVE_POINTS_CHECKBOX,
                label_text=STR.SAVE_IN,
                separator_top=False,
                separator_bottom=False,
            )
        )

        save_track_layout, self.save_track_selector = (
            WidgetFactory.create_save_file_selector(
                parent=self,
                file_filter=StringManager.FILTER_VECTOR,
                checkbox_text=STR.SAVE_TRACK_CHECKBOX,
                label_text=STR.SAVE_IN,
                separator_top=False,
                separator_bottom=False,
            )
        )

        self.save_collapsible.add_content_layout(save_points_layout)
        self.save_collapsible.add_content_layout(save_track_layout)

        # ====== ESTILOS (QML) - CollapsibleParametersWidget ======
        styles_layout, self.styles_collapsible = (
            WidgetFactory.create_collapsible_parameters(
                parent=self,
                title=STR.STYLES,
                expanded_by_default=False,
            )
        )

        qml_points_layout, self.qml_points_selector = WidgetFactory.create_qml_selector(
            parent=self,
            checkbox_text=STR.APPLY_STYLE_POINTS,
            label_text=STR.QML_POINTS,
            separator_top=False,
            separator_bottom=False,
        )

        qml_track_layout, self.qml_track_selector = WidgetFactory.create_qml_selector(
            parent=self,
            checkbox_text=STR.APPLY_STYLE_TRACK,
            label_text=STR.QML_TRACK,
            separator_top=False,
            separator_bottom=False,
        )

        self.styles_collapsible.add_content_layout(qml_points_layout)
        self.styles_collapsible.add_content_layout(qml_track_layout)

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

        # ====== CONTEÃšDO AO LAYOUT ======
        # MainLayout encapsula o scroll internamente
        # add_items() roteia automaticamente para scroll ou inner_layout
        self.layout.add_items(
            [
                folder_layout,
                opts_layout,
                required_layout,
                custom_layout,
                mrk_layout,
                save_layout,
                styles_layout,
                buttons_layout,
            ]
        )

    def _ensure_photos_dependency(self, checked: bool):
        if not checked:
            return

        if DependenciesManager.check_dependency("Pillow", self.TOOL_KEY):
            return

        confirmed = QgisMessageUtil.confirm(
            self.iface,
            STR.PHOTOS_METADATA_REQUIRED_MESSAGE,
            STR.REQUIRED_LIBRARY,
        )

        if not confirmed:
            self.chk_photos.setChecked(False)
            return

        started = DependenciesManager.install_dependency_gui(
            "Pillow", self.iface, self.TOOL_KEY
        )

        if not started:
            QgisMessageUtil.modal_error(
                self.iface,
                STR.INSTALL_DEPENDENCY_FAILED.format("Pillow"),
            )
            self.chk_photos.setChecked(False)

    def on_photos_changed(self, checked: bool):
        self._ensure_photos_dependency(checked)


    def _get_selected_required_fields(self):
        return self.required_fields_grid.get_checked_keys()

    def _get_selected_custom_fields(self):
        return self.custom_fields_grid.get_checked_keys()

    def _get_selected_mrk_fields(self):
        return self.mrk_fields_grid.get_checked_keys()

    def _load_prefs(self):
        self.logger.debug("Carregando preferÃªncias", code="PREFS_LOAD_START")
        prefs = load_tool_prefs(self.TOOL_KEY)

        folder_path = prefs.get("folder", "")
        if folder_path:
            self.folder_selector.set_path(folder_path)
            self.logger.debug(
                "Caminho restaurado", code="PREFS_FOLDER_RESTORED", path=folder_path
            )

        # Checkboxes
        self.checkbox_map["recursive"].setChecked(prefs.get("recursive", True))
        self.checkbox_map["photos"].setChecked(prefs.get("photos", True))

        # Filtros de campos de metadata
        required_selected = prefs.get(self.PREF_REQUIRED_FIELDS)
        custom_selected = prefs.get(self.PREF_CUSTOM_FIELDS)
        mrk_selected = prefs.get(self.PREF_MRK_FIELDS)

        if isinstance(required_selected, list):
            self.required_fields_grid.set_checked_keys(required_selected)
        if isinstance(custom_selected, list):
            self.custom_fields_grid.set_checked_keys(custom_selected)
        if isinstance(mrk_selected, list):
            self.mrk_fields_grid.set_checked_keys(mrk_selected)


        # Salvamento
        self.save_points_selector.set_enabled(prefs.get("save_file_pts", False))
        self.save_points_selector.set_file_path(prefs.get("output_path_pts", ""))
        self.save_track_selector.set_enabled(prefs.get("save_file", False))
        self.save_track_selector.set_file_path(prefs.get("output_path", ""))

        # Estilo (QML)
        self.qml_points_selector.set_enabled(prefs.get("apply_style_points", False))
        self.qml_points_selector.set_file_path(prefs.get("qml_path_points", ""))
        self.qml_track_selector.set_enabled(prefs.get("apply_style_track", False))
        self.qml_track_selector.set_file_path(prefs.get("qml_path_track", ""))

        # Estados dos CollapsibleParametersWidget
        self.opts_collapsible.set_expanded(prefs.get("opts_expanded", True))
        self.required_fields_collapsible.set_expanded(
            prefs.get("required_expanded", False)
        )
        self.custom_fields_collapsible.set_expanded(
            prefs.get("custom_expanded", False)
        )
        self.mrk_fields_collapsible.set_expanded(
            prefs.get("mrk_expanded", False)
        )
        self.save_collapsible.set_expanded(prefs.get("save_expanded", False))
        self.styles_collapsible.set_expanded(prefs.get("styles_expanded", False))

        self.logger.debug("PreferÃªncias carregadas", code="PREFS_LOAD_COMPLETE")

    def _save_prefs(self):
        self.logger.debug("Salvando preferÃªncias", code="PREFS_SAVE_START")

        paths = self.folder_selector.get_paths()
        folder_path = paths[0] if paths else ""

        prefs_data = {
            "folder": folder_path,
            "recursive": self.checkbox_map["recursive"].isChecked(),
            "photos": self.checkbox_map["photos"].isChecked(),
            self.PREF_REQUIRED_FIELDS: self._get_selected_required_fields(),
            self.PREF_CUSTOM_FIELDS: self._get_selected_custom_fields(),
            self.PREF_MRK_FIELDS: self._get_selected_mrk_fields(),
            "save_file": self.save_track_selector.is_enabled(),
            "save_file_pts": self.save_points_selector.is_enabled(),
            "output_path": self.save_track_selector.get_file_path(),
            "output_path_pts": self.save_points_selector.get_file_path(),
            "apply_style_track": self.qml_track_selector.is_enabled(),
            "qml_path_track": self.qml_track_selector.get_file_path(),
            "apply_style_points": self.qml_points_selector.is_enabled(),
            "qml_path_points": self.qml_points_selector.get_file_path(),
            # Estados dos CollapsibleParametersWidget
            "opts_expanded": self.opts_collapsible.is_expanded(),
            "required_expanded": self.required_fields_collapsible.is_expanded(),
            "custom_expanded": self.custom_fields_collapsible.is_expanded(),
            "mrk_expanded": self.mrk_fields_collapsible.is_expanded(),
            "save_expanded": self.save_collapsible.is_expanded(),
            "styles_expanded": self.styles_collapsible.is_expanded(),
            # Tamanho da janela (persistido automaticamente por BasePlugin.closeEvent)
            "window_width": self.width(),
            "window_height": self.height(),
        }
        save_tool_prefs(self.TOOL_KEY, prefs_data)

        self.logger.debug("PreferÃªncias salvas", code="PREFS_SAVE_COMPLETE")

    def execute_tool(self):
        self.logger.info(
            "Iniciando processamento de coordenadas de drone", code="EXEC_START"
        )

        paths = self.folder_selector.get_paths()
        if not paths:
            self.logger.error("Nenhum diretÃ³rio selecionado", code="NO_SELECTION")
            return

        recursive = self.checkbox_map["recursive"].isChecked()
        apply_photos = self.checkbox_map["photos"].isChecked()

        if apply_photos and not DependenciesManager.check_dependency("Pillow", self.TOOL_KEY):
            self.logger.warning(
                "Cruzamento com metadados solicitado sem Pillow disponÃ­vel; serÃ¡ ignorado"
            )
            apply_photos = False
            self.checkbox_map["photos"].setChecked(False)

        extra_fields = None

        context = ExecutionContext()
        context.set("paths", paths)
        context.set("recursive", recursive)
        context.set("extra_fields", extra_fields)
        context.set("selected_required_fields", self._get_selected_required_fields())
        context.set("selected_custom_fields", self._get_selected_custom_fields())
        context.set("selected_mrk_fields", self._get_selected_mrk_fields())
        context.set("tool_key", self.TOOL_KEY)
        context.set("points_layer_name", "MRK_Pontos")

        steps = [MrkParseStep()]
        if apply_photos:
            steps.append(PhotoMetadataStep())

        self.logger.debug(
            "Iniciando pipeline de processamento",
            code="PIPELINE_START",
            steps=[s.name() for s in steps],
        )

        engine = AsyncPipelineEngine(
            steps=steps,
            context=context,
            on_finished=self._on_pipeline_finished,
            on_error=self._on_pipeline_error,
        )
        engine.start()

    def _on_pipeline_finished(self, context):
        layer = context.get("layer")
        if not layer or not layer.isValid():
            from ..utils.QgisMessageUtil import QgisMessageUtil

            QgisMessageUtil.modal_error(self.iface, STR.ERROR_LAYER_NOT_FOUND)
            return

        if not QgsProject.instance().mapLayer(layer.id()):
            QgsProject.instance().addMapLayer(layer)

        # ===== PONTOS =====
        if self.save_points_selector.is_enabled():
            out_path = self.save_points_selector.get_file_path().strip()
            if out_path:
                saved_layer = VectorLayerSource.save_and_load_layer(
                    layer,
                    out_path,
                    tool_key=self.TOOL_KEY,
                    decision="rename",
                )
                if saved_layer and saved_layer.isValid():
                    QgsProject.instance().addMapLayer(saved_layer)
                    layer = saved_layer

        if self.qml_points_selector.is_enabled():
            qml = self.qml_points_selector.get_file_path().strip()
            if qml and os.path.exists(qml):
                ok = layer.loadNamedStyle(qml)
                if isinstance(ok, tuple):
                    ok = ok[0]
                if ok:
                    layer.triggerRepaint()

        # ===== TRAÃ‡O =====
        points = context.get("points", []) or []
        vl_line = VectorLayerGeometry.create_line_layer_from_points(
            points,
            group_by_fields=["mrk_path", "mrk_file"],
            attribute_fields=[
                "date_name",
                "folder",
                "mrk_file",
                "mrk_path",
                "flight_number",
                "flight_name",
            ],
        )
        if vl_line:
            out_layer = None
            save_to_file = self.save_track_selector.is_enabled()
            out_path = (
                self.save_track_selector.get_file_path().strip()
                if save_to_file
                else None
            )
            if save_to_file and out_path:
                saved_layer = VectorLayerSource.save_and_load_layer(
                    vl_line,
                    out_path,
                    tool_key=self.TOOL_KEY,
                    decision="rename",
                )
                if saved_layer and saved_layer.isValid():
                    out_layer = saved_layer
                    QgsProject.instance().addMapLayer(out_layer)
            else:
                out_layer = vl_line
                QgsProject.instance().addMapLayer(out_layer)

            if self.qml_track_selector.is_enabled() and out_layer:
                qml = self.qml_track_selector.get_file_path().strip()
                if qml and os.path.exists(qml):
                    ok = out_layer.loadNamedStyle(qml)
                    if isinstance(ok, tuple):
                        ok = ok[0]
                    if ok:
                        out_layer.triggerRepaint()

        from ..utils.QgisMessageUtil import QgisMessageUtil

        QgisMessageUtil.bar_success(self.iface, STR.SUCCESS_MESSAGE)


def run(iface):
    dlg = DroneCordinates(iface)
    dlg.setModal(False)
    dlg.show()
    return dlg
