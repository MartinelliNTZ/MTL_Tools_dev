# -*- coding: utf-8 -*-
import os
from PyQt5.QtGui import QIcon
from qgis.core import (
    QgsProcessingAlgorithm,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterFolderDestination,
    QgsProcessingParameterBoolean,
    QgsProcessing,
    QgsVectorLayer,
    QgsCoordinateTransform,
    QgsProject,
)

import processing
class GroupProcessing:
        def __init__(self, id=None, name=None, icon_path="cadmus_icon.ico"):
            self.id = id
            self.name = name
            self.icon_path = icon_path

class BaseProcessingAlgorithm(QgsProcessingAlgorithm):
    """
    Base class for processing algorithms in the Cadmus plugin.
    """
    GROUP_ESTATISTICA = GroupProcessing(id="estatistica", name="Estatística")
    GROUP_RASTER = GroupProcessing(id="raster", name="Raster")
    GROUP_VETORIAL = GroupProcessing(id="vetorial", name="Vetorial")

    def icon(self,icon_path = "cadmus_icon.ico"):

        path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "resources",
            "icons",
            icon_path,
        )

        return QIcon(path)
    

