# -*- coding: utf-8 -*-
import os
import tempfile
from qgis.core import QgsVectorLayer, QgsDistanceArea, QgsProject
from qgis.PyQt.QtCore import QVariant
from .BaseTask import BaseTask
from ..config.LogUtils import LogUtils


class LineFieldsTask(BaseTask):
    """
    Task assíncrona para calcular comprimento de linhas.

    Esta implementação é "compute-only" e NÃO modifica a camada diretamente.
    Ela retorna um dicionário com o formato:
      { 'updates': { fid: { field_name: value, ... }, ... }, 'missing_fields': [field_name, ...] }
    O Step correspondente aplica as mudanças no thread principal.
    """

    def __init__(self, *, layer, field_map, precision: int = 4, tool_key: str, tmp_dir: str = None):
        super().__init__("Calculando comprimento de linhas", tool_key)
        self.layer = layer
        self.field_map = field_map
        self.precision = precision

        LogUtils.log(
            f"LineFieldsTask.__init__: layer={layer.name()}, modes={list(field_map.keys())}",
            level="DEBUG",
            tool=self.tool_key,
            class_name=self.__class__.__name__
        )

    def _run(self) -> bool:
        if self.isCanceled():
            return False

        LogUtils.log(
            f"LineFieldsTask._run: START - computing line lengths (worker)",
            level="INFO",
            tool=self.tool_key,
            class_name=self.__class__.__name__
        )

        updates = {}
        count = 0
        computed = 0

        d = QgsDistanceArea()
        d.setSourceCrs(self.layer.crs(), QgsProject.instance().transformContext())
        ell = self.layer.crs().ellipsoidAcronym() or "WGS84"
        d.setEllipsoid(ell)

        for feat in self.layer.getFeatures():
            if self.isCanceled():
                LogUtils.log(
                    "LineFieldsTask: cancelado durante cálculo",
                    level="INFO",
                    tool=self.tool_key,
                    class_name=self.__class__.__name__
                )
                return False

            count += 1
            geom = feat.geometry()
            if geom and not geom.isEmpty():
                vals = {}
                if "Elipsoidal" in self.field_map:
                    length_m = d.measureLength(geom)
                    vals[self.field_map["Elipsoidal"]] = round(length_m, self.precision)
                if "Cartesiana" in self.field_map:
                    vals[self.field_map["Cartesiana"]] = round(geom.length(), self.precision)

                if vals:
                    updates[feat.id()] = vals
                    computed += 1

            if count % 5000 == 0:
                LogUtils.log(
                    f"LineFieldsTask: PROGRESS - scanned {count} features, computed {computed}",
                    level="DEBUG",
                    tool=self.tool_key,
                    class_name=self.__class__.__name__
                )

        LogUtils.log(
            f"LineFieldsTask._run: FINISHED - computed={computed} / scanned={count}",
            level="INFO",
            tool=self.tool_key,
            class_name=self.__class__.__name__
        )

        self.result = {
            "updates": updates,
            "missing_fields": [
                fname for fname in set(self.field_map.values())
                if fname not in [f.name() for f in self.layer.fields()]
            ]
        }
        return True
