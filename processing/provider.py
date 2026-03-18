# -*- coding: utf-8 -*-
import os
from qgis.PyQt.QtGui import QIcon
from qgis.core import QgsProcessingProvider
from .RasterMassSampler import RasterMassSampler
from .RasterMassClipper import RasterMassClipper
from .DifferenceFields import DifferenceFieldsAlgorithm
from .AttributeStatistics import AttributeStatistics
from .GeometryLineFromPoints import GeometryLineFromPoints

# from .elevation_analisys import ElevationAnalisys


class MTLProvider(QgsProcessingProvider):

    def loadAlgorithms(self):
        print("[DEBUG] Registrando algoritmos MTL…")
        self.addAlgorithm(RasterMassSampler())
        self.addAlgorithm(RasterMassClipper())
        self.addAlgorithm(DifferenceFieldsAlgorithm())
        self.addAlgorithm(AttributeStatistics())
        self.addAlgorithm(GeometryLineFromPoints())

    def id(self):
        return "cadmus"

    def name(self):
        return "Cadmus"

    def longName(self):
        return "Cadmus – Processamento"

    def icon(self):
        path = os.path.join(
            os.path.dirname(__file__), "..", "resources", "icons", "cadmus_icon.ico"
        )
        return QIcon(path)
