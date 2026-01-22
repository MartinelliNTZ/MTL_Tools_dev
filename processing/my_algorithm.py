# -*- coding: utf-8 -*-
from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterRasterLayer,
    QgsProcessingParameterNumber
)

class MTLExampleAlgorithm(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterNumber(
                "VALOR",
                "Número de exemplo",
                QgsProcessingParameterNumber.Double,
                defaultValue=123.45
            )
        )

    def processAlgorithm(self, parameters, context, feedback):

        valor = self.parameterAsDouble(parameters, "VALOR", context)

        feedback.pushInfo(f"Executando algoritmo exemplo…")
        feedback.pushInfo(f"Valor informado: {valor}")

        return {}

    def name(self):
        return "algoritmode exemplo"

    def displayName(self):
        return "Algoritimo de Exemplo (MTL)"

    def group(self):
        return "Exemplo"

    def groupId(self):
        return "exemplo"

    def shortHelpString(self):
        return "Exemplo mínimo de algoritmo para aparecer na Caixa de Processamento."
    def createInstance(self):
        return MTLExampleAlgorithm()

