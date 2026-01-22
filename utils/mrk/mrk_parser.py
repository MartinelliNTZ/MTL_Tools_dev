# -*- coding: utf-8 -*-
import os
import re

from qgis.core import (
    QgsVectorLayer, QgsFeature, QgsGeometry,
    QgsPointXY, QgsField, QgsFields
)
from PyQt5.QtCore import QVariant


class MrkParser:

    LINE_RE = re.compile(
        r"(?P<foto>\d+).*?"
        r"(?P<lat>-?\d+\.\d+),Lat.*?"
        r"(?P<lon>-?\d+\.\d+),Lon.*?"
        r"(?P<alt>-?\d+(\.\d+)?),Ellh",
        re.IGNORECASE
    )

    @staticmethod
    def parse_folder(folder, recursive=True, extra_fields=None):
        points = []

        for root, _, files in os.walk(folder):
            for f in files:
                if not f.lower().endswith(".mrk"):
                    continue

                with open(os.path.join(root, f), "r",
                          encoding="utf-8", errors="ignore") as fh:
                    for line in fh:
                        m = MrkParser.LINE_RE.search(line)
                        if not m:
                            continue
                        data_mrk = None
                       
                        # extrai data do nome do MRK: DJI_YYYYMMDDHHMM_...
                        m_date = re.search(r"DJI_(\d{8})", f)
                        if m_date:
                            data_mrk = m_date.group(1)

                        points.append({
                            "foto": int(m.group("foto")),
                            "lat": float(m.group("lat")),
                            "lon": float(m.group("lon")),
                            "alt": float(m.group("alt")),
                            "data_name": data_mrk,
                            "folder": root
                        })


            if not recursive:
                break

        return points

    @staticmethod
    def to_point_layer(points, name="MRK_Pontos", extra_fields=None):

        fields = QgsFields()
        fields.append(QgsField("foto", QVariant.Int))
        fields.append(QgsField("alt", QVariant.Double))
        fields.append(QgsField("data_name", QVariant.String))

        if extra_fields:
            for field_name, qtype in extra_fields.items():
                fields.append(QgsField(field_name, qtype))
                
            




        vl = QgsVectorLayer(
            "Point?crs=EPSG:4326", name, "memory"
        )
        vl.dataProvider().addAttributes(fields)
        vl.updateFields()


        vl.startEditing()

        for p in points:
            f = QgsFeature(vl.fields())
            f.setGeometry(QgsGeometry.fromPointXY(
                QgsPointXY(p["lon"], p["lat"])
            ))
            attrs = [
                p.get("foto"),
                p.get("alt"),
                p.get("data_name")
            ]

            if extra_fields:
                for name in extra_fields.keys():
                    attrs.append(p.get(name))

                        
            #attrs.append(p.get("data_name"))


            f.setAttributes(attrs)
            vl.addFeature(f)

        vl.commitChanges()
        vl.updateExtents()
        return vl

