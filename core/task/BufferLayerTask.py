from .BaseTask import BaseTask
from .TaskFeedback import TaskFeedback
from ..config.LogUtils import LogUtils
from ...utils.vector.VectorLayerGeometry import VectorLayerGeometry
import time



class BufferLayerTask(BaseTask):
    """
    Executa buffer em arquivo físico (GPKG).
    Seguro para grandes volumes.
    """

    def __init__(
        self,
        *,
        input_path: str,
        output_path: str,
        distance: float,
        segments: int = 5,
        end_cap_style: int = 1,
        join_style: int = 1,
        miter_limit: float = 2.0,
        dissolve: bool = False,
        tool_key: str
    ):
        super().__init__("Gerando buffer (heavy)", tool_key)

        self.input_path = input_path
        self.output_path = output_path
        self.distance = distance
        self.segments = segments
        self.end_cap_style = end_cap_style
        self.join_style = join_style
        self.miter_limit = miter_limit
        self.dissolve = dissolve

        LogUtils.log(
            f"BufferLayerTask initialized: {self.input_path} -> {self.output_path}, distance={self.distance}",
            level="DEBUG",
            tool=self.tool_key,
            class_name=self.__class__.__name__
        )

    def _run(self) -> bool:

        if self.isCanceled():
            LogUtils.log(
                "BufferLayerTask canceled before start",
                level="INFO",
                tool=self.tool_key,
                class_name=self.__class__.__name__
            )
            return False

        LogUtils.log(
            f"Starting buffer task: {self.input_path} -> {self.output_path}",
            level="INFO",
            tool=self.tool_key,
            class_name=self.__class__.__name__
        )
        feedback = TaskFeedback(self)

        try:
            VectorLayerGeometry.create_buffer_to_path_safe(
                input_path=self.input_path,
                output_path=self.output_path,
                distance=self.distance,
                segments=self.segments,
                end_cap_style=self.end_cap_style,
                join_style=self.join_style,
                miter_limit=self.miter_limit,
                dissolve=self.dissolve,
                external_tool_key=self.tool_key,
                feedback = feedback,
            )
            #            time.sleep(10)

        except Exception as e:
            LogUtils.log(
                f"Erro no buffer: {str(e)}",
                level="CRITICAL",
                tool=self.tool_key,
                class_name=self.__class__.__name__
            )
            raise

        if self.isCanceled():
            LogUtils.log(
                "BufferLayerTask canceled after execution",
                level="INFO",
                tool=self.tool_key,
                class_name=self.__class__.__name__
            )
            return False

        self.result = self.output_path

        LogUtils.log(
            "BufferLayerTask completed successfully",
            level="INFO",
            tool=self.tool_key,
            class_name=self.__class__.__name__
        )

        return True
