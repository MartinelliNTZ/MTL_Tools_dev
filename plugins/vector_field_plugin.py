# -*- coding: utf-8 -*-
from qgis.PyQt.QtWidgets import QAction
from qgis.core import QgsVectorLayer, QgsWkbTypes, QgsApplication
import os

from ..utils.vector.VectorLayerAttributes import VectorLayerAttributes
from ..utils.vector.VectorLayerMetrics import VectorLayerMetrics
from ..utils.vector.VectorLayerProjection import VectorLayerProjection
from ..utils.altimetry_task import AltimetriaTask
from ..utils.qgis_messagem_util import QgisMessageUtil
from ..utils.crs_utils import get_coord_info
from ..utils.tool_keys import ToolKey
from .BasePlugin import BasePluginMTL


class VectorFieldPlugin(BasePluginMTL):
    

    def __init__(self, iface):
        self.iface = iface
        self.actions = []
        # Inicializar plugin sem UI, mas com carregamento de settings
        self.init(
            tool_key=ToolKey.VECTOR_FIELDS,
            class_name="VectorFieldPlugin",
            build_ui=False,
            load_settings_prefs=True
        )

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
    # HELPERS
    # --------------------------------------------------
    def _resolve_calculation_mode(self, layer, requested_mode):
        """
        Resolve o modo de cálculo com validações automáticas.
        Se CRS geográfico + modo Cartesiana, muda para Ambos automaticamente.
        
        Returns
        -------
        tuple
            (modo_final: str, foi_alterado: bool)
            Exemplo: ('Ambos', True) ou ('Elipsoidal', False)
        """
        if requested_mode != "Cartesiana":
            return requested_mode, False
        
        if not VectorLayerProjection.is_geographic_crs(layer):
            return requested_mode, False
        
        # CRS geográfico + modo Cartesiana = problema
        self.logger.warning(
            f"CRS geográfico detectado com modo Cartesiano. Mudando para Ambos."
        )
        
        warning_msg = (
            f"⚠️ Camada usa CRS Geográfico ({layer.crs().authid()})\n\n"
            f"Modo 'Cartesiano' resultaria em valores em graus² (inválido).\n\n"
            f"Calculando AMBOS os modos automaticamente para referência."
        )
        QgisMessageUtil.bar_warning(self.iface, warning_msg)
        
        return "Ambos", True

    # --------------------------------------------------
    # CONTROLLER
    # --------------------------------------------------
    def run_vector_field(self):
        self.logger.info("Iniciando Calcular Campos Vetoriais")
        
        layer = self.get_active_vector_layer(require_editable=True)
        if not layer:
            self.logger.warning("Nenhuma camada vetorial editável disponível")
            return

        self.logger.debug(f"Camada selecionada: {layer.name()}")
        geom_type = layer.geometryType()
        self.logger.debug(f"Tipo de geometria: {geom_type}")

        handlers = {
            QgsWkbTypes.PointGeometry: self._run_point_fields,
            QgsWkbTypes.LineGeometry: self._run_line_fields,
            QgsWkbTypes.PolygonGeometry: self._run_polygon_fields,
        }

        handler = handlers.get(geom_type)
        if not handler:
            self.logger.error(f"Tipo de geometria não suportado: {geom_type}")
            QgisMessageUtil.bar_warning(
                self.iface,
                "Tipo de geometria não suportado"
            )
            return

        try:
            handler(layer)
            self.logger.info("Calcular Campos Vetoriais finalizado com sucesso")
        except Exception as e:
            self.logger.error(f"Erro ao executar handler: {str(e)}")
            QgisMessageUtil.bar_critical(
                self.iface,
                f"Erro ao calcular campos:\n{str(e)}"
            )
        
    def resolve_field_name(self, layer, base_name):
        """Resolve conflito de nome de campo"""
        self.logger.debug(f"Resolvendo nome de campo: {base_name}")
        
        if layer.fields().lookupField(base_name) == -1:
            self.logger.debug(f"Campo '{base_name}' disponível")
            return base_name

        action = QgisMessageUtil.ask_field_conflict(self.iface, base_name)
        self.logger.debug(f"Ação do usuário para conflito: {action}")

        if action == "cancel":
            self.logger.debug("Usuário cancelou operação")
            return None

        if action == "replace":
            return base_name
        
        i = 1
        while layer.fields().lookupField(f"{base_name}_{i}") != -1:
            i += 1

        new_name = f"{base_name}_{i}"
        self.logger.debug(f"Campo renomeado para: {new_name}")
        return new_name


    def _run_polygon_fields(self, layer):
        """Calcula área para polígonos"""
        self.logger.info("Iniciando cálculo de área para polígonos")
        
        requested_mode = self.settings_preferences.get('calculation_method', 'Elipsoidal')
        calculation_mode, mode_altered = self._resolve_calculation_mode(layer, requested_mode)
        self.logger.debug(f"Modo de cálculo final: {calculation_mode}, foi alterado: {mode_altered}")
        
        field_map = VectorLayerAttributes.resolve_field_names_for_calculation(
            layer, "area", calculation_mode
        )
        self.logger.debug(f"Mapa de campos para polígonos: {field_map}")
        
        # Resolver conflitos de nomes para cada modo
        resolved_fields = {}
        for mode, base_field in field_map.items():
            resolved = self.resolve_field_name(layer, base_field)
            if not resolved:
                self.logger.warning(f"Cálculo de área para {mode} cancelado")
                return
            resolved_fields[mode] = resolved

        try:
            # Criar campos
            self.logger.debug(f"Criando campos: {list(resolved_fields.values())}")
            VectorLayerAttributes.create_point_coordinate_fields(layer, resolved_fields)
            
            # Calcular área elipsoidal
            if "Elipsoidal" in resolved_fields:
                self.logger.debug(f"Calculando área ELIPSOIDAL no campo: {resolved_fields['Elipsoidal']}")
                VectorLayerMetrics.calculate_polygon_area(layer, resolved_fields["Elipsoidal"], use_ellipsoidal=True)
            
            # Calcular área cartesiana
            if "Cartesiana" in resolved_fields:
                self.logger.debug(f"Calculando área CARTESIANA no campo: {resolved_fields['Cartesiana']}")
                VectorLayerMetrics.calculate_polygon_area(layer, resolved_fields["Cartesiana"], use_ellipsoidal=False)
            
            self.logger.info(f"Área calculada com sucesso: {list(resolved_fields.values())}")
            
            # Exibir mensagem de sucesso apenas se o modo NÃO foi alterado
            if not mode_altered:
                QgisMessageUtil.bar_success(self.iface, "Área calculada")
        except Exception as e:
            self.logger.error(f"Erro ao calcular área: {str(e)}")
            raise
        
    def _run_line_fields(self, layer):
        """Calcula comprimento para linhas"""
        self.logger.info("Iniciando cálculo de comprimento para linhas")
        
        requested_mode = self.settings_preferences.get('calculation_method', 'Elipsoidal')
        calculation_mode, mode_altered = self._resolve_calculation_mode(layer, requested_mode)
        self.logger.debug(f"Modo de cálculo final: {calculation_mode}, foi alterado: {mode_altered}")
        
        field_map = VectorLayerAttributes.resolve_field_names_for_calculation(
            layer, "length", calculation_mode
        )
        self.logger.debug(f"Mapa de campos para linhas: {field_map}")
        
        # Resolver conflitos de nomes para cada modo
        resolved_fields = {}
        for mode, base_field in field_map.items():
            resolved = self.resolve_field_name(layer, base_field)
            if not resolved:
                self.logger.warning(f"Cálculo de comprimento para {mode} cancelado")
                return
            resolved_fields[mode] = resolved

        try:
            # Criar campos
            self.logger.debug(f"Criando campos: {list(resolved_fields.values())}")
            VectorLayerAttributes.create_point_coordinate_fields(layer, resolved_fields)
            
            # Calcular comprimento elipsoidal
            if "Elipsoidal" in resolved_fields:
                self.logger.debug(f"Calculando comprimento ELIPSOIDAL no campo: {resolved_fields['Elipsoidal']}")
                VectorLayerMetrics.calculate_line_length(layer, resolved_fields["Elipsoidal"], use_ellipsoidal=True)
            
            # Calcular comprimento cartesiano
            if "Cartesiana" in resolved_fields:
                self.logger.debug(f"Calculando comprimento CARTESIANO no campo: {resolved_fields['Cartesiana']}")
                VectorLayerMetrics.calculate_line_length(layer, resolved_fields["Cartesiana"], use_ellipsoidal=False)
            
            self.logger.info(f"Comprimento calculado com sucesso: {list(resolved_fields.values())}")
            
            # Exibir mensagem de sucesso apenas se o modo NÃO foi alterado
            if not mode_altered:
                QgisMessageUtil.bar_success(self.iface, "Comprimento calculado")
        except Exception as e:
            self.logger.error(f"Erro ao calcular comprimento: {str(e)}")
            raise
            
    def _run_point_fields(self, layer):
        """Calcula coordenadas X, Y (e opcionalmente Z) para pontos"""
        self.logger.info("Iniciando cálculo de coordenadas para pontos")
        
        include_z = QgisMessageUtil.confirm(
            self.iface,
            "Deseja adicionar Z (Altimetria)?"
        )
        self.logger.debug(f"Altimetria incluída: {include_z}")

        field_map = {}
        bases = ["x", "y"] + (["z"] if include_z else [])

        for base in bases:
            name = self.resolve_field_name(layer, base)
            if not name:
                self.logger.warning(f"Campo {base} cancelado pelo usuário")
                return
            field_map[base] = name

        try:
            self.logger.debug(f"Mapa de campos: {field_map}")
            
            # Criar campos
            self.logger.debug("Criando campos de coordenadas")
            VectorLayerAttributes.create_point_coordinate_fields(layer, field_map)
            
            # Atualizar X, Y
            self.logger.debug("Atualizando coordenadas X, Y")
            VectorLayerAttributes.update_point_xy_coordinates(layer, field_map)
            
            self.logger.info("Campos X/Y calculados com sucesso")
            QgisMessageUtil.bar_success(self.iface, "Campos X/Y calculados")

            if not include_z:
                return

            """    # Processar Z (altimetria)
            total = layer.featureCount()
            self.logger.info(f"Iniciando cálculo de altimetria para {total} feições")
            
            if total > 5000:
                self.logger.warning(f"Camada com {total} feições > 5000: Z será ignorado")
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
                        self.logger.debug(f"Altimetria recebida para {len(z_results)} feições")
                        VectorLayerAttributes.update_feature_values(layer, z_results, field_map["z"])
                        self.logger.info("X, Y e Z calculados com sucesso")
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
                QgsApplication.taskManager().addTask(task)"""
                
        except Exception as e:
            self.logger.error(f"Erro ao calcular coordenadas: {str(e)}")
            raise
