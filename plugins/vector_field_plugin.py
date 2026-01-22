# -*- coding: utf-8 -*-
from qgis.PyQt.QtWidgets import QAction
from qgis.core import QgsVectorLayer, QgsWkbTypes, QgsApplication
import os

from ..model.vector_field_calculator import VectorFieldCalculator
from ..utils.altimetry_task import AltimetriaTask
from ..utils.qgis_messagem_util import QgisMessageUtil
from ..utils.crs_utils import get_coord_info
from .base_plugin import BasePluginMTL


class VectorFieldPlugin(BasePluginMTL):
    

    def __init__(self, iface):
        self.iface = iface
        self.actions = []

    def initGui(self):
        self.create_action(
            "../resources/icons/vector_field.png",
            "Calcular Campos Vetoriais",
            self.run_vector_field
        )
    
    

    def unload(self):
        for a in self.actions:
            self.iface.removePluginMenu("MTL Tools", a)

    # --------------------------------------------------
    # CONTROLLER
    # --------------------------------------------------
    def run_vector_field(self):
        layer = self.get_active_vector_layer(require_editable=True)
        if not layer:
            return

        calc = VectorFieldCalculator(layer)

        handlers = {
            QgsWkbTypes.PointGeometry: self._run_point_fields,
            QgsWkbTypes.LineGeometry: self._run_line_fields,
            QgsWkbTypes.PolygonGeometry: self._run_polygon_fields,
        }

        handler = handlers.get(layer.geometryType())
        if not handler:
            QgisMessageUtil.bar_warning(
                self.iface,
                "Tipo de geometria não suportado"
            )
            return

        handler(layer, calc)
        
    def resolve_field_name(self, layer, base_name):
        if layer.fields().lookupField(base_name) == -1:
            return base_name

        action = QgisMessageUtil.ask_field_conflict(self.iface, base_name)

        if action == "cancel":
            return None

        if action == "replace":
            return base_name
        
        i = 1
        while layer.fields().lookupField(f"{base_name}_{i}") != -1:
            i += 1

        return f"{base_name}_{i}"


    def _run_polygon_fields(self, layer, calc):
        field = self.resolve_field_name(layer, "area")
        if not field:
            return

        calc.calculate_polygon_area(field)
        QgisMessageUtil.bar_success(self.iface, "Área calculada")
        
    def _run_line_fields(self, layer, calc):
        field = self.resolve_field_name(layer, "length")
        if not field:
            return

        calc.calculate_line_length(field)
        QgisMessageUtil.bar_success(self.iface, "Comprimento calculado")
    def _run_point_fields(self, layer, calc):
        include_z = QgisMessageUtil.confirm(
            self.iface,
            "Deseja adicionar Z (Altimetria)?"
        )

        field_map = {}
        bases = ["x", "y"] + (["z"] if include_z else [])

        for base in bases:
            name = self.resolve_field_name(layer, base)
            if not name:
                return
            field_map[base] = name

        calc.create_point_fields(field_map)
        calc.update_point_xy(field_map)

        if not include_z:
            QgisMessageUtil.bar_success(self.iface, "Campos X/Y calculados")
            return

        total = layer.featureCount()
        if total > 5000:
            QgisMessageUtil.bar_warning(
                self.iface,
                "Mais de 5000 feições: Z ignorado"
            )
            return

        z_results = {}
        pending = total

        def make_callback(fid):
            def cb(value, error):
                nonlocal pending
                if not error:
                    z_results[fid] = round(value, 8)
                pending -= 1

                if pending == 0:
                    calc.update_point_z(z_results, field_map["z"])
                    QgisMessageUtil.bar_success(
                        self.iface,
                        "X, Y e Z calculados com sucesso"
                    )
            return cb

        for feat in layer.getFeatures():
            p = feat.geometry().asPoint()
            info = get_coord_info(p, layer.crs())

            task = AltimetriaTask(
                info["lat"],
                info["lon"],
                make_callback(feat.id())
            )
            QgsApplication.taskManager().addTask(task)
