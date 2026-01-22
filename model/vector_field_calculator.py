# -*- coding: utf-8 -*-
from qgis.core import QgsVectorLayer, QgsField, QgsWkbTypes, QgsDistanceArea, QgsProject

from qgis.PyQt.QtCore import QVariant


class VectorFieldCalculator:
    """
    MODEL PURO
    - Não acessa iface
    - Não cria task
    - Não exibe mensagens
    - Apenas cria campos e calcula valores
    """

    def __init__(self, layer: QgsVectorLayer):
        self.layer = layer

    # --------------------------------------------------
    # Utils
    # --------------------------------------------------
    def field_exists(self, name: str) -> bool:
        return self.layer.fields().lookupField(name) != -1

    # --------------------------------------------------
    # POINT
    # --------------------------------------------------
    def create_point_fields(self, field_map: dict):
        """
        field_map = {"x": "x", "y": "y", "z": "z_1"}
        """
        self.layer.startEditing()

        for name in field_map.values():
            self.layer.addAttribute(
                QgsField(name, QVariant.Double, len=20, prec=8)
            )

        self.layer.updateFields()

    def update_point_xy(self, field_map: dict):
        for feat in self.layer.getFeatures():
            geom = feat.geometry()
            if geom.isEmpty():
                continue

            p = geom.asPoint()
            feat[field_map["x"]] = round(p.x(), 8)
            feat[field_map["y"]] = round(p.y(), 8)
            self.layer.updateFeature(feat)

    def update_point_z(self, z_values: dict, z_field: str):
        for fid, z in z_values.items():
            if z is not None:
                feat = self.layer.getFeature(fid)
                feat[z_field] = z
                self.layer.updateFeature(feat)

    # --------------------------------------------------
    # LINE
    # --------------------------------------------------
    def calculate_line_length(self, field_name: str):
        self.layer.startEditing()

        self.layer.addAttribute(
            QgsField(field_name, QVariant.Double, len=16, prec=4)
        )
        self.layer.updateFields()

        # -----------------------------------------
        # CONFIGURA MEDIDOR ELIPSOIDAL
        # -----------------------------------------
        d = QgsDistanceArea()
        d.setSourceCrs(
            self.layer.crs(),
            QgsProject.instance().transformContext()
        )

        ellipsoid = self.layer.crs().ellipsoidAcronym()
        if not ellipsoid:
            ellipsoid = "WGS84"

        d.setEllipsoid(ellipsoid)

        # -----------------------------------------
        # CÁLCULO DE COMPRIMENTO (METROS)
        # -----------------------------------------
        for feat in self.layer.getFeatures():
            geom = feat.geometry()
            if geom and not geom.isEmpty():
                length_m = d.measureLength(geom)  # 👈 ELIPSOIDAL
                feat[field_name] = round(length_m, 4)
                self.layer.updateFeature(feat)

        #self.layer.commitChanges()
    # --------------------------------------------------
    # POLYGON
    # --------------------------------------------------

    def calculate_polygon_area(self, field_name: str):
        self.layer.startEditing()

        self.layer.addAttribute(
            QgsField(field_name, QVariant.Double, len=16, prec=4)
        )
        self.layer.updateFields()

        # -----------------------------------------
        # CONFIGURA MEDIDOR ELIPSOIDAL
        # -----------------------------------------
        d = QgsDistanceArea()
        d.setSourceCrs(
            self.layer.crs(),
            QgsProject.instance().transformContext()
        )

        # usa o elipsóide definido no CRS (ex: SIRGAS / WGS84)
        ellipsoid = self.layer.crs().ellipsoidAcronym()
        if not ellipsoid:
            ellipsoid = "WGS84"

        d.setEllipsoid(ellipsoid)
       # d.setEllipsoidalMode(True)

        # -----------------------------------------
        # CÁLCULO DE ÁREA (m² → hectares)
        # -----------------------------------------
        for feat in self.layer.getFeatures():
            geom = feat.geometry()
            if geom and not geom.isEmpty():
                area_m2 = d.measureArea(geom)
                area_ha = area_m2 / 10000.0
                feat[field_name] = round(area_ha, 4)
                self.layer.updateFeature(feat)

        #self.layer.commitChanges()

