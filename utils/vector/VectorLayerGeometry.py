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
from ...utils.string_utils import StringUtils
from ...core.config.LogUtils import LogUtils
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
        LogUtils.log(f"create_buffer_geometry: distance={distance}, segments={segments}, dissolve={dissolve}", level="DEBUG", tool=external_tool_key, class_name="VectorLayerGeometry")
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
    @staticmethod
    def explode_lines_to_path(
        *,
        input_path: str,
        output_path: str,
        external_tool_key="untraceable"
    ) -> str:
        """
        Explode linhas usando arquivos físicos.
        Seguro para grandes volumes.
        """
        LogUtils.log(f"explode_lines_to_path: {input_path} -> {output_path}", level="INFO", tool=external_tool_key, class_name="VectorLayerGeometry")
        if not input_path or not output_path:
            raise ValueError("input_path e output_path são obrigatórios")

        params = {
            "INPUT": input_path,
            "OUTPUT": output_path
        }

        processing.run("native:explodelines", params)

        LogUtils.log("explode_lines_to_path completed", level="INFO", tool=external_tool_key, class_name="VectorLayerGeometry")
        return output_path

    @staticmethod
    def explode_lines_to_path_safe(
        *,
        layer: QgsVectorLayer,
        output_path: str,
        external_tool_key="untraceable"
    ) -> str:
        """
        Explode linhas (LineString / MultiLineString) manualmente.
        Thread-safe. Compatível com QgsTask.
        """
        LogUtils.log(f"explode_lines_to_path_safe start -> output: {output_path}", level="INFO", tool=external_tool_key, class_name="VectorLayerGeometry")
        if not layer or not layer.isValid():
            LogUtils.log("Camada inválida para explode_lines_to_path_safe", level="CRITICAL", tool=external_tool_key, class_name="VectorLayerGeometry")
            raise ValueError("Camada inválida")

        if layer.geometryType() != QgsWkbTypes.LineGeometry:
            LogUtils.log("Camada não é do tipo linha em explode_lines_to_path_safe", level="CRITICAL", tool=external_tool_key, class_name="VectorLayerGeometry")
            raise ValueError("Camada não é do tipo linha")

        options = QgsVectorFileWriter.SaveVectorOptions()
        options.driverName = "GPKG"
        options.fileEncoding = "UTF-8"
        options.layerName = Path(output_path).stem
        options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteFile

        transform_context = QgsProject.instance().transformContext()

        writer = QgsVectorFileWriter.create(
            output_path,
            layer.fields(),
            QgsWkbTypes.LineString,
            layer.crs(),
            transform_context,
            options
        )

        if writer.hasError() != QgsVectorFileWriter.NoError:
            LogUtils.log(f"Erro ao criar writer: {writer.errorMessage()}", level="CRITICAL", tool=external_tool_key, class_name="VectorLayerGeometry")
            raise RuntimeError(writer.errorMessage())

        LogUtils.log("Writer criado com sucesso para explode_lines_to_path_safe", level="DEBUG", tool=external_tool_key, class_name="VectorLayerGeometry")

        feat_out = QgsFeature(layer.fields())

        processed = 0
        for feat in layer.getFeatures():
            geom = feat.geometry()
            if not geom or geom.isEmpty():
                continue

            if geom.isMultipart():
                parts = geom.asMultiPolyline()
            else:
                parts = [geom.asPolyline()]

            for part in parts:
                if len(part) < 2:
                    continue

                for i in range(len(part) - 1):
                    line = QgsGeometry.fromPolylineXY([part[i], part[i + 1]])
                    feat_out.setAttributes(feat.attributes())
                    feat_out.setGeometry(line)
                    writer.addFeature(feat_out)
                    processed += 1

        del writer
        LogUtils.log(f"explode_lines_to_path_safe completed, processed features (approx): {processed}", level="INFO", tool=external_tool_key, class_name="VectorLayerGeometry")
        return output_path


    @staticmethod
    def get_layer_type(layer: QgsVectorLayer) -> Optional[str]:
        LogUtils.log("get_layer_type called", level="DEBUG", tool="untraceable", class_name="VectorLayerGeometry")
        if not isinstance(layer, QgsVectorLayer):
            return None

        geom_type = layer.geometryType()

        if geom_type == QgsWkbTypes.PointGeometry:
            LogUtils.log("get_layer_type: PointGeometry", level="INFO", tool="untraceable", class_name="VectorLayerGeometry")
            return QgsWkbTypes.PointGeometry
        if geom_type == QgsWkbTypes.LineGeometry:
            LogUtils.log("get_layer_type: LineGeometry", level="INFO", tool="untraceable", class_name="VectorLayerGeometry")
            return QgsWkbTypes.LineGeometry
        if geom_type == QgsWkbTypes.PolygonGeometry:
            LogUtils.log("get_layer_type: PolygonGeometry", level="INFO", tool="untraceable", class_name="VectorLayerGeometry")
            return QgsWkbTypes.PolygonGeometry

        return None

    @staticmethod
    def get_selected_features( layer: QgsVectorLayer):
            LogUtils.log("get_selected_features called", level="DEBUG", tool="untraceable", class_name="VectorLayerGeometry")
            if not isinstance(layer, QgsVectorLayer):
                return None, "Layer inválido"

            fids = layer.selectedFeatureIds()
            if not fids:
                LogUtils.log("Nenhuma feição selecionada na camada", level="INFO", tool="untraceable", class_name="VectorLayerGeometry")
                return None, "Nenhuma feição selecionada na camada."

            request = QgsFeatureRequest().setFilterFids(fids)

            mem_layer = layer.materialize(request)
            if not mem_layer or not mem_layer.isValid():
                LogUtils.log("Falha ao materializar feições selecionadas", level="CRITICAL", tool="untraceable", class_name="VectorLayerGeometry")
                return None, "Falha ao materializar feições selecionadas."

            LogUtils.log(f"get_selected_features: {len(fids)} features", level="INFO", tool="untraceable", class_name="VectorLayerGeometry")
            return mem_layer, None

    @staticmethod
    def singleparts_to_multparts(layer, feedback=None, only_selected=False):
        LogUtils.log("singleparts_to_multparts start", level="DEBUG", tool="untraceable", class_name="VectorLayerGeometry")
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
        LogUtils.log(f"singleparts_to_multparts: total features to process {total}", level="INFO", tool="untraceable", class_name="VectorLayerGeometry")
        new_features = []
        ids_to_delete = []

        for i, feat in enumerate(feats):

            if feedback and feedback.isCanceled():
                LogUtils.log("singleparts_to_multparts canceled by feedback", level="INFO", tool="untraceable", class_name="VectorLayerGeometry")
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
            LogUtils.log(f"singleparts_to_multparts added {len(new_features)} features and removed {len(ids_to_delete)}", level="INFO", tool="untraceable", class_name="VectorLayerGeometry")
        return True


    def get_geometry_difference(self, geometry1, geometry2, external_tool_key="untraceable"):
        """Calcula a diferença entre duas geometrias."""
        pass

    def convert_geometry_type(self, layer, target_type, external_tool_key="untraceable"):
        """Converte geometrias para um tipo diferente quando possível."""
        pass
    
    
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
    
    def dissolve_geometries_by_attribute(self, layer, dissolve_field, external_tool_key="untraceable"):
        """Dissolve geometrias agrupadas por um atributo específico."""
        pass

    def merge_geometries(self, geometries_list, external_tool_key="untraceable"):
        """Combina múltiplas geometrias em uma única geometria multipart."""
        pass