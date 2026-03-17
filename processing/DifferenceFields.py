# -*- coding: utf-8 -*-
import os
from PyQt5.QtGui import QIcon
from ..core.config.LogUtils import LogUtils
from qgis.core import (    
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterField,
    QgsProcessingParameterString,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterNumber,
    QgsProcessing,
)
from ..utils.ToolKeys import ToolKey
from ..utils.Preferences import Preferences
#from .model.difference_fields_model import DifferenceFieldsModel
from PyQt5.QtCore import QVariant
from .BaseProcessingAlgorithm import BaseProcessingAlgorithm
from qgis.core import QgsFields, QgsField, QgsFeature, QgsFeatureSink
from PyQt5.QtCore import QVariant



class DifferenceFieldsAlgorithm(BaseProcessingAlgorithm):
    
    TOOL_KEY = ToolKey.DIFFERENCE_FIELDS
    ALGORITHM_NAME = "difference_fields"
    ALGORITHM_DISPLAY_NAME = "Gerador de Diferenças entre Campos"
    ALGORITHM_GROUP = BaseProcessingAlgorithm.GROUP_ESTATISTICA
    ICON = "field_diference.ico"
    INSTRUCTIONS_FILE = "difference_fields.html"
    logger = LogUtils(tool=TOOL_KEY, class_name="DifferenceFieldsAlgorithm", level="DEBUG")
    
    #especificas do algoritmo
    INPUT_LAYER = "INPUT_LAYER"
    BASE_FIELD = "BASE_FIELD"
    EXCLUDE_FIELDS = "EXCLUDE_FIELDS"  # <-- AGORA É EXCLUÍR CAMPOS
    PREFIX = "PREFIX"
    PRECISION = "PRECISION"
    OUTPUT = "OUTPUT"

    NUMERIC = {
        QVariant.Int,
        QVariant.UInt,
        QVariant.LongLong,
        QVariant.ULongLong,
        QVariant.Double,
    } 

    def save_prefs(self, prefix, precision):
        Preferences.save_tool_prefs(self.TOOL_KEY, {"prefix": prefix, "precision": precision})

    # Definição dos parâmetros
    def initAlgorithm(self, config=None):
        self.logger.debug("Inicializando parâmetros do algoritmo DifferenceFieldsAlgorithm…")
        self.load_preferences()

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT_LAYER, "Camada de Pontos", [QgsProcessing.TypeVectorPoint]
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                self.BASE_FIELD,
                "Campo Base (subtraendo)",
                parentLayerParameterName=self.INPUT_LAYER,
                type=QgsProcessingParameterField.Numeric,
            )
        )

        param_exclude = QgsProcessingParameterField(
            self.EXCLUDE_FIELDS,
            "Campos a EXCLUIR do cálculo",
            parentLayerParameterName=self.INPUT_LAYER,
            type=QgsProcessingParameterField.Numeric,
            allowMultiple=True,
        )
        param_exclude.setFlags(
            param_exclude.flags() | QgsProcessingParameterField.FlagOptional
        )
        self.addParameter(param_exclude)

        self.addParameter(
            QgsProcessingParameterString(
                self.PREFIX, "Prefixo para novos campos", defaultValue=self.prefs.get("prefix", "diff_")
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.PRECISION,
                "Precisão (casas decimais)",
                type=QgsProcessingParameterNumber.Integer,
                minValue=0,
                maxValue=10,
                defaultValue=self.prefs.get("precision", 2),
            )
        )

        self.addParameter(QgsProcessingParameterFeatureSink(self.OUTPUT, "Diferenca"))

    # PROCESSAMENTO
    def processAlgorithm(self, params, context, feedback):
        layer = self.parameterAsSource(params, self.INPUT_LAYER, context)
        base_field = self.parameterAsFields(params, self.BASE_FIELD, context)[0]

        # Lê os campos a excluir (podem ser 0)
        excludeds = self.parameterAsFields(params, self.EXCLUDE_FIELDS, context)

        prefix = self.parameterAsString(params, self.PREFIX, context)
        precision = self.parameterAsInt(params, self.PRECISION, context)

        # ------------------------------------------------------------
        # SE O USUÁRIO NÃO INFORMAR NADA → USAR TODOS OS CAMPOS MENOS O BASE
        # ------------------------------------------------------------
        if not excludeds or len(excludeds) == 0:
            fields_to_compare = [
                f.name()
                for f in layer.fields()
                if f.type() in self.NUMERIC and f.name() != base_field
            ]
            feedback.pushInfo(
                "Nenhum campo excluído → usando todos os campos numéricos."
            )
        else:
            # Se informou campos para excluir, usar todos MENOS esses
            fields_to_compare = [
                f.name()
                for f in layer.fields()
                if f.type() in self.NUMERIC and f.name() not in excludeds and f.name() != base_field
            ]

        feedback.pushInfo(f"Base: {base_field}")
        feedback.pushInfo(f"Campos EXCLUÍDOS: {excludeds}")
        feedback.pushInfo(f"Campos utilizados no cálculo: {fields_to_compare}")
        feedback.pushInfo(f"Prefixo: {prefix}")
        feedback.pushInfo(f"Precisão: {precision}")

        # Salvar preferências
        self.save_prefs(prefix, precision)

        # Campos de saída
        out_fields = self.create_output_fields(layer, fields_to_compare, prefix=prefix)

        sink, dest = self.parameterAsSink(
            params, self.OUTPUT, context, out_fields, layer.wkbType(), layer.sourceCrs()
        )

        # Processar feições
        self.process_features(layer, base_field, fields_to_compare, out_fields, sink, precision=precision)

        feedback.pushInfo("✔ Processo finalizado com sucesso.")

        return {self.OUTPUT: dest}
    
    def create_output_fields(self, source_layer, fields_to_compare, prefix="diff_"):
        out_fields = QgsFields()
        for f in source_layer.fields():
            out_fields.append(f)

        for col in fields_to_compare:
            new_name = f"{prefix}{col}"
            out_fields.append(QgsField(new_name, QVariant.Double))

        return out_fields

    def process_features(self, layer, base_field, fields_to_compare, out_fields, sink, precision=2):
        for feat in layer.getFeatures():
            geom = feat.geometry()
            attrs = feat.attributes()
            base_value = feat[base_field]

            out_feat = QgsFeature(out_fields)
            out_feat.setGeometry(geom)

            for col in fields_to_compare:
                value = feat[col]
                if value is None or base_value is None:
                    attrs.append(None)
                else:
                    diff = float(value) - float(base_value)
                    attrs.append(round(diff, precision))

            out_feat.setAttributes(attrs)
            sink.addFeature(out_feat, QgsFeatureSink.FastInsert)
