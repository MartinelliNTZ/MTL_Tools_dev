# drone_task.py
# -*- coding: utf-8 -*-
import os
from qgis.core import QgsTask
from ..mrk.photo_metadata import PhotoMetadata
from ..log_utils import LogUtils
from ..tool_keys import ToolKey

class DronePhotosTask(QgsTask):
    TOOL_KEY = ToolKey.DRONE_COORDINATES

    def __init__(self, description, points, base_folder, recursive=True, callback=None):
        super().__init__(description, QgsTask.CanCancel)
        LogUtils.log(self.TOOL_KEY, f"Inicializando task: {description}")
        self.points = points
        self.base_folder = base_folder
        self.recursive = recursive
        self.result_points = None
        self.callback = callback

    # ---------- RUN SEM ARGUMENTOS ----------
    def run(self):
        LogUtils.log(self.TOOL_KEY, f"ENTRANDO NO RUN DA TASK: cruzando fotos em {self.base_folder}")
        try:
            self.result_points = PhotoMetadata.enrich(
                self.points,
                base_folder=self.base_folder,
                recursive=self.recursive
            )
            self.setProgress(100)  # atualiza progresso no QGIS
            LogUtils.log(self.TOOL_KEY, f"Cruzamento concluído ({len(self.result_points)} pontos)")
            self.finished(True)
            return True
        except Exception as e:
            LogUtils.exception(self.TOOL_KEY, e)
            return False

    # ---------- CALLBACK FINAL ----------
    def finished(self, result):
        LogUtils.log(self.TOOL_KEY, f"FINALIZANDO TASK: {self.description()}")
        if result and self.callback:
            self.callback(self.result_points)
        elif not result:
            LogUtils.log(self.TOOL_KEY, "O cruzamento de fotos falhou ou foi cancelado")
