# -*- coding: utf-8 -*-
import os
from qgis.PyQt.QtGui import QIcon
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
from ..core.config.LogUtils import LogUtils
from ..utils.Preferences import Preferences
from ..utils.ToolKeys import ToolKey


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
    prefs = {}  # para armazenar preferências carregadas
    INSTRUCTIONS_FILE = None
    TOOL_KEY = None
    ALGORITHM_NAME = None
    ALGORITHM_DISPLAY_NAME = None
    ALGORITHM_GROUP = GROUP_VETORIAL
    ICON = "cadmus_icon.ico"

    def shortHelpString(self):
        if self.INSTRUCTIONS_FILE:
            path = os.path.join(
                os.path.dirname(__file__),
                "..",
                "resources",
                "instructions",
                "html",
                self.INSTRUCTIONS_FILE,
            )
            try:
                with open(path, encoding="utf-8") as f:
                    return f.read()
            except Exception as e:                
                return f
        else:
            return

    def icon(self):
        icon_path = os.path.join(
            os.path.dirname(__file__), "..", "resources", "icons", self.ICON
        )
        if os.path.exists(icon_path):
            return QIcon(icon_path)
        return QIcon()

    def createInstance(self):
        return self.__class__()

    def name(self):
        if self.ALGORITHM_NAME:
            return self.ALGORITHM_NAME
        raise NotImplementedError(
            "Algoritmo precisa definir ALGORITHM_NAME ou override name()."
        )

    def displayName(self):
        if self.ALGORITHM_DISPLAY_NAME:
            return self.ALGORITHM_DISPLAY_NAME
        raise NotImplementedError(
            "Algoritmo precisa definir ALGORITHM_DISPLAY_NAME ou override displayName()."
        )

    def group(self):
        return (
            self.ALGORITHM_GROUP.name
            if self.ALGORITHM_GROUP
            else self.GROUP_VETORIAL.name
        )

    def groupId(self):
        return (
            self.ALGORITHM_GROUP.id if self.ALGORITHM_GROUP else self.GROUP_VETORIAL.id
        )

    def load_preferences(self):
        if not self.TOOL_KEY:
            return {}
        try:
            self.prefs = Preferences.load_tool_prefs(self.TOOL_KEY)
        except Exception as e:
            LogUtils(
                tool=ToolKey.UNTRACEABLE,
                class_name=self.__class__.__name__,
                level=LogUtils.WARNING,
            ).warning(f"Falha ao carregar preferências de {self.TOOL_KEY}: {e}")
            return {}
    
