# -*- coding: utf-8 -*-

from typing import Optional

from qgis.core import (
    QgsVectorLayer,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsProject,
    QgsUnitTypes,
    QgsFeature,
    QgsGeometry
)


class VectorLayerProjection:
    """
    Responsável por:

    - CRS
    - Conversão de unidades
    - Reprojeção

    NÃO salva camada.
    NÃO valida regra de negócio.
    NÃO altera atributos.
    """

    # ---------------------------------------------------------
    # CONVERSÃO DE DISTÂNCIA
    # ---------------------------------------------------------
    @staticmethod
    def convert_distance_to_layer_units(
        layer: QgsVectorLayer,
        distance_meters: float
    ) -> float:
        """
        Converte uma distância em METROS
        para a unidade da camada.

        Dialog nunca deve saber se é grau, metro ou pé.
        """

        if not layer or not layer.isValid():
            return distance_meters

        crs = layer.crs()
        unit = crs.mapUnits()

        # Se já estiver em metros
        if unit == QgsUnitTypes.DistanceMeters:
            return distance_meters

        # Se estiver em graus (ex: EPSG:4326)
        if unit == QgsUnitTypes.DistanceDegrees:
            # Conversão média aproximada
            # 1 grau ≈ 111320 metros
            return distance_meters / 111320.0

        # Outras unidades (feet, etc.)
        factor = QgsUnitTypes.fromUnitToUnitFactor(
            QgsUnitTypes.DistanceMeters,
            unit
        )

        return distance_meters * factor

    # ---------------------------------------------------------
    # REPROJEÇÃO EM MEMÓRIA
    # ---------------------------------------------------------
    @staticmethod
    def reproject_layer(
        layer: QgsVectorLayer,
        target_crs: QgsCoordinateReferenceSystem
    ) -> Optional[QgsVectorLayer]:
        """
        Cria uma nova camada em memória reprojetada.
        """

        if not layer or not layer.isValid():
            return None

        if not target_crs or not target_crs.isValid():
            return None

        source_crs = layer.crs()

        if source_crs == target_crs:
            return layer

        uri = f"{layer.wkbType()}?crs={target_crs.authid()}"
        new_layer = QgsVectorLayer(uri, f"{layer.name()}_reprojected", "memory")

        provider = new_layer.dataProvider()
        provider.addAttributes(layer.fields())
        new_layer.updateFields()

        transform = QgsCoordinateTransform(
            source_crs,
            target_crs,
            QgsProject.instance().transformContext()
        )

        feats = []

        for feat in layer.getFeatures():
            new_feat = QgsFeature(layer.fields())
            new_feat.setAttributes(feat.attributes())

            geom = feat.geometry()
            if geom and not geom.isEmpty():
                geom = QgsGeometry(geom)
                geom.transform(transform)
                new_feat.setGeometry(geom)

            feats.append(new_feat)

        provider.addFeatures(feats)
        new_layer.updateExtents()

        return new_layer

    # ---------------------------------------------------------
    # GARANTIR CRS ESPECÍFICO
    # ---------------------------------------------------------
    @staticmethod
    def ensure_crs(
        layer: QgsVectorLayer,
        target_crs: QgsCoordinateReferenceSystem
    ) -> Optional[QgsVectorLayer]:
        """
        Garante que a camada esteja no CRS desejado.
        Se já estiver, retorna ela mesma.
        Caso contrário, reprojeta.
        """

        if not layer or not layer.isValid():
            return None

        if layer.crs() == target_crs:
            return layer

        return VectorLayerProjection.reproject_layer(layer, target_crs)
    def get_layer_crs(self, layer, external_tool_key="untraceable"):
        """Obtém o CRS atual da camada."""
        pass

    def set_layer_crs(self, layer, target_crs, external_tool_key="untraceable"):
        """Define o CRS da camada sem reprojetar (apenas muda a definição)."""
        pass
    def validate_crs_compatibility(self, layer1, layer2, external_tool_key="untraceable"):
        """Verifica se duas camadas possuem CRS compatíveis ou próximos."""
        pass

    def get_layer_unit_type(self, layer, external_tool_key="untraceable"):
        """Obtém o tipo de unidade de medida do CRS da camada (metros, graus, etc)."""
        pass

    def convert_distance_unit(self, distance_value, from_unit, to_unit, external_tool_key="untraceable"):
        """Converte um valor de distância entre diferentes unidades de medida."""
        pass

    def convert_area_unit(self, area_value, from_unit, to_unit, external_tool_key="untraceable"):
        """Converte um valor de área entre diferentes unidades de medida."""
        pass

    def get_layer_extent_in_different_crs(self, layer, target_crs, external_tool_key="untraceable"):
        """Calcula a extensão da camada quando projetada em um CRS diferente."""
        pass

    def check_layer_is_geographic_crs(self, layer, external_tool_key="untraceable"):
        """Verifica se a camada usa sistema de coordenadas geográficas (lat/lon)."""
        pass

    def check_layer_is_projected_crs(self, layer, external_tool_key="untraceable"):
        """Verifica se a camada usa sistema de coordenadas projetado."""
        pass

    def get_crs_axis_order(self, crs, external_tool_key="untraceable"):
        """Obtém a ordem de eixos do CRS (XY ou YX)."""
        pass

    def list_common_crs_for_region(self, region_code, external_tool_key="untraceable"):
        """Lista os CRS mais comuns e apropriados para uma região geográfica."""
        pass
