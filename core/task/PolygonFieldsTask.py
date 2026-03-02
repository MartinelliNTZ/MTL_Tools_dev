# -*- coding: utf-8 -*-
import os
import tempfile
from qgis.core import QgsVectorLayer, QgsField, QgsDistanceArea, QgsProject
from qgis.PyQt.QtCore import QVariant
from .BaseTask import BaseTask
from ...utils.vector.VectorLayerSource import VectorLayerSource
from ..config.LogUtils import LogUtils


class PolygonFieldsTask(BaseTask):
    """
    Task assíncrona para calcular área de polígonos.
    
    Modifica o arquivo original (sem criar cópias):
    1. Abre layer em modo edição
    2. Adiciona campos se necessário
    3. Calcula áreas no arquivo original
    4. Commita mudanças (salva direto no arquivo)
    
    Resultado: on_success() apenas confirma (microsegundos, não trava UI)
    """

    def __init__(self, *, layer, field_map, precision: int = 4, tool_key: str, tmp_dir: str = None):
        super().__init__("Calculando área de polígonos", tool_key)
        self.layer = layer
        self.field_map = field_map
        self.precision = precision
        
        LogUtils.log(
            f"PolygonFieldsTask.__init__: layer={layer.name()}, modes={list(field_map.keys())}",
            level="DEBUG",
            tool=self.tool_key,
            class_name=self.__class__.__name__
        )

    def _run(self) -> bool:
        if self.isCanceled():
            return False

        LogUtils.log(
            f"PolygonFieldsTask._run: START - calculando áreas no arquivo original",
            level="INFO",
            tool=self.tool_key,
            class_name=self.__class__.__name__
        )
        
        # New approach: do not modify the layer in the worker thread.
        # Compute a mapping of feature id -> { field_name: value }
        updates = {}
        missing_fields = set()

        count = 0
        computed = 0
        for feat in self.layer.getFeatures():
            if self.isCanceled():
                LogUtils.log(
                    "PolygonFieldsTask: cancelado durante cálculo",
                    level="INFO",
                    tool=self.tool_key,
                    class_name=self.__class__.__name__
                )
                return False

            count += 1
            geom = feat.geometry()
            if geom and not geom.isEmpty():
                vals = {}
                # Elipsoidal
                if "Elipsoidal" in self.field_map:
                    d = QgsDistanceArea()
                    d.setSourceCrs(
                        self.layer.crs(),
                        QgsProject.instance().transformContext()
                    )
                    ell = self.layer.crs().ellipsoidAcronym() or "WGS84"
                    d.setEllipsoid(ell)
                    area_m2 = d.measureArea(geom)
                    vals[self.field_map["Elipsoidal"]] = round(area_m2 / 10000.0, self.precision)
                # Cartesiana
                if "Cartesiana" in self.field_map:
                    area_m2 = geom.area()
                    vals[self.field_map["Cartesiana"]] = round(area_m2 / 10000.0, self.precision)

                if vals:
                    updates[feat.id()] = vals
                    computed += 1

            if count % 5000 == 0:
                LogUtils.log(
                    f"PolygonFieldsTask: PROGRESS - {count} features scanned, {computed} computed",
                    level="DEBUG",
                    tool=self.tool_key,
                    class_name=self.__class__.__name__
                )

        LogUtils.log(
            f"PolygonFieldsTask._run: CONCLUÍDO - computed={computed} / scanned={count}",
            level="INFO",
            tool=self.tool_key,
            class_name=self.__class__.__name__
        )

        # Return structured result for on_success to apply on main thread
        self.result = {
            "updates": updates,
            "missing_fields": [fname for fname in set(self.field_map.values()) if fname not in [f.name() for f in self.layer.fields()]]
        }
        return True

