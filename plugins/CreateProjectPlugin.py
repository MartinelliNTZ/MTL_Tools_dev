# -*- coding: utf-8 -*-
import os
import re
from pathlib import Path

from qgis.PyQt.QtCore import QCoreApplication, QProcess
from qgis.core import (
    QgsCoordinateReferenceSystem,
    QgsProject,
    QgsRasterLayer,
    QgsRectangle,
    QgsVectorLayer,
)

from ..core.config.LogUtils import LogUtils
from ..core.ui.dialogs.DefaultProjectsFolderDialog import DefaultProjectsFolderDialog
from ..core.ui.dialogs.ProjectNameDialog import ProjectNameDialog
from ..i18n.TranslationManager import STR
from ..resources.OtherFilesManager import OtherFilesManager
from ..utils.ExplorerUtils import ExplorerUtils
from ..utils.Preferences import load_tool_prefs, save_tool_prefs
from ..utils.ProjectUtils import ProjectUtils
from ..utils.QgisMessageUtil import QgisMessageUtil
from ..utils.ToolKeys import ToolKey
from ..utils.vector.VectorLayerSource import VectorLayerSource


class CreateProjectPlugin:
    DEFAULT_PROJECTS_FOLDER = "C:/QgisProjects"
    PROJECTS_FOLDER_PREF_KEY = "projects_folder"
    TOOL_KEY = ToolKey.CREATE_PROJECT
    GENERIC_PROJECT_PATTERN = re.compile(r"^NovoProjeto_(\d+)$")
    DEFAULT_CRS_AUTHID = "EPSG:4326"
    DEFAULT_CRS_PREF_KEY = "default_crs_authid"
    GOOGLE_HYBRID_LAYER_NAME = "Google Hybrid"
    GOOGLE_HYBRID_URI = (
        "type=xyz&zmin=0&zmax=21&"
        "url=https://mt1.google.com/vt/lyrs=y%26x=%7Bx%7D%26y=%7By%7D%26z=%7Bz%7D"
    )
    SCENARIO_UNSAVED_WITH_CONTENT = 1
    SCENARIO_SAVED_CURRENT_PROJECT = 2
    SCENARIO_UNSAVED_EMPTY_PROJECT = 3

    def __init__(self, iface):
        self.iface = iface
        self.logger = LogUtils(
            tool=self.TOOL_KEY, class_name="CreateProjectPlugin", level=LogUtils.DEBUG
        )

    def execute(self):
        self.logger.info("Iniciando fluxo de criacao de novo projeto")
        system_prefs = load_tool_prefs(ToolKey.SYSTEM)
        base_folder = self._resolve_base_folder(system_prefs)
        if not base_folder:
            return

        project_name = self._resolve_project_name(base_folder)
        if not project_name:
            return

        default_crs_authid = (
            system_prefs.get(self.DEFAULT_CRS_PREF_KEY) or self.DEFAULT_CRS_AUTHID
        )
        self._create_project_structure(base_folder, project_name, default_crs_authid)

    def _resolve_base_folder(self, system_prefs: dict) -> str:
        base_folder = (system_prefs.get(self.PROJECTS_FOLDER_PREF_KEY) or "").strip()
        if base_folder:
            if self._prepare_existing_base_folder(base_folder):
                return base_folder
            return ""

        base_folder = self._prompt_and_persist_base_folder(system_prefs)
        if not base_folder:
            return ""
        if self._prepare_new_base_folder(base_folder):
            return base_folder
        return ""

    def _prompt_and_persist_base_folder(self, system_prefs: dict) -> str:
        should_define = QgisMessageUtil.confirm(
            self.iface,
            STR.PROJECTS_DEFAULT_FOLDER_MISSING,
            title=STR.PROJECTS_DEFAULT_FOLDER_MISSING_TITLE,
        )
        if not should_define:
            self.logger.info("Usuario cancelou definicao da pasta padrao")
            return ""

        folder_dialog = DefaultProjectsFolderDialog(parent=self.iface.mainWindow())
        if not folder_dialog.exec():
            self.logger.info("Usuario cancelou o dialogo da pasta padrao")
            return ""

        base_folder = folder_dialog.get_folder_path().strip()
        system_prefs[self.PROJECTS_FOLDER_PREF_KEY] = base_folder
        save_tool_prefs(ToolKey.SYSTEM, system_prefs)
        self.logger.info(f"Pasta padrao salva nas system prefs: {base_folder}")
        return base_folder

    def _prepare_new_base_folder(self, base_folder: str) -> bool:
        try:
            os.makedirs(base_folder, exist_ok=True)
            return True
        except Exception as e:
            self.logger.error(f"Erro ao criar pasta padrao '{base_folder}': {e}")
            QgisMessageUtil.modal_error(
                self.iface,
                f"{STR.PROJECT_DEFAULT_FOLDER_PREPARE_ERROR}\n{base_folder}\n\n{e}",
            )
            return False

    def _prepare_existing_base_folder(self, base_folder: str) -> bool:
        try:
            os.makedirs(base_folder, exist_ok=True)
            return True
        except Exception as e:
            self.logger.error(
                f"Erro ao preparar pasta padrao existente '{base_folder}': {e}"
            )
            QgisMessageUtil.modal_error(
                self.iface,
                f"{STR.PROJECT_DEFAULT_FOLDER_ACCESS_ERROR}\n{base_folder}\n\n{e}",
            )
            return False

    def _resolve_project_name(self, base_folder: str) -> str:
        suggested_name = self._next_generic_project_name(base_folder)
        name_dialog = ProjectNameDialog(
            suggested_name=suggested_name, parent=self.iface.mainWindow()
        )
        if not name_dialog.exec():
            self.logger.info("Usuario cancelou o dialogo de nome do projeto")
            return ""

        project_name = self._sanitize_project_name(name_dialog.get_project_name())
        return project_name or suggested_name

    def _sanitize_project_name(self, raw_name: str) -> str:
        cleaned = re.sub(r'[<>:"/\\\\|?*]+', " ", raw_name or "")
        cleaned = re.sub(r"\s+", " ", cleaned).strip().rstrip(".")
        return cleaned

    def _next_generic_project_name(self, base_folder: str) -> str:
        folder = Path(base_folder)
        highest = 0

        if folder.exists():
            for child in folder.iterdir():
                if not child.is_dir():
                    continue
                match = self.GENERIC_PROJECT_PATTERN.match(child.name)
                if match:
                    highest = max(highest, int(match.group(1)))

        return f"NovoProjeto_{highest + 1}"

    def _get_qgis_executable(self) -> str:
        executable = QCoreApplication.applicationFilePath()
        if executable and os.path.exists(executable):
            return executable
        return ""

    def _open_project_in_new_window(
        self, project_file: Path, focus_extent: QgsRectangle = None
    ) -> bool:
        executable = self._get_qgis_executable()
        if not executable:
            self.logger.error("Executavel do QGIS nao encontrado para nova janela")
            return False

        args = []
        if (
            focus_extent is not None
            and hasattr(focus_extent, "isEmpty")
            and not focus_extent.isEmpty()
        ):
            extent_str = (
                f"{focus_extent.xMinimum()},{focus_extent.yMinimum()},"
                f"{focus_extent.xMaximum()},{focus_extent.yMaximum()}"
            )
            args.extend(["--extent", extent_str])
        args.append(str(project_file))

        started = QProcess.startDetached(executable, args)
        if isinstance(started, tuple):
            started = started[0]

        self.logger.debug(
            f"Abertura de nova janela para projeto '{project_file}' "
            f"com args {args}: {started}"
        )
        return bool(started)

    def _add_google_basemap(self, project: QgsProject):
        existing_names = [layer.name() for layer in project.mapLayers().values()]
        if self.GOOGLE_HYBRID_LAYER_NAME in existing_names:
            self.logger.debug("Camada base Google ja existe no projeto; ignorando")
            return

        layer = QgsRasterLayer(
            self.GOOGLE_HYBRID_URI,
            self.GOOGLE_HYBRID_LAYER_NAME,
            "wms",
        )
        if not layer.isValid():
            self.logger.warning("Falha ao criar camada base Google Hybrid (XYZ)")
            return

        project.addMapLayer(layer, True)
        self.logger.info("Camada base Google Hybrid adicionada ao projeto")

    def _detect_creation_scenario(self, current_project: QgsProject) -> int:
        if current_project.fileName():
            return self.SCENARIO_SAVED_CURRENT_PROJECT
        if current_project.mapLayers():
            return self.SCENARIO_UNSAVED_WITH_CONTENT
        return self.SCENARIO_UNSAVED_EMPTY_PROJECT

    def _should_load_line_for_scenario(self, scenario: int) -> bool:
        return scenario in (
            self.SCENARIO_SAVED_CURRENT_PROJECT,
            self.SCENARIO_UNSAVED_EMPTY_PROJECT,
        )

    def _copy_and_load_line_reference_layer(
        self, project: QgsProject, project_vectors_folder: Path
    ):
        line_path = OtherFilesManager.vector_path(OtherFilesManager.LINE_VECTOR)
        if not os.path.exists(line_path):
            self.logger.warning(
                f"Arquivo de referencia nao encontrado para carga automatica: {line_path}"
            )
            return None, ""

        copied_line_path = ExplorerUtils.copy_file_to_folder(
            source_file=line_path,
            destination_folder=str(project_vectors_folder),
            tool_key=self.TOOL_KEY,
            overwrite=True,
        )
        if not copied_line_path:
            self.logger.warning(
                f"Falha ao copiar line.gpkg para pasta do projeto: {project_vectors_folder}"
            )
            return None, ""

        normalized_target = ProjectUtils.normalize_layer_source(copied_line_path)
        for layer in project.mapLayers().values():
            source_normalized = ProjectUtils.normalize_layer_source(layer.source())
            if source_normalized == normalized_target:
                self.logger.debug(
                    f"Camada de referencia ja carregada no projeto: {copied_line_path}"
                )
                if isinstance(layer, QgsVectorLayer):
                    return layer, copied_line_path
                return None, copied_line_path

        line_layer = VectorLayerSource.load_existing_vector_layer(
            copied_line_path, tool_key=self.TOOL_KEY
        )
        if not line_layer or not line_layer.isValid():
            self.logger.warning(
                f"Falha ao carregar camada de referencia line.gpkg copiada: {copied_line_path}"
            )
            return None, copied_line_path

        project.addMapLayer(line_layer, True)
        self.logger.info(
            f"Camada de referencia carregada a partir da copia: {copied_line_path}"
        )
        return line_layer, copied_line_path

    def _resolve_valid_crs(self, authid: str) -> QgsCoordinateReferenceSystem:
        crs = QgsCoordinateReferenceSystem(authid or self.DEFAULT_CRS_AUTHID)
        if crs.isValid():
            return crs

        self.logger.warning(
            f"SRC padrao invalido nas preferencias: '{authid}'. "
            f"Usando fallback {self.DEFAULT_CRS_AUTHID}"
        )
        return QgsCoordinateReferenceSystem(self.DEFAULT_CRS_AUTHID)

    def _apply_project_crs(self, project: QgsProject, authid: str):
        crs = self._resolve_valid_crs(authid)
        project.setCrs(crs)
        self.logger.info(f"SRC aplicado ao projeto: {crs.authid()}")

    def _create_project_structure(
        self, base_folder: str, project_name: str, default_crs_authid: str
    ):
        project_folder = Path(base_folder) / project_name
        project_file = project_folder / f"{project_name}.qgz"
        vectors_folder = project_folder / "vectors"
        rasters_folder = project_folder / "rasters"
        current_project = QgsProject.instance()
        current_project_path = current_project.fileName()
        scenario = self._detect_creation_scenario(current_project)
        should_load_line = self._should_load_line_for_scenario(scenario)

        if project_folder.exists():
            self.logger.warning(f"Pasta de projeto ja existe: {project_folder}")
            QgisMessageUtil.modal_warning(
                self.iface,
                f"{STR.PROJECT_FOLDER_ALREADY_EXISTS}\n{project_folder}",
            )
            return

        try:
            vectors_folder.mkdir(parents=True, exist_ok=False)
            rasters_folder.mkdir(parents=True, exist_ok=False)
        except Exception as e:
            self.logger.error(
                f"Erro ao criar estrutura de pastas para '{project_folder}': {e}"
            )
            QgisMessageUtil.modal_error(
                self.iface,
                f"{STR.PROJECT_FOLDER_CREATE_ERROR}\n{project_folder}\n\n{e}",
            )
            return

        try:
            if not current_project_path:
                self._apply_project_crs(current_project, default_crs_authid)
                self._add_google_basemap(current_project)
                line_layer = None
                line_path_in_project = ""
                if should_load_line:
                    line_layer, line_path_in_project = (
                        self._copy_and_load_line_reference_layer(
                            current_project, vectors_folder
                        )
                    )
                    if line_layer:
                        ProjectUtils.center_canvas_on_file_extent(
                            iface=self.iface,
                            file_path=line_path_in_project,
                            project=current_project,
                            layer_name=line_layer.name(),
                            tool_key=self.TOOL_KEY,
                        )
                if hasattr(current_project, "setPresetHomePath"):
                    current_project.setPresetHomePath(str(project_folder))
                current_project.setFileName(str(project_file))

                if not current_project.write(str(project_file)):
                    raise RuntimeError(STR.CURRENT_PROJECT_SAVE_TO_NEW_DESTINATION_ERROR)

                self.logger.info(
                    f"Projeto atual sem arquivo salvo em: {project_file}"
                )
            else:
                new_project = QgsProject()
                self._apply_project_crs(new_project, default_crs_authid)
                self._add_google_basemap(new_project)
                line_layer = None
                if should_load_line:
                    line_layer, _ = (
                        self._copy_and_load_line_reference_layer(
                            new_project, vectors_folder
                        )
                    )
                if hasattr(new_project, "setPresetHomePath"):
                    new_project.setPresetHomePath(str(project_folder))
                new_project.setFileName(str(project_file))

                if not new_project.write(str(project_file)):
                    raise RuntimeError(STR.NEW_PROJECT_FILE_WRITE_ERROR)

                line_extent = None
                if line_layer and line_layer.isValid():
                    layer_extent = line_layer.extent()
                    if not layer_extent.isEmpty():
                        line_extent = layer_extent

                if not self._open_project_in_new_window(project_file, line_extent):
                    raise RuntimeError(STR.OPEN_NEW_QGIS_WINDOW_ERROR)
        except Exception as e:
            self.logger.error(f"Erro ao criar projeto QGIS '{project_file}': {e}")
            QgisMessageUtil.modal_error(
                self.iface,
                f"{STR.PROJECT_FILE_CREATE_ERROR}\n{project_file}\n\n{e}",
            )
            return

        self.logger.info(f"Projeto criado com sucesso em: {project_folder}")
        QgisMessageUtil.modal_result_with_folder(
            self.iface,
            title=STR.PROJECT_CREATED_TITLE,
            message=(
                STR.PROJECT_CREATED_SUCCESS.format(project_name=project_name)
                if not current_project_path
                else STR.PROJECT_CREATED_OPENED_NEW_WINDOW.format(
                    project_name=project_name
                )
            ),
            folder_path=str(project_folder),
            parent=self.iface.mainWindow(),
        )


def run(iface):
    plugin = CreateProjectPlugin(iface)
    plugin.execute()
    return plugin
