# -*- coding: utf-8 -*-
import os
import shutil
from datetime import datetime
from pathlib import Path
from qgis.core import QgsProject, QgsMapLayer, QgsVectorLayer
from qgis.PyQt.QtWidgets import QApplication
from ..utils.log_utils import LogUtils
from pathlib import Path
import gc




class ProjectUtils:
    """
    Utilitários relacionados ao projeto QGIS (.qgz).
    Não possui dependência de UI.
    """

    @staticmethod
    def is_project_saved(project: QgsProject) -> bool:
        return bool(project.fileName())

    @staticmethod
    def get_project_dir(project: QgsProject) -> str:
        """
        Retorna diretório do projeto salvo ou homePath como fallback.
        """
        if project.fileName():
            return str(Path(project.fileName()).parent)
        return project.homePath() or os.path.expanduser("~")

    @staticmethod
    def create_project_backup(project: QgsProject) -> str:
        """
        Cria backup do .qgz em subpasta 'backup'.
        Retorna caminho do arquivo criado.
        Lança exceção se projeto não estiver salvo.
        """
        project_file = project.fileName()
        if not project_file:
            raise RuntimeError("Projeto não está salvo. Backup impossível.")

        project_path = Path(project_file)
        project_dir = project_path.parent

        backup_folder = project_dir / "backup"
        backup_folder.mkdir(exist_ok=True)

        ts = datetime.now().strftime("%Y%m%d%H%M%S")
        base_name = project_path.stem[:100]
        backup_name = f"{base_name}_{ts}{project_path.suffix}"

        backup_path = backup_folder / backup_name
        shutil.copy2(project_file, backup_path)

        return str(backup_path)
    
    
    @staticmethod
    def is_layer_in_project(layer: QgsMapLayer) -> bool:
        """
        Verifica se a camada informada está presente no projeto QGIS aberto.

        :param layer: QgsMapLayer selecionada (ex: cmb_layers.currentLayer())
        :return: True se estiver no projeto, False caso contrário
        """
        try:
            if layer is None:
                return False

            project = QgsProject.instance()
            return layer.id() in project.mapLayers()

        except Exception as e:
            LogUtils.log("project_utils", f"Erro ao verificar camada no projeto: {e}")
            return False

    @staticmethod
    def remove_layer_from_project(layer: QgsMapLayer) -> bool:
        """
        Remove a camada informada do projeto QGIS aberto.

        :param layer: QgsMapLayer a ser removida
        :return: True se removida com sucesso, False em erro
        """
        try:
            if layer is None:
                return False

            project = QgsProject.instance()

            if layer.id() not in project.mapLayers():
                return False

            project.removeMapLayer(layer.id())
            return True

        except Exception as e:
            LogUtils.log("project_utils", f"Erro ao remover camada do projeto: {e}")
            return False
    @staticmethod
    def is_file_in_project(file_path: str) -> bool:
        """
        Verifica se existe uma camada no projeto cujo source corresponde ao arquivo informado.
        """
        try:
            if not file_path:
                return False

            target = Path(file_path).resolve()

            for layer in QgsProject.instance().mapLayers().values():
                source = layer.source()

                if not source:
                    continue

                # Normaliza o path da layer (remove |layername= etc)
                layer_path = source.split("|")[0]

                if Path(layer_path).resolve() == target:
                    return True

            return False

        except Exception as e:
            LogUtils.log("project_utils", f"Erro ao verificar arquivo no projeto: {e}")
            return False
    @staticmethod
    def remove_file_from_project(file_path: str) -> bool:
        """
        Remove do projeto a camada cujo source corresponde ao arquivo informado.
        """
        try:
            if not file_path:
                return False

            target = Path(file_path).resolve()
            project = QgsProject.instance()

            for layer_id, layer in project.mapLayers().items():
                source = layer.source()
                if not source:
                    continue

                layer_path = source.split("|")[0]

                if Path(layer_path).resolve() == target:
                    project.removeMapLayer(layer_id)
                    return True

            return False

        except Exception as e:
            LogUtils.log("project_utils", f"Erro ao remover arquivo do projeto: {e}")
            return False

    @staticmethod
    def remove_file_from_project_hard(file_path: str) -> bool:
        """
        Remove a camada do projeto e tenta liberar completamente o datasource
        (incluindo OGR), reduzindo ao máximo locks de arquivo.
        """
        if not file_path:
            return False

        target = Path(file_path).resolve()
        project = QgsProject.instance()

        layer_to_remove = None
        layer_id = None

        # 1. localizar camada
        for lid, layer in project.mapLayers().items():
            if not isinstance(layer, QgsVectorLayer):
                continue

            source = layer.source()
            if not source:
                continue

            layer_path = Path(source.split("|")[0]).resolve()
            if layer_path == target:
                layer_to_remove = layer
                layer_id = lid
                break

        if layer_to_remove is None:
            return False

        try:
            # 2. garantir que não está em edição
            if layer_to_remove.isEditable():
                # rollback força o provider a soltar locks
                layer_to_remove.rollBack()

            # 3. remover do projeto
            project.removeMapLayer(layer_id)

            # 4. quebrar referências explícitas
            layer_to_remove = None

            # 5. processar eventos Qt (Windows é sensível a isso)
            QApplication.processEvents()

            # 6. forçar coleta de lixo
            gc.collect()

            return True

        except Exception as e:
            LogUtils.log(
                "project_utils",
                f"Erro ao remover camada e liberar datasource: {e}"
            )
            return False











