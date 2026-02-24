# core/engine_tasks/SaveVectorStep.py

from .BaseStep import BaseStep
from ..task.SaveVectorLayerTask import SaveVectorLayerTask
from qgis.core import QgsVectorLayer


class SaveVectorStep(BaseStep):

    def name(self) -> str:
        return "SaveVectorStep"

    def create_task(self, context):

        context.require(["current_path", "tool_key"])

        current_path = context.get("current_path")
        save_to_folder = context.get("save_to_folder", False)
        output_path = context.get("output_path")
        output_name = context.get("output_name")
        tool_key = context.get("tool_key")

        layer = QgsVectorLayer(current_path, output_name, "ogr")

        if not layer.isValid():
            raise RuntimeError("SaveVectorStep: falha ao carregar camada do current_path.")

        return SaveVectorLayerTask(
            layer=layer,
            output_path=output_path,
            save_to_folder=save_to_folder,
            output_name=output_name or layer.name(),
            decision="rename",
            tool_key=tool_key
        )

    def on_success(self, context, result):

        if not result:
            raise RuntimeError("SaveVectorStep: falha ao salvar camada.")

        context.set("layer", result)