# -*- coding: utf-8 -*-
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

class BaseProcessingAlgorithm(QgsProcessingAlgorithm):
    """
    Base class for processing algorithms in the Cadmus plugin.
    """

