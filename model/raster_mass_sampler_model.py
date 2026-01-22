# -*- coding: utf-8 -*-
import os
from PyQt5.QtCore import QVariant
from qgis.core import (
    QgsFields, QgsField, QgsFeature, QgsCoordinateTransform
)

class RasterMassSamplerModel:
    """
    Lógica reutilizável da amostragem massiva.
    NÃO depende de QgsProcessingAlgorithm.
    """

    def process(self, pts, rasters, context, feedback, forced_input_crs=None):
        """
        :param pts: source de pontos
        :param rasters: lista de QGIS raster layers
        :param context: QgsProcessingContext
        :param feedback: feedback
        :param forced_input_crs: CRS forçado opcional
        :return: (out_fields, lista_features)
        """

        # CRS de entrada real
        effective_pts_crs = forced_input_crs if forced_input_crs else pts.sourceCrs()

        # Campos baseados nos pontos
        out_fields = QgsFields()
        for f in pts.fields():
            out_fields.append(f)

        raster_fields = []
        for ras in rasters:
            name = os.path.splitext(ras.name())[0][:10]
            raster_fields.append(name)
            out_fields.append(QgsField(name, QVariant.Double))

        feedback.pushInfo(f"[DEBUG] Campos criados: {raster_fields}")

        # Transforms CRS
        transforms = []
        for ras in rasters:
            transforms.append(
                QgsCoordinateTransform(
                    effective_pts_crs,
                    ras.crs(),
                    context.transformContext()
                )
            )

        # Execução
        result_features = []

        for feat in pts.getFeatures():
            geom = feat.geometry()
            if geom is None:
                continue

            out_feat = QgsFeature(out_fields)
            out_feat.setGeometry(geom)
            attrs = feat.attributes()

            for i, ras in enumerate(rasters):
                pt = transforms[i].transform(geom.asPoint())
                val = ras.dataProvider().sample(pt, 1)[0]

                feedback.pushInfo(
                    f"[DEBUG] Ponto {feat.id()}, Raster {ras.name()} = {val}"
                )

                attrs.append(float(val) if val is not None else None)

            out_feat.setAttributes(attrs)
            result_features.append(out_feat)

        feedback.pushInfo("[DEBUG] Lógica finalizada.")

        return out_fields, result_features
