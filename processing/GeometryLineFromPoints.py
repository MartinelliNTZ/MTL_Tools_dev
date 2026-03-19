# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QVariant
from ..core.config.LogUtils import LogUtils
from qgis.core import (
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterField,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterBoolean,
    QgsProcessing,
    QgsFields,
    QgsField,
    QgsFeature,
    QgsFeatureSink,
    QgsGeometry,
    QgsWkbTypes,
    QgsProcessingException,
)
from .BaseProcessingAlgorithm import BaseProcessingAlgorithm
from ..utils.ToolKeys import ToolKey


class GeometryLineFromPoints(BaseProcessingAlgorithm):
    TOOL_KEY = ToolKey.GEOMETRY_LINE_FROM_POINTS
    ALGORITHM_NAME = "geometry_difference_line"
    ALGORITHM_DISPLAY_NAME = "Linha de Diferença entre Pontos"
    ALGORITHM_GROUP = BaseProcessingAlgorithm.GROUP_VETORIAL
    ICON = "line_difference.ico"
    INSTRUCTIONS_FILE = "geometry_difference_line.html"

    # especificas do algoritmo
    INPUT_LAYER_A = "INPUT_LAYER_A"
    INPUT_LAYER_B = "INPUT_LAYER_B"
    USE_SECOND_LAYER = "USE_SECOND_LAYER"
    FIELD_A = "FIELD_A"
    FIELD_B = "FIELD_B"
    OUTPUT = "OUTPUT"
    DISPLAY_HELP = "DISPLAY_HELP"

    logger = LogUtils(
        tool=TOOL_KEY, class_name="GeometryLineFromPointsAlgorithm", level="DEBUG"
    )

    def initAlgorithm(self, config=None):
        self.load_preferences()  # use load prefs direto sem sobrescrever
        self.logger.debug(f"Preferências carregadas: {self.prefs}")

        self.logger.debug(
            "Inicializando parâmetros do algoritmo GeometryLineFromPointsAlgorithm…"
        )
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT_LAYER_A,
                "Camada de Pontos (Modo 1) / Primeira Camada (Modo 2)",
                [QgsProcessing.TypeVectorPoint],
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                self.FIELD_A,
                "Atributo base - camada A",
                parentLayerParameterName=self.INPUT_LAYER_A,
                type=QgsProcessingParameterField.Any,
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.USE_SECOND_LAYER,
                "Usar segunda camada (modo 2)",
                defaultValue=self.prefs.get("use_second_layer", False),
            )
        )

        layer_b_param = QgsProcessingParameterFeatureSource(
            self.INPUT_LAYER_B,
            "Segunda Camada de Pontos (Modo 2 - opcional)",
            [QgsProcessing.TypeVectorPoint],
            optional=True,
        )
        layer_b_param.setFlags(
            layer_b_param.flags() | QgsProcessingParameterFeatureSource.FlagOptional
        )
        self.addParameter(layer_b_param)

        field_b_param = QgsProcessingParameterField(
            self.FIELD_B,
            "Atributo base - camada B (modo 2)",
            parentLayerParameterName=self.INPUT_LAYER_B,
            type=QgsProcessingParameterField.Any,
            optional=True,
        )
        field_b_param.setFlags(
            field_b_param.flags() | QgsProcessingParameterField.FlagOptional
        )
        self.addParameter(field_b_param)

        self.addParameter(
            QgsProcessingParameterFeatureSink(self.OUTPUT, "Linhas de diferenças")
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.DISPLAY_HELP,
                "Exibir campo de ajuda (Necessario executar e reiniciar)",
                defaultValue=self.prefs.get("display_help", True),
            )
        )

    @staticmethod
    def _feature_point(feat):
        geom = feat.geometry()
        if geom is None or geom.isEmpty():
            return None

        if geom.type() == QgsWkbTypes.PointGeometry:
            try:
                point = geom.asPoint()
                if point is None:
                    return None
                return point
            except Exception:
                LogUtils(
                    tool=GeometryLineFromPoints.TOOL_KEY, class_name="GeometryLine"
                ).warning(f"Erro ao extrair ponto da geometria do recurso {feat.id()}")

        # Para MultiPoint ou outro, usa centroide
        try:
            centroid = geom.centroid()
            if centroid is None or centroid.isEmpty():
                return None
            return centroid.asPoint()
        except Exception:
            return None

    @staticmethod
    def _append_line_features(features, sink, out_fields, key_name):
        for f1, f2 in features:
            geom1 = GeometryLineFromPoints._feature_point(f1)
            geom2 = GeometryLineFromPoints._feature_point(f2)
            if geom1 is None or geom2 is None:
                GeometryLineFromPoints.logger.warning(
                    f"Ignorando par vazio em '{key_name}' (geom1={geom1}, geom2={geom2})"
                )
                continue

            line = QgsGeometry.fromPolylineXY([geom1, geom2])
            if line is None or line.isEmpty():
                GeometryLineFromPoints.logger.warning(
                    f"Geometria de linha inválida para par {f1.id()}-{f2.id()}"
                )
                continue

            distance = geom1.distance(geom2)
            out_feat = QgsFeature(out_fields)
            out_feat.setGeometry(line)
            out_feat.setAttributes(
                [key_name, int(f1.id()), int(f2.id()), float(distance)]
            )
            sink.addFeature(out_feat, QgsFeatureSink.FastInsert)
            GeometryLineFromPoints.logger.debug(
                f"Adicionada linha: group={key_name}, a={f1.id()}, b={f2.id()}, d={distance:.3f}"
            )

    def processAlgorithm(self, params, context, feedback):
        self.logger.debug("processAlgorithm iniciado")
        layer_a = self.parameterAsSource(params, self.INPUT_LAYER_A, context)
        if layer_a is None:
            self.logger.error("Camada A inválida")
            raise QgsProcessingException("Camada A inválida.")

        use_second = self.parameterAsBool(params, self.USE_SECOND_LAYER, context)
        layer_b = self.parameterAsSource(params, self.INPUT_LAYER_B, context)

        field_a = self.parameterAsString(params, self.FIELD_A, context)
        field_b = (
            self.parameterAsString(params, self.FIELD_B, context)
            if layer_b is not None
            else None
        )

        self.logger.debug(
            f"Parâmetros: use_second={use_second}, field_a={field_a}, field_b={field_b}"
        )

        if use_second and layer_b is None:
            raise QgsProcessingException(
                "Modo 2 requisita uma segunda camada de pontos."
            )

        if use_second and not field_b:
            raise QgsProcessingException(
                "No modo 2 informe o campo de agrupamento da camada B."
            )

        fields = QgsFields()
        fields.append(QgsField("group_key", QVariant.String))
        fields.append(QgsField("feature_a", QVariant.Int))
        fields.append(QgsField("feature_b", QVariant.Int))
        fields.append(QgsField("distance", QVariant.Double))

        (sink, dest_id) = self.parameterAsSink(
            params,
            self.OUTPUT,
            context,
            fields,
            QgsWkbTypes.LineString,
            layer_a.sourceCrs(),
        )

        if sink is None:
            raise QgsProcessingException("Erro ao criar camada de saída.")

        if use_second:
            # Modo 2: pares entre camadas A e B pelo valor do campo
            index_b = {}
            for feat_b in layer_b.getFeatures():
                key = feat_b[field_b]
                if key is None:
                    continue
                index_b.setdefault(str(key), []).append(feat_b)

            for feat_a in layer_a.getFeatures():
                key = feat_a[field_a]
                if key is None:
                    continue
                matches = index_b.get(str(key))
                if not matches:
                    continue

                pair_list = [(feat_a, feat_b) for feat_b in matches]
                self._append_line_features(pair_list, sink, fields, str(key))

        else:
            # Modo 1: uma camada, pares sequenciais por atributo
            groups = {}
            for feat in layer_a.getFeatures():
                key = feat[field_a]
                if key is None:
                    continue
                groups.setdefault(str(key), []).append(feat)

            for key_name, feats in groups.items():
                if len(feats) < 2:
                    continue
                # ordena para garantir ordem estável
                feats = sorted(feats, key=lambda f: f.id())

                pair_list = [(feats[i], feats[i + 1]) for i in range(len(feats) - 1)]
                self._append_line_features(pair_list, sink, fields, str(key_name))

        display_help = (
            bool(self.parameterAsBool(params, self.DISPLAY_HELP, context))
            if self.DISPLAY_HELP in params
            else False
        )
        self.prefs.update(
            {"use_second_layer": bool(use_second), "display_help": display_help}
        )
        self.save_preferences()
        self.logger.info(f"Preferência use_second_layer salva: {use_second}")

        feedback.pushInfo("✔ Processo concluído: linhas geradas com sucesso.")

        self.logger.debug("processAlgorithm concluído")
        return {self.OUTPUT: dest_id}
