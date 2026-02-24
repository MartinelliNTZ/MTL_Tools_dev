from pathlib import Path
from qgis.core import (
            QgsVectorFileWriter,
            QgsProject,
            QgsVectorLayer,
            QgsWkbTypes,
            QgsFeatureRequest,
            QgsVectorLayer,
        QgsVectorFileWriter,
        QgsProject,
        )
from typing import Optional, Tuple 
import os
import tempfile 
import time
from ...utils.string_utils import StringUtils
from ...utils.project_utils import ProjectUtils
from ...core.config.LogUtils import LogUtils
class VectorLayerSource:
    """
    Responsável pela entrada, saída e origem de camadas vetoriais.
    
    Escopo:
    - Carregar camadas vetoriais de diferentes fontes
    - Salvar camadas em diferentes formatos
    - Validar integridade de camadas
    - Clonar camadas existentes
    - Gerenciar origem de dados (arquivo, banco, memória)
    
    Responsabilidade Principal:
    - Orquestrar operações de I/O de camadas vetoriais
    - Garantir que camadas sejam carregadas e salvas corretamente
    - Validar antes de operações críticas
    
    NÃO é Responsabilidade:
    - Reprojetar camadas (use VectorLayerProjection)
    - Calcular geometria ou métricas (use VectorLayerGeometry/VectorLayerMetrics)
    - Manipular atributos (use VectorLayerAttributes)
    - Renderizar ou exibir dados
    """

    @staticmethod
    def save_vector_layer_to_file(
        layer: QgsVectorLayer,
        output_path,
        decision="rename",
        external_tool_key="untraceable"
    ):
        class_name = "VectorLayerSource"

        LogUtils.log(
            f"Iniciando salvamento da camada: {layer.name() if layer else 'None'}",
            level="INFO",
            tool=external_tool_key,
            class_name=class_name
        )

        if not layer or not layer.isValid():
            LogUtils.log(
                "Camada inválida",
                level="CRITICAL",
                tool=external_tool_key,
                class_name=class_name
            )
            return None

        ext = os.path.splitext(output_path)[1].lower()
        driver = StringUtils.VECTOR_DRIVERS.get(ext)

        if not driver:
            LogUtils.log(
                f"Formato não suportado: {ext}",
                level="CRITICAL",
                tool=external_tool_key,
                class_name=class_name
            )
            return None

        # garante que a pasta existe
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir, exist_ok=True)
            except Exception as e:
                LogUtils.log(
                    f"Falha ao criar diretório: {e}",
                    level="CRITICAL",
                    tool=external_tool_key,
                    class_name=class_name
                )
                return None

        final_path = output_path

        # =====================
        # RENAME
        # =====================
        if decision == "rename" and os.path.exists(output_path):
            final_path = VectorLayerSource.generate_incremental_path(output_path)
            LogUtils.log(
                f"Arquivo já existe, novo nome: {final_path}",
                level="INFO",
                tool=external_tool_key,
                class_name=class_name
            )

        # =====================
        # OVERWRITE
        # =====================
        elif decision == "overwrite" and os.path.exists(output_path):

            if ProjectUtils.is_layer_in_project(layer):
                LogUtils.log(
                    "Camada está no projeto, removendo para liberar lock",
                    level="WARNING",
                    tool=external_tool_key,
                    class_name=class_name
                )
                ProjectUtils.remove_layer_from_project(layer)

            if ext == ".shp":
                if not VectorLayerSource.delete_shapefile_set(output_path):
                    LogUtils.log(
                        "Falha ao remover arquivos do Shapefile",
                        level="CRITICAL",
                        tool=external_tool_key,
                        class_name=class_name
                    )
                    return None
            else:
                try:
                    os.remove(output_path)
                except Exception as e:
                    LogUtils.log(
                        f"Erro ao remover arquivo existente: {e}",
                        level="CRITICAL",
                        tool=external_tool_key,
                        class_name=class_name
                    )
                    return None

        # =====================
        # SALVAMENTO
        # =====================
        LogUtils.log(
            f"Salvando arquivo em: {final_path}",
            level="INFO",
            tool=external_tool_key,
            class_name=class_name
        )

        options = QgsVectorFileWriter.SaveVectorOptions()
        options.driverName = driver
        options.fileEncoding = "UTF-8"

        # AQUI ESTAVA O ERRO CRÍTICO
        if ext == ".gpkg":
            LogUtils.log(
                f"Extensão é GeoPackage, aplicando opções específicas. {ext}",
                level="INFO",
                tool=external_tool_key,
                class_name=class_name
            )

            layer_name = layer.name() or Path(final_path).stem
            #layer_name = layer_name.replace(" ", "_")
            options.layerName = layer_name

            if os.path.exists(final_path):
                options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteLayer
                LogUtils.log(
                    f"GPKG existente | sobrescrevendo camada: {layer_name}",
                    level="DEBUG",
                    tool=external_tool_key,
                    class_name=class_name
                )
            else:
                options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteFile
                LogUtils.log(
                    f"GPKG não existe | criando arquivo e camada: {layer_name}",
                    level="DEBUG",
                    tool=external_tool_key,
                    class_name=class_name
                )
        else:
            options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteFile



        transform_context = QgsProject.instance().transformContext()

        result, error_message = QgsVectorFileWriter.writeAsVectorFormatV2(
            layer,
            final_path,
            transform_context,
            options
        )

        if result != QgsVectorFileWriter.NoError:
            LogUtils.log(
                f"Erro ao salvar camada | Código={result} | Msg={error_message}",
                level="CRITICAL",
                tool=external_tool_key,
                class_name=class_name
            )
            return None

        LogUtils.log(
            "Camada salva com sucesso",
            level="INFO",
            tool=external_tool_key,
            class_name=class_name
        )

        return final_path  
    
    # ------------------------------------------------------------------
    # SALVAMENTO CENTRALIZADO
    # ------------------------------------------------------------------
    @staticmethod
    def save_layer(
        layer: QgsVectorLayer,
        *,
        output_path: Optional[str],
        save_to_folder: bool,
        output_name: str,
        decision: Optional[str] = None,
        external_tool_key: str = "untraceable"
    ) -> Optional[QgsVectorLayer]:

        if not layer or not layer.isValid():
            return None

        final_layer = layer.materialize(QgsFeatureRequest())
        layer = None  # libera memória

        # -------------------------------------------------
        # salvar em disco
        # -------------------------------------------------
        if save_to_folder:

            saved_path = VectorLayerSource.save_vector_layer_to_file(
                layer=final_layer,
                output_path=output_path,
                decision=decision or "rename",
                external_tool_key=external_tool_key
            )

            if not saved_path:
                return None

            final_layer = QgsVectorLayer(
                saved_path,
                Path(saved_path).stem,
                "ogr"
            )

            if not final_layer.isValid():
                return None

        # -------------------------------------------------
        # adicionar ao projeto
        # -------------------------------------------------
        if save_to_folder:
            output_name = Path(output_path).stem

        final_layer.setName(output_name)
        #QgsProject.instance().addMapLayer(final_layer)

        return final_layer

    @staticmethod
    def export_temp_layer(
        layer: QgsVectorLayer,
        prefix: str = "tmp_layer",
        external_tool_key: str = "untraceable"
    ) -> Optional[str]:

        if not layer or not layer.isValid():
            return None

        tmp_dir = tempfile.mkdtemp(prefix=prefix)
        output_path = os.path.join(tmp_dir, f"{prefix}.gpkg")

        return VectorLayerSource.save_vector_layer_to_file(
            layer=layer,
            output_path=output_path,
            decision="overwrite",
            external_tool_key=external_tool_key
        )

    @staticmethod
    def delete_shapefile_set(base_path, retries=5, delay=0.3):
        """
        base_path = caminho do .shp
        """
        folder = os.path.dirname(base_path)
        base = os.path.splitext(os.path.basename(base_path))[0]

        for attempt in range(retries):
            errors = []
            for ext in StringUtils.SHP_EXTENSIONS:
                f = os.path.join(folder, base + ext)
                if os.path.exists(f):
                    try:
                        os.remove(f)
                    except Exception as e:
                        errors.append((f, str(e)))

            if not errors:
                return True

            time.sleep(delay)

        return False

    @staticmethod
    def generate_incremental_path(path):
        folder = os.path.dirname(path)
        name, ext = os.path.splitext(os.path.basename(path))

        counter = 1
        new_path = path
        while os.path.exists(new_path):
            new_path = os.path.join(folder, f"{name}_{counter}{ext}")
            counter += 1

        return new_path


    # ------------------------------------------------------------------
    # VALIDAÇÃO CENTRALIZADA
    # ------------------------------------------------------------------
    @staticmethod
    def validate_layer(
        layer: QgsVectorLayer,
        *,
        expected_geometry: Optional[int] = None,
        require_editable: bool = False
    ) -> Tuple[bool, Optional[str]]:
        """
        Valida camada vetorial com regras padronizadas.

        Retorna:
            (True, None) se OK
            (False, "mensagem erro") se inválida
        """

        if not layer:
            return False, "Nenhuma camada foi informada."

        if not isinstance(layer, QgsVectorLayer):
            return False, "Objeto informado não é uma camada vetorial."

        if not layer.isValid():
            return False, "Camada inválida."

        if expected_geometry is not None:
            if layer.geometryType() != expected_geometry:
                expected_name = QgsWkbTypes.displayString(expected_geometry)
                current_name = QgsWkbTypes.displayString(layer.geometryType())
                return False, (
                    f"Tipo de geometria inválido.\n"
                    f"Esperado: {expected_name}\n"
                    f"Atual: {current_name}"
                )

        if require_editable and not layer.isEditable():
            return False, "A camada precisa estar em modo de edição."

        return True, None




    def load_vector_layer_from_file(self, file_path, external_tool_key="untraceable"):
        """Carrega uma camada vetorial de um arquivo no disco."""
        pass

    def load_vector_layer_from_database(self, connection_string, layer_name, external_tool_key="untraceable"):
        """Carrega uma camada vetorial de um banco de dados."""
        pass

    def create_memory_layer(self, layer_name, geometry_type, crs, external_tool_key="untraceable"):
        """Cria uma camada vetorial em memória com geometria e CRS especificados."""
        pass


    def save_vector_layer_to_database(self, layer, connection_string, table_name, external_tool_key="untraceable"):
        """Salva uma camada vetorial em um banco de dados."""
        pass

    def clone_vector_layer(self, source_layer, include_features, external_tool_key="untraceable"):
        """Cria uma cópia exata de uma camada vetorial com ou sem feições."""
        pass

    def validate_layer_integrity(self, layer, external_tool_key="untraceable"):
        """Verifica se a camada está válida e íntegra para operações."""
        pass

    def get_layer_source_uri(self, layer, external_tool_key="untraceable"):
        """Obtém a URI ou caminho completo da origem da camada."""
        pass

    def check_file_format_compatibility(self, file_path, target_format, external_tool_key="untraceable"):
        """Verifica se o arquivo pode ser convertido para o formato desejado."""
        pass

    def reload_layer_from_source(self, layer, external_tool_key="untraceable"):
        """Recarrega a camada a partir de sua fonte original."""
        pass

    def export_layer_statistics(self, layer, output_path, external_tool_key="untraceable"):
        """Exporta estatísticas básicas da camada para arquivo de relatório."""
        pass

    def validate_geometry_before_save(self, layer, external_tool_key="untraceable"):
        """Valida geometrias da camada antes de salvar para evitar corrupção."""
        pass
