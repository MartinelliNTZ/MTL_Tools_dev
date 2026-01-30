import processing
from qgis.core import QgsVectorLayer
from .BaseTask import BaseTask
from ..config.LogUtils import LogUtils
from ...utils.vector.VectorLayerGeometry import VectorLayerGeometry
import time

class ExplodeHugeLayerTask(BaseTask):
    """
    Explode linhas usando processing em arquivo físico.
    Seguro para milhões de feições.
    """

    def __init__(
        self,
        *,
        input_path: str,
        output_path: str,
        tool_key: str
    ):
        super().__init__("Explodindo linhas (heavy)", tool_key)
        self.input_path = input_path
        self.output_path = output_path
        LogUtils.log(f"ExplodeHugeLayerTask initialized for {self.input_path} -> {self.output_path}", level="DEBUG", tool=self.tool_key, class_name=self.__class__.__name__)

    def _run(self) -> bool:
        if self.isCanceled():
            LogUtils.log("ExplodeHugeLayerTask canceled before start", level="INFO", tool=self.tool_key, class_name=self.__class__.__name__)
            return False
        LogUtils.log(f"Starting explode task for {self.input_path} -> {self.output_path}", level="INFO", tool=self.tool_key, class_name=self.__class__.__name__)       
        ok = VectorLayerGeometry.explode_lines_to_path(
            input_path=self.input_path,
            output_path=self.output_path,
            external_tool_key=self.tool_key
        )

        if not ok:
            return False

        self.result = self.output_path
        return True

        LogUtils.log("Explosão concluída, continuando processamento", level="INFO", tool=self.tool_key, class_name=self.__class__.__name__)

        return True
