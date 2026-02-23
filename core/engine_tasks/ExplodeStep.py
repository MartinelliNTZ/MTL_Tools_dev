# -*- coding: utf-8 -*-
import os
import tempfile

from .BaseStep import BaseStep
from .ExecutionContext import ExecutionContext
from ..task.ExplodeHugeLayerTask import ExplodeHugeLayerTask
from ...utils.vector.VectorLayerSource import VectorLayerSource


class ExplodeStep(BaseStep):

    def name(self) -> str:
        return "explode"

    def create_task(self, context: ExecutionContext):

        context.require(["layer", "tool_key"])

        layer = context.get("layer")
        tool_key = context.get("tool_key")

        tmp_dir = context.get("tmp_dir")
        if not tmp_dir:
            tmp_dir = tempfile.mkdtemp(prefix="pipeline_")
            context.set("tmp_dir", tmp_dir)

        input_path = os.path.join(tmp_dir, "input.gpkg")
        exploded_path = os.path.join(tmp_dir, "exploded.gpkg")

        input_path = VectorLayerSource.save_vector_layer_to_file(
            layer=layer,
            output_path=input_path,
            decision="overwrite",
            external_tool_key=tool_key
        )

        if not input_path:
            raise RuntimeError("Falha ao exportar camada para explode.")

        return ExplodeHugeLayerTask(
            input_path=input_path,
            output_path=exploded_path,
            tool_key=tool_key
        )

    def on_success(self, context: ExecutionContext, result):
        context.set("current_path", result)