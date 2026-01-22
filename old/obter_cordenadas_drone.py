import os
import re
from qgis.core import (
    QgsVectorLayer,
    QgsFeature,
    QgsGeometry,
    QgsPointXY,
    QgsField,
    QgsProject
)
from PyQt5.QtCore import QVariant

BASE_DIR = r"D:\MINERADORA CODEMIN\INPUT"

# -----------------------------
# REGEX
# -----------------------------

# Nome do MRK
name_pattern = re.compile(
    r"DJI_(\d{8})(\d{4})_(\d+)_voo(.+)\.mrk",
    re.IGNORECASE
)

# Linha MRK
line_pattern = re.compile(
    r"^\s*(\d+).*?(-?\d+\.\d+),Lat\s+(-?\d+\.\d+),Lon\s+(\d+\.\d+),Ellh"
)

points = []

# -----------------------------
# VARREDURA MRK
# -----------------------------
for root, _, files in os.walk(BASE_DIR):
    for file in files:
        if file.lower().endswith(".mrk"):
            m_name = name_pattern.match(file)
            if not m_name:
                continue

            data, hora, voo, projeto = m_name.groups()
            projeto = projeto.strip()

            path = os.path.join(root, file)

            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    m = line_pattern.search(line)
                    if m:
                        foto = int(m.group(1))
                        lat = float(m.group(2))
                        lon = float(m.group(3))
                        alt = float(m.group(4))

                        points.append(
                            (foto, lon, lat, alt, data, hora, voo, projeto)
                        )

# -----------------------------
# CAMADA DE PONTOS (MEMORY)
# -----------------------------
vl_points = QgsVectorLayer("Point?crs=EPSG:4326", "photos_points", "memory")
prov = vl_points.dataProvider()

prov.addAttributes([
    QgsField("foto", QVariant.Int),
    QgsField("data", QVariant.String),
    QgsField("hora", QVariant.String),
    QgsField("voo", QVariant.String),
    QgsField("projeto", QVariant.String),
    QgsField("alt", QVariant.Double)
])

vl_points.updateFields()

for foto, lon, lat, alt, data, hora, voo, projeto in points:
    feat = QgsFeature(vl_points.fields())
    feat.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(lon, lat)))
    feat.setAttributes([foto, data, hora, voo, projeto, alt])
    prov.addFeature(feat)

vl_points.updateExtents()
QgsProject.instance().addMapLayer(vl_points)

# -----------------------------
# CAMADA DE TRAJETO (MEMORY)
# -----------------------------
vl_line = QgsVectorLayer("LineString?crs=EPSG:4326", "drone_track", "memory")
prov_l = vl_line.dataProvider()

line_geom = QgsGeometry.fromPolylineXY(
    [QgsPointXY(lon, lat) for _, lon, lat, *_ in points]
)

feat_line = QgsFeature()
feat_line.setGeometry(line_geom)
prov_l.addFeature(feat_line)

vl_line.updateExtents()
QgsProject.instance().addMapLayer(vl_line)
