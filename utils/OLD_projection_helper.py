# -*- coding: utf-8 -*-
from qgis.core import (
    QgsCoordinateTransform,
    QgsFeature,
    QgsFields,
    QgsGeometry
)

class ProjectionHelper:
    """
    Classe utilitária para reprojetar features entre CRS diferentes.
    Reutilizável em qualquer ferramenta.
    """

    def reproject_features(self, features, source_crs, target_crs, context):
        """
        :param features: lista de QgsFeature
        :param source_crs: QgsCoordinateReferenceSystem
        :param target_crs: QgsCoordinateReferenceSystem
        :param context: QgsProcessingContext
        :return: nova lista de features reprojetadas
        """
        if not target_crs.isValid():
            return features  # Sem reprojeção

        transform = QgsCoordinateTransform(source_crs, target_crs, context.transformContext())
        reproj = []

        for feat in features:
            new_feat = QgsFeature(feat)
            geom = feat.geometry()

            if geom is not None:
                new_geom = QgsGeometry(geom)
                new_geom.transform(transform)
                new_feat.setGeometry(new_geom)

            reproj.append(new_feat)

        return reproj
