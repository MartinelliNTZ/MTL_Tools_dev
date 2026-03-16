# -*- coding: utf-8 -*-
import os
from PyQt5.QtGui import QIcon

from qgis.core import (
    QgsProcessingAlgorithm,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterFolderDestination,
    QgsProcessing,
)

import processing

from ..utils.Preferences import load_tool_prefs, save_tool_prefs
from ..utils.ToolKeys import ToolKey


TOOL_KEY = ToolKey.RASTER_MASS_CLIPPER


class RasterMassClipper(QgsProcessingAlgorithm):
    """
    QgsProcessingAlgorithm: Recorte massivo de rasters usando camada máscara.
    """

    INPUT_MASK = "INPUT_MASK"
    INPUT_RASTERS = "INPUT_RASTERS"
    OUTPUT_FOLDER = "OUTPUT_FOLDER"

    def name(self):
        return "raster_mass_clipper"

    def displayName(self):
        return "Recorte Massivo de Rasters"

    def createInstance(self):
        return RasterMassClipper()

    # -------------------------- INIT -------------------------
    def initAlgorithm(self, config=None):

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT_MASK,
                "Camada máscara (polígono)",
                [QgsProcessing.TypeVectorPolygon],
            )
        )

        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUT_RASTERS,
                "Rasters",
                QgsProcessing.TypeRaster,
            )
        )

        self.addParameter(
            QgsProcessingParameterFolderDestination(
                self.OUTPUT_FOLDER,
                "Pasta de saída",
            )
        )

    # ----------------------- PROCESS -------------------------
    def processAlgorithm(self, params, context, feedback):

        rasters = self.parameterAsLayerList(params, self.INPUT_RASTERS, context)
        out_folder = self.parameterAsString(params, self.OUTPUT_FOLDER, context)

        os.makedirs(out_folder, exist_ok=True)

        total = len(rasters)

        for i, ras in enumerate(rasters):

            if feedback.isCanceled():
                break

            feedback.setProgress(int((i / total) * 100))

            raster_path = ras.source()
            base = os.path.splitext(os.path.basename(raster_path))[0]

            out_path = os.path.join(out_folder, f"{base}_clip.tif")

            feedback.pushInfo(f"Recortando: {base}")

            processing.run(
                "gdal:cliprasterbymasklayer",
                {
                    "INPUT": raster_path,
                    "MASK": params[self.INPUT_MASK],
                    "SOURCE_CRS": None,
                    "TARGET_CRS": None,
                    "NODATA": None,
                    "ALPHA_BAND": False,
                    "CROP_TO_CUTLINE": True,
                    "KEEP_RESOLUTION": True,
                    "OPTIONS": "",
                    "DATA_TYPE": 0,
                    "OUTPUT": out_path,
                },
                context=context,
                feedback=feedback,
            )

        # ----------------- SALVAR PREFERÊNCIAS -----------------

        prefs = load_tool_prefs(TOOL_KEY)
        prefs["last_output_folder"] = out_folder
        save_tool_prefs(TOOL_KEY, prefs)

        clickable = f'<a href="file:///{out_folder}">{out_folder}</a>'
        feedback.pushInfo(f"Arquivos salvos em: {clickable}")

        return {self.OUTPUT_FOLDER: out_folder}

    # ------------------------ UI INFO ------------------------

    def icon(self):
        path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "resources",
            "icons",
            "raster_clip_mass.ico",
        )
        return QIcon(path)

    def group(self):
        return "Estatistica"

    def groupId(self):
        return "estatistica"