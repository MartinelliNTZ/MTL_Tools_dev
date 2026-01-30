from qgis.core import QgsTask, QgsMessageLog, Qgis
from ..config.LogUtils import LogUtils

class BaseTask(QgsTask):
    """
    Classe base para todas as tasks do plugin.

    Responsabilidades:
    - Executar processamento pesado fora da UI
    - Capturar exceções de forma segura
    - Permitir cancelamento
    - Retornar resultado para o controller
    """

    def __init__(self, description: str, tool_key="untraceable"):
        super().__init__(description, QgsTask.CanCancel)
        self.tool_key = tool_key
        self.exception = None
        self.result = None

        LogUtils.log("Task initialized", level="DEBUG", tool=self.tool_key, class_name=self.__class__.__name__)

        # callbacks
        self.on_success = None
        self.on_error = None

    def run(self) -> bool:
        LogUtils.log("Task started", level="INFO", tool=self.tool_key, class_name=self.__class__.__name__)
        try:
            return self._run()
        except Exception as e:
            self.exception = e
            LogUtils.log(f"Unhandled exception in task: {e}", level="CRITICAL", tool=self.tool_key, class_name=self.__class__.__name__)
            return False

    def finished(self, success: bool):
        if success:
            LogUtils.log("Task finished successfully", level="INFO", tool=self.tool_key, class_name=self.__class__.__name__)
            if callable(self.on_success):
                self.on_success(self.result)
            return

        # erro
        LogUtils.log(f"Task finished with error: {self.exception}", level="CRITICAL", tool=self.tool_key, class_name=self.__class__.__name__)
        if callable(self.on_error):
            self.on_error(self.exception)
        else:
            QgsMessageLog.logMessage(
                str(self.exception),
                self.tool_key,
                Qgis.Critical
            )

    def _run(self) -> bool:
        raise NotImplementedError