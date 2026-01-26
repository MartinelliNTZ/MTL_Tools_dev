from pathlib import Path
from qgis.core import (
            QgsVectorFileWriter,
            QgsProject,
            QgsVectorLayer,
            QgsCoordinateReferenceSystem,
            QgsCoordinateTransform,
            QgsFeature,
            QgsGeometry, 
            QgsPointXY,  
            QgsWkbTypes,
            QgsFeatureRequest,
            QgsField
        )
from qgis.core import (
    QgsVectorLayer,
    QgsVectorFileWriter,
    QgsProject,
    QgsCoordinateTransformContext
)
from pathlib import Path
from ...utils.log_utils import LogUtilsOld
from ...utils.string_utils import StringUtils
import os
from typing import Optional
import processing
class VectorLayerGeometry:
    """
    Responsável pelas transformações geométricas de camadas vetoriais.
    
    Escopo:
    - Aplicar operações geométricas (buffer, dissolve, merge, explode)
    - Transformar geometrias (simplificar, suavizar, validar)
    - Operações topológicas (union, intersection, difference)
    - Alterar estrutura geométrica das feições
    - Converter entre tipos de geometria
    
    Responsabilidade Principal:
    - Orquestrar transformações que ALTERAM as geometrias
    - Garantir validade após transformações
    - Manter coerência topológica
    
    NÃO é Responsabilidade:
    - Ler ou calcular métricas (use VectorLayerMetrics)
    - Reprojetar (use VectorLayerProjection)
    - Manipular atributos (use VectorLayerAttributes)
    - Carregar ou salvar (use VectorLayerSource)
    """

    def create_buffer_geometry(        
             *,
        layer: QgsVectorLayer,
        distance: float,
        output_path: Optional[str] = None,
        segments: int = 5,
        end_cap_style: int = 1,
        join_style: int = 1,
        miter_limit: float = 2.0,
        dissolve: bool = False,
        external_tool_key="untraceable"        
    ) -> Optional[QgsVectorLayer]:
        """Cria buffer ao redor das geometrias com distância e número de segmentos especificados."""
        if VectorLayerGeometry.get_layer_type(layer) not in (
            QgsWkbTypes.PointGeometry,QgsWkbTypes.LineGeometry,QgsWkbTypes.PolygonGeometry
        ):
            return None

        params = {
            'INPUT': layer,
            'DISTANCE': distance,
            'SEGMENTS': segments,
            'END_CAP_STYLE': end_cap_style,
            'JOIN_STYLE': join_style,
            'MITER_LIMIT': miter_limit,
            'DISSOLVE': dissolve,
            'OUTPUT': output_path or 'memory:'
        }

        result = processing.run(
            'native:buffer',
            params,            
        )

        return result.get('OUTPUT')

    def dissolve_geometries_by_attribute(self, layer, dissolve_field, external_tool_key="untraceable"):
        """Dissolve geometrias agrupadas por um atributo específico."""
        pass

    def merge_geometries(self, geometries_list, external_tool_key="untraceable"):
        """Combina múltiplas geometrias em uma única geometria multipart."""
        pass

    def explode_multipart_features(        *, 
                                   layer: QgsVectorLayer,
                                external_tool_key="untraceable"
    ) -> Optional[QgsVectorLayer]:
        """Explode feições multipart em feições simples."""

        if VectorLayerGeometry.get_layer_type(layer) == QgsWkbTypes.LineGeometry:
            result = processing.run(
                'native:explodelines',
                {
                    'INPUT': layer,
                    'OUTPUT': 'memory:'
                },
            
            )

            return result.get('OUTPUT')
        return None # poligons e point a implementar

    def simplify_geometry(self, layer, tolerance, external_tool_key="untraceable"):
        """Simplifica geometrias reduzindo vértices mantendo forma geral."""
        pass

    def smooth_geometry(self, layer, smoothing_iterations, external_tool_key="untraceable"):
        """Suaviza geometrias através de algoritmo iterativo."""
        pass

    def validate_geometry(self, geometry, external_tool_key="untraceable"):
        """Verifica se uma geometria é válida e sem problemas topológicos."""
        pass

    def fix_invalid_geometry(self, geometry, external_tool_key="untraceable"):
        """Tenta corrigir automaticamente uma geometria inválida."""
        pass

    def get_geometry_intersection(self, geometry1, geometry2, external_tool_key="untraceable"):
        """Calcula a interseção entre duas geometrias."""
        pass

    def get_geometry_union(self, geometry1, geometry2, external_tool_key="untraceable"):
        """Calcula a união entre duas geometrias."""
        pass
    @staticmethod
    def get_layer_type(layer: QgsVectorLayer) -> Optional[str]:
        """Retorna o tipo de geometria da camada vetorial.
        Args:
            layer (QgsVectorLayer): A camada vetorial a ser verificada.
            Returns:QgsWkbTypes.PointGeometry, 
            QgsWkbTypes.LineGeometry, 
            QgsWkbTypes.PolygonGeometry ou None
            """
        if not isinstance(layer, QgsVectorLayer):
            return None

        geom_type = layer.geometryType()

        if geom_type == QgsWkbTypes.PointGeometry:
            return QgsWkbTypes.PointGeometry
        if geom_type == QgsWkbTypes.LineGeometry:
            return QgsWkbTypes.LineGeometry
        if geom_type == QgsWkbTypes.PolygonGeometry:
            return QgsWkbTypes.PolygonGeometry

        return None

    @staticmethod
    def get_selected_features( layer: QgsVectorLayer):
            """
            Retorno:
                (QgsVectorLayer, None) em caso de sucesso
                (None, str) em caso de erro
            """

            if not isinstance(layer, QgsVectorLayer):
                return None, "Layer inválido"

            fids = layer.selectedFeatureIds()
            if not fids:
                return None, "Nenhuma feição selecionada na camada."

            request = QgsFeatureRequest().setFilterFids(fids)

            mem_layer = layer.materialize(request)
            if not mem_layer or not mem_layer.isValid():
                return None, "Falha ao materializar feições selecionadas."

            return mem_layer, None


    def get_geometry_difference(self, geometry1, geometry2, external_tool_key="untraceable"):
        """Calcula a diferença entre duas geometrias."""
        pass

    def convert_geometry_type(self, layer, target_type, external_tool_key="untraceable"):
        """Converte geometrias para um tipo diferente quando possível."""
        pass
    @staticmethod
    def singleparts_to_multparts(layer, feedback=None, only_selected=False):
        """
        Separa feições MULTIPART em feições simples (explode multipart)
        - mesma camada
        - respeita seleção
        """

        if not isinstance(layer, QgsVectorLayer):
            return False

        if not QgsWkbTypes.isMultiType(layer.wkbType()):
            # camada não é multipart
            return True

        # 🔀 decide fonte das feições
        if only_selected and layer.selectedFeatureCount() > 0:
            feats = list(layer.selectedFeatures())
        else:
            feats = list(layer.getFeatures())

        total = len(feats)

        new_features = []
        ids_to_delete = []

        for i, feat in enumerate(feats):

            if feedback and feedback.isCanceled():
                return False

            geom = feat.geometry()
            if not geom or geom.isEmpty():
                continue

            if not geom.isMultipart():
                continue

            parts = geom.constGet()

            for part in parts:
                new_feat = QgsFeature(layer.fields())
                new_feat.setAttributes(feat.attributes())
                new_feat.setGeometry(QgsGeometry(part.clone()))
                new_features.append(new_feat)

            ids_to_delete.append(feat.id())

            if feedback:
                feedback.setProgress(int((i + 1) / total * 100))

        # 🔥 Remove multipart
        if ids_to_delete:
            layer.deleteFeatures(ids_to_delete)

        # ➕ Adiciona singleparts
        if new_features:
            layer.addFeatures(new_features)

        layer.updateExtents()
        return True
