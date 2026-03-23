# -*- coding: utf-8 -*-
import os

from qgis.core import QgsProject, QgsVectorLayer

from ..engine_tasks.AsyncPipelineEngine import AsyncPipelineEngine
from ..engine_tasks.ExecutionContext import ExecutionContext
from ..engine_tasks.MrkParseStep import MrkParseStep
from ...i18n.TranslationManager import STR
from ...utils.QgisMessageUtil import QgisMessageUtil
from ...utils.ToolKeys import ToolKey
from ...utils.ExplorerUtils import ExplorerUtils
from ...utils.vector.VectorLayerGeometry import VectorLayerGeometry
from ...utils.vector.VectorLayerSource import VectorLayerSource


class DroneCoordinatesRunner:
    """Executa o pipeline de MRK fora da UI principal do dialog."""

    def __init__(self, iface, tool_key=ToolKey.DRONE_COORDINATES):
        self.iface = iface
        self.tool_key = tool_key
        self._engine = None
        self._on_finished = None
        self._on_error = None

    def run_mrk_file(
        self,
        file_path: str,
        *,
        on_finished=None,
        on_error=None,
    ) -> bool:
        if not file_path or not os.path.isfile(file_path):
            return False

        self._on_finished = on_finished
        self._on_error = on_error

        points_path = ExplorerUtils.build_suffixed_output_path(
            file_path, STR.POINTS.lower()
        )
        track_path = ExplorerUtils.build_suffixed_output_path(
            file_path, STR.TRACK.lower()
        )

        existing_points = self._load_existing_layer(points_path)
        existing_track = self._load_existing_layer(track_path)
        if existing_points and existing_track:
            self._load_layer(existing_points)
            self._load_layer(existing_track)
            QgisMessageUtil.bar_success(
                self.iface, STR.LOADED_EXISTING_GPKG, duration=4
            )
            if callable(self._on_finished):
                self._on_finished(
                    {
                        "file_path": file_path,
                        "points_layer": existing_points,
                        "track_layer": existing_track,
                        "used_existing": True,
                    }
                )
            return True

        context = ExecutionContext()
        context.set("paths", [file_path])
        context.set("recursive", False)
        context.set("extra_fields", None)
        context.set("tool_key", self.tool_key)
        context.set("points_layer_name", f"{STR.POINTS}")
        context.set("track_layer_name", f"{STR.TRACK}")
        context.set("auto_points_output_path", points_path)
        context.set("auto_track_output_path", track_path)
        context.set("source_mrk_file", file_path)

        self._engine = AsyncPipelineEngine(
            steps=[MrkParseStep()],
            context=context,
            on_finished=self._on_pipeline_finished,
            on_error=self._on_pipeline_error,
        )
        self._engine.start()
        return True

    def _on_pipeline_finished(self, context: ExecutionContext):
        layer = context.get("layer")
        points = context.get("points", []) or []

        if not layer or not layer.isValid():
            self._notify_error(STR.ERROR_LAYER_NOT_FOUND)
            return

        points_output_path = context.get("auto_points_output_path")
        track_output_path = context.get("auto_track_output_path")

        points_layer = self._save_or_load_existing(
            layer,
            points_output_path,
            fallback_name=STR.POINTS,
        )
        if points_layer and points_layer.id() != layer.id():
            QgsProject.instance().removeMapLayer(layer.id())

        line_layer = VectorLayerGeometry.create_line_layer_from_points(
            points,
            name=STR.TRACK,
            group_by_fields=["mrk_path", "mrk_file"],
            attribute_fields=[
                "data_name",
                "folder",
                "mrk_file",
                "mrk_path",
                "numdovoo",
                "nomedovoo",
            ],
        )

        track_layer = None
        if line_layer and line_layer.isValid():
            track_layer = self._save_or_load_existing(
                line_layer,
                track_output_path,
                fallback_name=STR.TRACK,
            )

        QgisMessageUtil.bar_success(self.iface, STR.CONVERT_FILE_SUCCESS, duration=4)
        if callable(self._on_finished):
            self._on_finished(
                {
                    "file_path": context.get("source_mrk_file"),
                    "points_layer": points_layer,
                    "track_layer": track_layer,
                    "used_existing": False,
                }
            )

    def _on_pipeline_error(self, errors):
        exc = errors[0] if errors else Exception(STR.CONVERT_FILE_ERROR)
        self._notify_error(str(exc))

    def _notify_error(self, message: str):
        QgisMessageUtil.bar_critical(self.iface, f"{STR.CONVERT_FILE_ERROR} {message}")
        if callable(self._on_error):
            self._on_error(message)

    def _save_or_load_existing(
        self,
        layer: QgsVectorLayer,
        output_path: str,
        *,
        fallback_name: str,
    ):
        existing = self._load_existing_layer(output_path)
        if existing:
            self._load_layer(existing)
            return existing

        saved_layer = VectorLayerSource.save_and_load_layer(
            layer,
            output_path,
            tool_key=self.tool_key,
            decision="overwrite",
        )

        if saved_layer and saved_layer.isValid():
            saved_layer.setName(fallback_name)
            self._load_layer(saved_layer)
            return saved_layer

        # Fallback: se falhar ao salvar, ainda disponibiliza a camada em memoria.
        layer.setName(fallback_name)
        self._load_layer(layer)
        return layer

    def _load_existing_layer(self, path: str):
        if not path or not os.path.exists(path):
            return None
        layer = QgsVectorLayer(path, os.path.splitext(os.path.basename(path))[0], "ogr")
        if not layer.isValid():
            return None
        return layer

    def _load_layer(self, layer: QgsVectorLayer):
        if not layer or not layer.isValid():
            return
        if not QgsProject.instance().mapLayer(layer.id()):
            QgsProject.instance().addMapLayer(layer)
