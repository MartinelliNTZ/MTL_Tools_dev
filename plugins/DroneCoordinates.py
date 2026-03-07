# -*- coding: utf-8 -*-
import os

#from shapely import points
from qgis.PyQt.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton
)
from qgis.core import QgsProject, QgsApplication
from ..plugins.BasePlugin import BasePluginMTL
from ..core.engine_tasks.AsyncPipelineEngine import AsyncPipelineEngine
from ..core.engine_tasks.ExecutionContext import ExecutionContext
from ..core.engine_tasks.MrkParseStep import MrkParseStep
from ..core.engine_tasks.PhotoMetadataStep import PhotoMetadataStep
from ..utils.mrk.mrk_parser import MrkParser
from ..utils.mrk.photo_metadata import PhotoMetadata
from ..utils.vector.VectorLayerGeometry import VectorLayerGeometry
from ..utils.vector.VectorLayerSource import VectorLayerSource
from ..core.config.LogUtilsNew import LogUtilsNew
from ..utils.string_utils import StringUtils

from ..utils.preferences import load_tool_prefs, save_tool_prefs
from ..utils.ToolKeys import ToolKey
from ..core.ui.WidgetFactory import WidgetFactory
from pathlib import Path


class DroneCordinates(BasePluginMTL):

    TOOL_KEY = ToolKey.DRONE_COORDINATES

    LABEL_RECURSIVE = "Vasculhar subpastas"
    LABEL_MERGE = "Unir todos os MRKs"
    LABEL_PHOTOS = "Cruzar com metadados das fotos (Não recomendado para grandes volumes)"

    def __init__(self, iface):
        super().__init__(iface.mainWindow())
        self.iface = iface

        # Inicializar logger de sessão (arquivo JSON)
        plugin_root = Path(__file__).parent.parent
        LogUtilsNew.init(plugin_root)

        # Inicializa a UI e preferências via BasePluginMTL
        self.init(
            self.TOOL_KEY,
            "Drone Coordinates",
            load_settings_prefs=False,
            build_ui=True,
            min_width=250,
            min_height=450,
        )

    def _build_ui(self, **kwargs):
        super()._build_ui(
            title="Coordenadas de Drone",
            icon_path="coord.ico",
            instructions_file="drone_coordinates_help.md",
            min_width=250   ,
            min_height=450,
        )

        # ====== PASTA MRK ======
        folder_layout, self.folder_selector = WidgetFactory.create_path_selector(
            parent=self,
            title="Pasta MRK:",
            mode="folder",
        )

        # ====== OPÇÕES ======
        opts_layout, self.checkbox_map = WidgetFactory.create_checkbox_grid(
            names=[
                self.LABEL_RECURSIVE,
                self.LABEL_MERGE,
                self.LABEL_PHOTOS,
            ],
            items_per_row=1,
            checked_by_default=False,
            title="Opções",
        )

        # ====== SALVAMENTO ======
        save_points_layout, self.save_points_selector = WidgetFactory.create_save_file_selector(
            parent=self,
            file_filter=StringUtils.FILTER_VECTOR,
            checkbox_text="Salvar pontos MRK em arquivo? (caso não marcado: camada temporária)",
            label_text="Salvar em:",

        )

        save_track_layout, self.save_track_selector = WidgetFactory.create_save_file_selector(
            parent=self,
            file_filter=StringUtils.FILTER_VECTOR,
            checkbox_text="Salvar rastro em arquivo? (caso não marcado: camada temporária)",
            label_text="Salvar em:",
        )

        # ====== ESTILO (QML) - Parâmetros Avançados ======
        qml_points_layout, self.qml_points_selector = WidgetFactory.create_qml_selector(
            parent=self,
            checkbox_text="Aplicar estilo (QML) nos pontos?",
            label_text="QML pontos:",
        )

        qml_track_layout, self.qml_track_selector = WidgetFactory.create_qml_selector(
            parent=self,
            checkbox_text="Aplicar estilo (QML) no rastro?",
            label_text="QML:",
        )

        adv_layout, self.adv_params = WidgetFactory.create_collapsible_parameters(
            parent=self,
            title="Parâmetros Avançados",
            expanded_by_default=False,
        )
        self.adv_params.add_content_layout(qml_points_layout)
        self.adv_params.add_content_layout(qml_track_layout)

        # ====== BOTOES ======
        buttons_layout, self.action_buttons = WidgetFactory.create_bottom_action_buttons(
            parent=self,
            run_callback=self._run,
            close_callback=self.close,
            info_callback=self.show_info_dialog,
            tool_key=self.TOOL_KEY,
        )

        self.layout.add_items(
            [
                folder_layout,
                opts_layout,
                save_points_layout,
                save_track_layout,
                adv_layout,
                buttons_layout,
            ]
        )

    def _load_prefs(self):
        self.logger.debug("Carregando preferências", code="PREFS_LOAD_START")
        prefs = load_tool_prefs(self.TOOL_KEY)

        folder_path = prefs.get("folder", "")
        if folder_path:
            self.folder_selector.set_path(folder_path)
            self.logger.debug(
                "Caminho restaurado", code="PREFS_FOLDER_RESTORED", path=folder_path
            )

        # Checkboxes
        self.checkbox_map[self.LABEL_RECURSIVE].setChecked(prefs.get("recursive", True))
        self.checkbox_map[self.LABEL_MERGE].setChecked(prefs.get("merge", True))
        self.checkbox_map[self.LABEL_PHOTOS].setChecked(prefs.get("photos", True))

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

        self.logger.debug("Preferências carregadas", code="PREFS_LOAD_COMPLETE")

    def _save_prefs(self):
        self.logger.debug("Salvando preferências", code="PREFS_SAVE_START")

        paths = self.folder_selector.get_paths()
        folder_path = paths[0] if paths else ""

        save_tool_prefs(
            self.TOOL_KEY,
            {
                "folder": folder_path,
                "recursive": self.checkbox_map[self.LABEL_RECURSIVE].isChecked(),
                "merge": self.checkbox_map[self.LABEL_MERGE].isChecked(),
                "photos": self.checkbox_map[self.LABEL_PHOTOS].isChecked(),
                "save_file": self.save_track_selector.is_enabled(),
                "save_file_pts": self.save_points_selector.is_enabled(),
                "output_path": self.save_track_selector.get_file_path(),
                "output_path_pts": self.save_points_selector.get_file_path(),
                "apply_style_track": self.qml_track_selector.is_enabled(),
                "qml_path_track": self.qml_track_selector.get_file_path(),
                "apply_style_points": self.qml_points_selector.is_enabled(),
                "qml_path_points": self.qml_points_selector.get_file_path(),
            },
        )

        self.logger.debug("Preferências salvas", code="PREFS_SAVE_COMPLETE")

    def _run(self):
        self.logger.info("Iniciando processamento de coordenadas de drone", code="EXEC_START")

        paths = self.folder_selector.get_paths()
        if not paths:
            self.logger.error("Nenhum diretório selecionado", code="NO_SELECTION")
            return

        recursive = self.checkbox_map[self.LABEL_RECURSIVE].isChecked()
        merge = self.checkbox_map[self.LABEL_MERGE].isChecked()
        apply_photos = self.checkbox_map[self.LABEL_PHOTOS].isChecked()

        extra_fields = PhotoMetadata.FIELDS_PHOTO if apply_photos else None

        context = ExecutionContext()
        context.set("paths", paths)
        context.set("recursive", recursive)
        context.set("merge", merge)
        context.set("extra_fields", extra_fields)
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

            QgisMessageUtil.modal_error(
                self.iface,
                "Erro: camada final não encontrada no contexto."
            )
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
                    toolkey=self.TOOL_KEY,
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

        # ===== TRAÇO =====
        points = context.get("points", []) or []
        vl_line = VectorLayerGeometry.create_line_layer_from_points(points)
        if vl_line:
            out_layer = None
            save_to_file = self.save_track_selector.is_enabled()
            out_path = (
                self.save_track_selector.get_file_path().strip() if save_to_file else None
            )
            if save_to_file and out_path:
                saved_layer = VectorLayerSource.save_and_load_layer(
                    vl_line,
                    out_path,
                    toolkey=self.TOOL_KEY,
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
        QgisMessageUtil.bar_success(self.iface, "Processamento executado com sucesso.")

        # Persistir preferências
        self._save_prefs()


def run_drone_cordinates(iface):
    dlg = DroneCordinates(iface)
    dlg.setModal(False)
    dlg.show()
    return dlg
