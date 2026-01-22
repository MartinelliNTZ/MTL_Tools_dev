# -*- coding: utf-8 -*-
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
from ..utils.log_utils import LogUtils
from ..utils.string_utils import StringUtils
import os
from typing import Optional
import processing


class VectorUtils:    
    TYPE_LINE = 'LineString'
    TYPE_POINT = 'Point'    
    TYPE_POLYGON = 'Polygon'

    @staticmethod
    def merge_layers(layers, name="MERGE"):
        if not layers:
            return None

        crs = layers[0].crs().authid()
        out = QgsVectorLayer(
            f"{layers[0].geometryType()}?crs={crs}",
            name, "memory"
        )

        prov = out.dataProvider()
        prov.addAttributes(layers[0].fields())
        out.updateFields()

        out.startEditing()
        for lyr in layers:
            for f in lyr.getFeatures():
                prov.addFeature(f)
        out.commitChanges()
        out.updateExtents()
        return out

    @staticmethod
    def points_to_path(points, name="Trilha"):
        if len(points) < 2:
            return None

        line = QgsVectorLayer(
            "LineString?crs=EPSG:4326", name, "memory"
        )

        geom = QgsGeometry.fromPolylineXY([
            QgsPointXY(p["lon"], p["lat"]) for p in points
        ])

        f = QgsFeature()
        f.setGeometry(geom)
        line.dataProvider().addFeature(f)
        line.updateExtents()
        return line

    @staticmethod
    def save_layer(
        layer: QgsVectorLayer,
        output_path: str,
        toolkey: str = "VectorUtils.save_layer",
        decision: str = "rename"  # "rename" | "overwrite"
    ) -> Optional[str]:
        """
        Salva uma camada vetorial em disco de forma segura.
        - NÃO remove arquivos manualmente
        - Deixa o QgsVectorFileWriter cuidar do overwrite
        - Retorna o caminho salvo (str) ou None em erro
        """

        LogUtils.log(toolkey, f"save_layer chamado → {output_path}. Decision: {decision}. Layer valid: {layer.isValid() if layer else 'None'}. ")

        if not isinstance(layer, QgsVectorLayer) or not output_path:
            LogUtils.log(toolkey, "Layer inválida ou output_path vazio")
            return None

        path = Path(output_path)

        # -------------------------------
        # CONFLITO DE NOME
        # -------------------------------
        if path.exists() and decision == "rename":
            path = VectorUtils._auto_rename(path)
            LogUtils.log(toolkey, f"Arquivo existe. Renomeado para: {path.name}")

        output_path = str(path)

        # -------------------------------
        # DRIVER
        # -------------------------------
        ext = path.suffix.lower()
        driver_map = {
            ".shp": "ESRI Shapefile",
            ".gpkg": "GPKG",
            ".geojson": "GeoJSON",
            ".json": "GeoJSON",
            ".kml": "KML"
        }

        driver = driver_map.get(ext)
        if not driver:
            LogUtils.log(toolkey, f"Extensão não suportada: {ext}")
            return None

        LogUtils.log(toolkey, f"Driver: {driver}")
        LogUtils.log(toolkey, f"CRS: {layer.crs().authid()}")
        LogUtils.log(toolkey, f"Features: {layer.featureCount()}")

        # -------------------------------
        # REPROJEÇÃO AUTOMÁTICA PARA KML
        # -------------------------------
        if driver == "KML" and layer.crs().authid() != "EPSG:4326":
            LogUtils.log(toolkey, "Reprojetando para EPSG:4326")

            target_crs = QgsCoordinateReferenceSystem("EPSG:4326")
            transform = QgsCoordinateTransform(
                layer.crs(),
                target_crs,
                QgsProject.instance()
            )

            mem = QgsVectorLayer(
                f"{layer.geometryType()}?crs=EPSG:4326",
                layer.name(),
                "memory"
            )
            mem.dataProvider().addAttributes(layer.fields())
            mem.updateFields()

            feats = []
            for f in layer.getFeatures():
                nf = QgsFeature(mem.fields())
                nf.setAttributes(f.attributes())
                g = f.geometry()
                g.transform(transform)
                nf.setGeometry(g)
                feats.append(nf)

            mem.dataProvider().addFeatures(feats)
            mem.updateExtents()
            layer = mem

            LogUtils.log(toolkey, "Reprojeção concluída")
                                # Remove dataset físico
            if decision == "overwrite" and (ext == ".shp" or ext == ".gpkg"):
                LogUtils.log(toolkey, "Overwrite solicitado pelo usuário limpando lixo SHP.")                    
                try:
                    VectorUtils._remove_existing_dataset(os.path)
                except Exception as e:
                    LogUtils.log("toolkey", f"Erro ao remover dataset existente: {e}")
                    return None   
    # -------------------------------
        # ESCRITA SEGURA (OVERWRITE REAL)
        # -------------------------------
        options = QgsVectorFileWriter.SaveVectorOptions()
        options.driverName = driver
        options.fileEncoding = "UTF-8"
        options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteFile

        context = QgsProject.instance().transformContext()

        if hasattr(QgsVectorFileWriter, "writeAsVectorFormatV3"):
            LogUtils.log(toolkey, "Usando writeAsVectorFormatV3")
            result = QgsVectorFileWriter.writeAsVectorFormatV3(
                layer,
                output_path,
                context,
                options
            )
        else:
            LogUtils.log(toolkey, "Usando writeAsVectorFormatV2")
            result = QgsVectorFileWriter.writeAsVectorFormatV2(
                layer,
                output_path,
                context,
                options
            )

        if isinstance(result, tuple):
            err_code = result[0]
            err_msg = result[1] if len(result) > 1 else ""
        else:
            err_code = result
            err_msg = ""

        if err_code != QgsVectorFileWriter.NoError:
            LogUtils.log(toolkey, f"ERRO AO SALVAR ({err_code}): {err_msg}")           
            
            return None

        LogUtils.log(toolkey, f"Arquivo salvo com sucesso: {output_path}")
        return output_path


    @staticmethod
    def save_layer_obsolet(
        layer,
        output_path,
        toolkey="VectorUtils.save_layer",
        decision: str = "rename"
    ):
        LogUtils.log(toolkey, f"save_layer chamado → {output_path}")

        if layer is None or not output_path:
            LogUtils.log(toolkey, "Layer ou output_path inválido")
            return None

        path = Path(output_path)

        # -------------------------------
        # TRATAMENTO DE CONFLITO
        # -------------------------------
        if path.exists():

            if decision == "rename":
                new_path = VectorUtils._auto_rename(path)
                LogUtils.log(
                    toolkey,
                    f"Arquivo existe. Renomeando para: {new_path.name}"
                )
                path = new_path

            elif decision == "overwrite":
                LogUtils.log(toolkey, "Arquivo existe. Overwrite solicitado")

                # Remove dataset físico
                try:
                    VectorUtils._remove_existing_dataset(path)
                except Exception as e:
                    LogUtils.log(toolkey, f"Erro ao remover dataset existente: {e}")
                    return None
            else:
                LogUtils.log(toolkey, f"Decision inválida: {decision}")
                return None

        output_path = str(path)

        # -------------------------------
        # DRIVER
        # -------------------------------
        ext = path.suffix.lower()

        driver_map = {
            ".shp": "ESRI Shapefile",
            ".gpkg": "GPKG",
            ".geojson": "GeoJSON",
            ".json": "GeoJSON",
            ".kml": "KML"
        }

        driver = driver_map.get(ext)
        if not driver:
            LogUtils.log(toolkey, f"Extensão não suportada: {ext}")
            return None

        LogUtils.log(toolkey, f"Driver: {driver}")
        LogUtils.log(toolkey, f"CRS: {layer.crs().authid()}")
        LogUtils.log(toolkey, f"Features: {layer.featureCount()}")

        # -------------------------------
        # REPROJEÇÃO REAL PARA KML
        # -------------------------------
        if driver == "KML" and layer.crs().authid() != "EPSG:4326":
            LogUtils.log(toolkey, "Reprojetando para EPSG:4326")

            target_crs = QgsCoordinateReferenceSystem("EPSG:4326")
            transform = QgsCoordinateTransform(
                layer.crs(),
                target_crs,
                QgsProject.instance()
            )

            mem = QgsVectorLayer(
                f"{layer.geometryType()}?crs=EPSG:4326",
                layer.name(),
                "memory"
            )
            mem.dataProvider().addAttributes(layer.fields())
            mem.updateFields()

            feats = []
            for f in layer.getFeatures():
                nf = QgsFeature(mem.fields())
                nf.setAttributes(f.attributes())
                g = f.geometry()
                g.transform(transform)
                nf.setGeometry(g)
                feats.append(nf)

            mem.dataProvider().addFeatures(feats)
            mem.updateExtents()
            layer = mem

            LogUtils.log(toolkey, "Reprojeção concluída")

        # -------------------------------
        # ESCRITA
        # -------------------------------
        options = QgsVectorFileWriter.SaveVectorOptions()
        options.driverName = driver
        options.fileEncoding = "UTF-8"

        context = QgsProject.instance().transformContext()

        # -------------------------------
        # ESCRITA (QGIS 3.16+ SAFE)
        # -------------------------------
        if hasattr(QgsVectorFileWriter, "writeAsVectorFormatV3"):
            LogUtils.log(toolkey, "Usando writeAsVectorFormatV3")
            result = QgsVectorFileWriter.writeAsVectorFormatV3(
                layer,
                output_path,
                context,
                options
            )
        else:
            LogUtils.log(toolkey, "Usando writeAsVectorFormatV2")
            result = QgsVectorFileWriter.writeAsVectorFormatV2(
                layer,
                output_path,
                context,
                options
            )


        if isinstance(result, tuple):
            err_code = result[0]
            err_msg = result[1] if len(result) > 1 else ""
        else:
            err_code = result
            err_msg = ""

        if err_code != QgsVectorFileWriter.NoError:
            LogUtils.log(toolkey, f"ERRO AO SALVAR ({err_code}): {err_msg}")
            return None

        LogUtils.log(toolkey, f"Arquivo salvo com sucesso: {output_path}")

        # -------------------------------
        # RECARREGAMENTO DA LAYER
        # -------------------------------
        saved_layer = QgsVectorLayer(
            output_path,
            path.stem,
            "ogr"
        )

        if not saved_layer.isValid():
            LogUtils.log(toolkey, "Layer salvo é inválido")
            return None

        LogUtils.log(toolkey, "Layer carregado com sucesso")
        return saved_layer 

    @staticmethod
    def _remove_existing_dataset(path: Path):
        """
        Remove dataset existente corretamente.
        - SHP: remove todos os arquivos associados
        - Outros: remove apenas o arquivo
        """

        suffix = path.suffix.lower()

        # SHAPEFILE = múltiplos arquivos
        if suffix == ".shp":
            base = path.with_suffix("")
            for ext in (".shp", ".shx", ".dbf", ".prj", ".cpg", ".qpj"):
                f = base.with_suffix(ext)
                if f.exists():
                    f.unlink()
        else:
            # GPKG, GEOJSON, KML etc
            path.unlink()

    # -------------------------------------------------
    @staticmethod
    def _auto_rename(path: Path) -> Path:
        base = path.stem
        ext = path.suffix
        parent = path.parent

        i = 1
        while True:
            new_path = parent / f"{base}_{i}{ext}"
            if not new_path.exists():
                return new_path
            i += 1

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


    @staticmethod
    def copy_attributes(
        target_layer,
        source_layer,
        field_names=None,
        conflict_resolver=None
    ):
        """
        Copia estrutura de atributos da camada source para target.

        conflict_resolver(field_name) -> "skip" | "rename" | "cancel"
        """

        if not target_layer.isEditable():
            target_layer.startEditing()

        for field in source_layer.fields():

            if field_names and field.name() not in field_names:
                continue

            idx = target_layer.fields().indexOf(field.name())

            # campo não existe
            if idx == -1:
                target_layer.addAttribute(QgsField(
                    field.name(),
                    field.type(),
                    field.typeName(),
                    field.length(),
                    field.precision()
                ))
                continue

            # conflito
            action = "skip"
            if conflict_resolver:
                action = conflict_resolver(field.name())

            if action == "cancel":
                return False

            if action == "rename":
                new_name = VectorUtils._generate_field_name(
                    target_layer, field.name()
                )
                target_layer.addAttribute(QgsField(
                    new_name,
                    field.type(),
                    field.typeName(),
                    field.length(),
                    field.precision()
                ))

        target_layer.updateFields()
        return True

    @staticmethod
    def _generate_field_name(layer, base):
        i = 1
        while layer.fields().indexOf(f"{base}_{i}") != -1:
            i += 1
        return f"{base}_{i}"


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

    @staticmethod
    def explode_lines(
        *,
        layer: QgsVectorLayer,
        feedback=None
    ) -> Optional[QgsVectorLayer]:

        if VectorUtils.get_layer_type(layer) != VectorUtils.TYPE_LINE:
            return None

        result = processing.run(
            'native:explodelines',
            {
                'INPUT': layer,
                'OUTPUT': 'memory:'
            },
            feedback=feedback
        )

        return result.get('OUTPUT')

    
    @staticmethod
    def buffer_layer(
        *,
        layer: QgsVectorLayer,
        distance: float,
        output_path: Optional[str] = None,
        segments: int = 5,
        end_cap_style: int = 1,
        join_style: int = 1,
        miter_limit: float = 2.0,
        dissolve: bool = False,
        feedback=None
    ) -> Optional[QgsVectorLayer]:

        if VectorUtils.get_layer_type(layer) not in (
            VectorUtils.TYPE_LINE,
            VectorUtils.TYPE_POLYGON
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
            feedback=feedback
        )

        return result.get('OUTPUT')

    @staticmethod
    def load_output_layer(
        output,
        name: str
    ) -> Optional[QgsVectorLayer]:

        if isinstance(output, QgsVectorLayer):
            output.setName(name)
            QgsProject.instance().addMapLayer(output)
            return output

        if isinstance(output, str) and os.path.exists(output):
            layer = QgsVectorLayer(output, Path(output).stem, 'ogr')
            if layer.isValid():
                QgsProject.instance().addMapLayer(layer)
                return layer

        if isinstance(output, str) and output.startswith('memory'):
            layer = QgsVectorLayer(output, name, 'memory')
            if layer.isValid():
                QgsProject.instance().addMapLayer(layer)
                return layer

        return None

    @staticmethod
    def get_layer_type(layer: QgsVectorLayer) -> Optional[str]:
        if not isinstance(layer, QgsVectorLayer):
            return None

        geom_type = layer.geometryType()

        if geom_type == QgsWkbTypes.PointGeometry:
            return VectorUtils.TYPE_POINT
        if geom_type == QgsWkbTypes.LineGeometry:
            return VectorUtils.TYPE_LINE
        if geom_type == QgsWkbTypes.PolygonGeometry:
            return VectorUtils.TYPE_POLYGON

        return None

