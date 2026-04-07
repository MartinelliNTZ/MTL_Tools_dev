# -*- coding: utf-8 -*-
import os
import re
from pathlib import Path

from qgis.PyQt.QtCore import QCoreApplication, QProcess
from qgis.PyQt.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QVBoxLayout,
)
from qgis.core import QgsCoordinateReferenceSystem, QgsProject, QgsRasterLayer

from ..core.config.LogUtils import LogUtils
from ..i18n.TranslationManager import STR
from ..resources.widgets.SelectorWidget import SelectorWidget
from ..utils.Preferences import load_tool_prefs, save_tool_prefs
from ..utils.QgisMessageUtil import QgisMessageUtil
from ..utils.ToolKeys import ToolKey


class _DefaultFolderDialog(QDialog):
    DEFAULT_FOLDER = "C:/QgisProjects"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(STR.DEFAULT_PROJECTS_FOLDER_TITLE)
        self.setModal(True)
        self.resize(620, 120)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        info = QLabel(STR.DEFAULT_PROJECTS_FOLDER_PROMPT)
        info.setWordWrap(True)
        layout.addWidget(info)

        self.selector = SelectorWidget(
            title=STR.PROJECTS_FOLDER,
            mode=SelectorWidget.MODE_FOLDER,
            parent=self,
        )
        self.selector.set_path(self.DEFAULT_FOLDER)
        layout.addWidget(self.selector)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_folder_path(self) -> str:
        text = self.selector._input.text().strip()
        return text or self.DEFAULT_FOLDER


class _ProjectNameDialog(QDialog):
    def __init__(self, suggested_name: str, parent=None):
        super().__init__(parent)
        self._suggested_name = suggested_name
        self.setWindowTitle(STR.PROJECT_NAME_TITLE)
        self.setModal(True)
        self.resize(460, 110)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        info = QLabel(STR.PROJECT_NAME_PROMPT)
        info.setWordWrap(True)
        layout.addWidget(info)

        row = QHBoxLayout()
        row.addWidget(QLabel(STR.PROJECT_NAME_LABEL))

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText(self._suggested_name)
        row.addWidget(self.name_input)
        layout.addLayout(row)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_project_name(self) -> str:
        return self.name_input.text().strip()


class CreateProjectPlugin:
    DEFAULT_PROJECTS_FOLDER = "C:/QgisProjects"
    PROJECTS_FOLDER_PREF_KEY = "projects_folder"
    TOOL_KEY = ToolKey.CREATE_PROJECT
    GENERIC_PROJECT_PATTERN = re.compile(r"^NovoProjeto_(\d+)$")
    DEFAULT_CRS_AUTHID = "EPSG:4326"
    DEFAULT_CRS_PREF_KEY = "default_crs_authid"
    GOOGLE_SATELLITE_LAYER_NAME = "Google Satellite"
    GOOGLE_SATELLITE_URI = (
        "type=xyz&zmin=0&zmax=21&"
        "url=https://mt1.google.com/vt/lyrs=s%26x=%7Bx%7D%26y=%7By%7D%26z=%7Bz%7D"
    )

    def __init__(self, iface):
        self.iface = iface
        self.logger = LogUtils(
            tool=self.TOOL_KEY, class_name="CreateProjectPlugin", level=LogUtils.DEBUG
        )

    def execute(self):
        self.logger.info("Iniciando fluxo de criacao de novo projeto")
        system_prefs = load_tool_prefs(ToolKey.SYSTEM)
        base_folder = (system_prefs.get(self.PROJECTS_FOLDER_PREF_KEY) or "").strip()

        if not base_folder:
            should_define = QgisMessageUtil.confirm(
                self.iface,
                STR.PROJECTS_DEFAULT_FOLDER_MISSING,
                title=STR.PROJECTS_DEFAULT_FOLDER_MISSING_TITLE,
            )
            if not should_define:
                self.logger.info("Usuario cancelou definicao da pasta padrao")
                return

            folder_dialog = _DefaultFolderDialog(parent=self.iface.mainWindow())
            if folder_dialog.exec() != QDialog.Accepted:
                self.logger.info("Usuario cancelou o dialogo da pasta padrao")
                return

            base_folder = folder_dialog.get_folder_path()
            try:
                os.makedirs(base_folder, exist_ok=True)
            except Exception as e:
                self.logger.error(f"Erro ao criar pasta padrao '{base_folder}': {e}")
                QgisMessageUtil.modal_error(
                    self.iface,
                    f"{STR.PROJECT_DEFAULT_FOLDER_PREPARE_ERROR}\n{base_folder}\n\n{e}",
                )
                return

            system_prefs[self.PROJECTS_FOLDER_PREF_KEY] = base_folder
            save_tool_prefs(ToolKey.SYSTEM, system_prefs)
            self.logger.info(f"Pasta padrao salva nas system prefs: {base_folder}")
        else:
            try:
                os.makedirs(base_folder, exist_ok=True)
            except Exception as e:
                self.logger.error(
                    f"Erro ao preparar pasta padrao existente '{base_folder}': {e}"
                )
                QgisMessageUtil.modal_error(
                    self.iface,
                    f"{STR.PROJECT_DEFAULT_FOLDER_ACCESS_ERROR}\n{base_folder}\n\n{e}",
                )
                return

        suggested_name = self._next_generic_project_name(base_folder)
        name_dialog = _ProjectNameDialog(
            suggested_name=suggested_name, parent=self.iface.mainWindow()
        )
        if name_dialog.exec() != QDialog.Accepted:
            self.logger.info("Usuario cancelou o dialogo de nome do projeto")
            return

        project_name = self._sanitize_project_name(name_dialog.get_project_name())
        if not project_name:
            project_name = suggested_name

        default_crs_authid = (
            system_prefs.get(self.DEFAULT_CRS_PREF_KEY) or self.DEFAULT_CRS_AUTHID
        )
        self._create_project_structure(base_folder, project_name, default_crs_authid)

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

    def _open_project_in_new_window(self, project_file: Path) -> bool:
        executable = self._get_qgis_executable()
        if not executable:
            self.logger.error("Executavel do QGIS nao encontrado para nova janela")
            return False

        started = QProcess.startDetached(executable, [str(project_file)])
        if isinstance(started, tuple):
            started = started[0]

        self.logger.debug(
            f"Abertura de nova janela para projeto '{project_file}': {started}"
        )
        return bool(started)

    def _add_google_basemap(self, project: QgsProject):
        existing_names = [layer.name() for layer in project.mapLayers().values()]
        if self.GOOGLE_SATELLITE_LAYER_NAME in existing_names:
            self.logger.debug("Camada base Google ja existe no projeto; ignorando")
            return

        layer = QgsRasterLayer(
            self.GOOGLE_SATELLITE_URI,
            self.GOOGLE_SATELLITE_LAYER_NAME,
            "wms",
        )
        if not layer.isValid():
            self.logger.warning("Falha ao criar camada base Google (XYZ)")
            return

        project.addMapLayer(layer, True)
        self.logger.info("Camada base Google adicionada ao projeto")

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
                if hasattr(new_project, "setPresetHomePath"):
                    new_project.setPresetHomePath(str(project_folder))
                new_project.setFileName(str(project_file))

                if not new_project.write(str(project_file)):
                    raise RuntimeError(STR.NEW_PROJECT_FILE_WRITE_ERROR)

                if not self._open_project_in_new_window(project_file):
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
