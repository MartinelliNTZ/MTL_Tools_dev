# -*- coding: utf-8 -*-
import os
import tempfile
from qgis.core import QgsVectorLayer, QgsField, QgsProject
from qgis.PyQt.QtCore import QVariant
from .BaseTask import BaseTask
from ...utils.vector.VectorLayerAttributes import VectorLayerAttributes
from ...utils.vector.VectorLayerSource import VectorLayerSource
from ..config.LogUtils import LogUtils


class PointFieldsTask(BaseTask):
    """
    Task assíncrona para calcular campos X e Y.
    
    Modifica o arquivo original (sem criar cópias):
    1. Abre layer em modo edição
    2. Adiciona campos X e Y se não existem
    3. Calcula coordenadas no arquivo original
    4. Commita mudanças (salva direto no arquivo)
    
    Resultado: on_success() apenas confirma (microsegundos, não trava UI)
    """

    def __init__(self, *, layer, field_map, tool_key: str, tmp_dir: str = None):
        super().__init__("Calculando campos de pontos", tool_key)
        self.layer = layer
        self.field_map = field_map
        
        LogUtils.log(
            f"PointFieldsTask.__init__: layer={layer.name()}",
            level="DEBUG",
            tool=self.tool_key,
            class_name=self.__class__.__name__
        )

    def _run(self) -> bool:
        if self.isCanceled():
            return False

        LogUtils.log(
            "PointFieldsTask._run: START - computing point coordinates (worker)",
            level="INFO",
            tool=self.tool_key,
            class_name=self.__class__.__name__
        )

        updates = {}
        count = 0
        computed = 0
        const_prec = 8

        for feat in self.layer.getFeatures():
            if self.isCanceled():
                LogUtils.log(
                    "PointFieldsTask: cancelado durante cálculo",
                    level="INFO",
                    tool=self.tool_key,
                    class_name=self.__class__.__name__
                )
                return False

            count += 1
            geom = feat.geometry()
            if geom and not geom.isEmpty():
                p = geom.asPoint()
                vals = {}
                if "x" in self.field_map:
                    vals[self.field_map["x"]] = round(p.x(), const_prec)
                if "y" in self.field_map:
                    vals[self.field_map["y"]] = round(p.y(), const_prec)

                if vals:
                    updates[feat.id()] = vals
                    computed += 1

            if count % 5000 == 0:
                LogUtils.log(
                    f"PointFieldsTask: PROGRESS - scanned {count} features, computed {computed}",
                    level="DEBUG",
                    tool=self.tool_key,
                    class_name=self.__class__.__name__
                )

        LogUtils.log(
            f"PointFieldsTask._run: CONCLUÍDO - computed={computed} / scanned={count}",
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

