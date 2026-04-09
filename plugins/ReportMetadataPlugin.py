# -*- coding: utf-8 -*-
import os
from datetime import datetime

from ..core.ui.WidgetFactory import WidgetFactory
from ..core.services.PhotoFolderVectorizationService import (
    PhotoFolderVectorizationService,
)
from ..core.services.ReportGenerationService import ReportGenerationService
from ..i18n.TranslationManager import STR
from ..plugins.BasePlugin import BasePluginMTL
from ..utils.ExplorerUtils import ExplorerUtils
from ..utils.Preferences import load_tool_prefs, save_tool_prefs
from ..utils.QgisMessageUtil import QgisMessageUtil
from ..utils.ToolKeys import ToolKey


class ReportMetadataPlugin(BasePluginMTL):
    """Ferramenta para regerar relatorios HTML a partir de JSONs temporarios."""

    TOOL_KEY = ToolKey.REPORT_METADATA
    PREF_SELECTED_JSON = "selected_json"
    PREF_PHOTO_FOLDER = "photo_folder"
    PREF_PHOTO_RECURSIVE = "photo_recursive"
    PREF_PHOTO_GENERATE_REPORT = "photo_generate_report"

    def __init__(self, iface):
        super().__init__(iface.mainWindow())
        self.iface = iface
        self.json_options = {}
        self.init(self.TOOL_KEY, self.__class__.__name__)

    def _build_ui(self, **kwargs):
        super()._build_ui(
            title=STR.REPORT_METADATA_TITLE,
            icon_path="coord.ico",
            enable_scroll=True,
        )

        self._reload_json_options(initial=True)

        dropdown_layout, self.json_selector = WidgetFactory.create_dropdown_selector(
            title="JSON:",
            options_dict=self.json_options,
            selected_key=self.preferences.get(self.PREF_SELECTED_JSON),
            allow_empty=True,
            empty_text=STR.SELECT,
            separator_top=False,
            separator_bottom=False,
            parent=self,
        )

        refresh_layout, self.refresh_button = WidgetFactory.create_simple_button(
            text=STR.REFRESH_JSON_LIST,
            parent=self,
            spacing=8,
        )
        self.refresh_button.clicked.connect(self._on_refresh)

        open_json_layout, self.open_json_button = WidgetFactory.create_simple_button(
            text=STR.OPEN_JSONS_FOLDER,
            parent=self,
            spacing=8,
        )
        self.open_json_button.clicked.connect(self._open_json_folder)

        open_reports_layout, self.open_reports_button = WidgetFactory.create_simple_button(
            text=STR.OPEN_REPORTS_FOLDER,
            parent=self,
            spacing=8,
        )
        self.open_reports_button.clicked.connect(self._open_reports_folder)

        photos_block_layout, self.photos_collapsible = (
            WidgetFactory.create_collapsible_parameters(
                parent=self,
                title=STR.VECTOR_WITHOUT_MRK_BLOCK_TITLE,
                expanded_by_default=False,
            )
        )

        folder_layout, self.photo_folder_selector = WidgetFactory.create_path_selector(
            parent=self,
            title=STR.PHOTO_FOLDER,
            mode="folder",
            separator_top=False,
            separator_bottom=False,
        )
        self.photos_collapsible.add_content_layout(folder_layout)

        photo_opts_layout, self.photo_opts_map = WidgetFactory.create_checkbox_grid(
            options_data={
                "photo_recursive": STR.RECURSIVE_SEARCH,
                "photo_generate_report": STR.GENERATE_REPORT,
            },
            items_per_row=1,
            checked_by_default=False,
            separator_top=False,
            separator_bottom=False,
        )
        self.photos_collapsible.add_content_layout(photo_opts_layout)

        photo_run_layout, self.photo_run_button = WidgetFactory.create_simple_button(
            text=STR.VECTORIZE_PHOTOS,
            parent=self,
            spacing=8,
        )
        self.photo_run_button.clicked.connect(self._run_photo_vectorization)
        self.photos_collapsible.add_content_layout(photo_run_layout)

        buttons_layout, _ = WidgetFactory.create_bottom_action_buttons(
            parent=self,
            run_callback=self.execute_tool,
            close_callback=self.close,
            info_callback=self.show_info_dialog,
            tool_key=self.TOOL_KEY,
            run_text=STR.GENERATE_REPORT,
        )

        self.layout.add_items(
            [
                dropdown_layout,
                refresh_layout,
                open_json_layout,
                open_reports_layout,
                photos_block_layout,
                buttons_layout,
            ]
        )

    def _format_json_label(self, file_path: str) -> str:
        file_name = os.path.basename(file_path)
        try:
            mtime = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            size_kb = round(os.path.getsize(file_path) / 1024.0, 1)
            return f"{mtime} | {size_kb} KB | {file_name}"
        except Exception:
            return file_name

    def _list_json_files(self):
        json_dir = ExplorerUtils.get_temp_folder(
            self.TOOL_KEY,
            ExplorerUtils.REPORTS_TEMP_FOLDER,
            ExplorerUtils.REPORTS_JSON_FOLDER,
        )
        files = []
        if os.path.isdir(json_dir):
            for name in os.listdir(json_dir):
                if name.lower().endswith(".json"):
                    files.append(os.path.join(json_dir, name))
        files.sort(key=lambda p: os.path.getmtime(p), reverse=True)
        return files

    def _reload_json_options(self, initial=False):
        files = self._list_json_files()
        self.json_options = {path: self._format_json_label(path) for path in files}
        if not initial:
            self.json_selector.set_options(self.json_options)
        self.logger.info(
            "Lista de JSONs temporarios atualizada",
            data={"total_json": len(self.json_options)},
        )

    def _on_refresh(self):
        self._reload_json_options(initial=False)
        if not self.json_options:
            QgisMessageUtil.bar_warning(
                self.iface,
                STR.NO_JSON_FOUND,
            )

    def _open_reports_folder(self):
        folder = ExplorerUtils.get_temp_folder(
            self.TOOL_KEY,
            ExplorerUtils.REPORTS_TEMP_FOLDER,
            ExplorerUtils.REPORTS_HTML_FOLDER,
        )
        ExplorerUtils.ensure_folder_exists(folder, self.TOOL_KEY)
        if not ExplorerUtils.open_folder(folder, self.TOOL_KEY):
            QgisMessageUtil.modal_warning(self.iface, STR.INVALID_FOLDER)

    def _open_json_folder(self):
        folder = ExplorerUtils.get_temp_folder(
            self.TOOL_KEY,
            ExplorerUtils.REPORTS_TEMP_FOLDER,
            ExplorerUtils.REPORTS_JSON_FOLDER,
        )
        ExplorerUtils.ensure_folder_exists(folder, self.TOOL_KEY)
        if not ExplorerUtils.open_folder(folder, self.TOOL_KEY):
            QgisMessageUtil.modal_warning(self.iface, STR.INVALID_FOLDER)

    def _save_prefs(self):
        selected = self.json_selector.get_selected_key() if self.json_selector else ""
        photo_paths = self.photo_folder_selector.get_paths()
        photo_folder = photo_paths[0] if photo_paths else ""
        self.preferences[self.PREF_SELECTED_JSON] = selected or ""
        self.preferences[self.PREF_PHOTO_FOLDER] = photo_folder
        self.preferences[self.PREF_PHOTO_RECURSIVE] = bool(
            self.photo_opts_map["photo_recursive"].isChecked()
        )
        self.preferences[self.PREF_PHOTO_GENERATE_REPORT] = bool(
            self.photo_opts_map["photo_generate_report"].isChecked()
        )
        save_tool_prefs(self.TOOL_KEY, self.preferences)

    def _load_prefs(self):
        self.preferences = load_tool_prefs(self.TOOL_KEY)
        folder = self.preferences.get(self.PREF_PHOTO_FOLDER, "")
        if folder:
            self.photo_folder_selector.set_path(folder)
        self.photo_opts_map["photo_recursive"].setChecked(
            self.preferences.get(self.PREF_PHOTO_RECURSIVE, True)
        )
        self.photo_opts_map["photo_generate_report"].setChecked(
            self.preferences.get(self.PREF_PHOTO_GENERATE_REPORT, True)
        )

    def execute_tool(self):
        selected_json = self.json_selector.get_selected_key() if self.json_selector else ""
        if not selected_json:
            QgisMessageUtil.modal_warning(self.iface, STR.SELECT_FILE)
            return

        if not os.path.isfile(selected_json):
            QgisMessageUtil.modal_warning(
                self.iface,
                f"{STR.FILE_NOT_FOUND}: {selected_json}",
            )
            return

        try:
            payload = ReportGenerationService(tool_key=self.TOOL_KEY).generate_from_json(
                selected_json
            )
            html_path = payload.get("html_path", "")
            if html_path:
                if not ExplorerUtils.open_file(html_path, self.TOOL_KEY):
                    QgisMessageUtil.bar_warning(
                        self.iface,
                        f"{STR.WARNING}: nao foi possivel abrir o HTML automaticamente.",
                    )
            self._save_prefs()
            QgisMessageUtil.bar_success(
                self.iface,
                f"{STR.SUCCESS_MESSAGE} {html_path}",
            )
        except Exception as e:
            self.logger.error(f"Erro ao gerar relatorio via plugin: {e}")
            QgisMessageUtil.modal_error(self.iface, f"{STR.ERROR}: {e}")

    def _run_photo_vectorization(self):
        photo_paths = self.photo_folder_selector.get_paths()
        photo_folder = (photo_paths[0] if photo_paths else "").strip()
        if not photo_folder or not os.path.isdir(photo_folder):
            QgisMessageUtil.modal_warning(self.iface, STR.SELECT_VALID_FOLDER)
            return

        recursive = bool(self.photo_opts_map["photo_recursive"].isChecked())
        generate_report = bool(self.photo_opts_map["photo_generate_report"].isChecked())

        try:
            payload = PhotoFolderVectorizationService(
                tool_key=self.TOOL_KEY
            ).generate_from_folder(
                base_folder=photo_folder,
                recursive=recursive,
                generate_report=generate_report,
                layer_name=STR.PHOTOS_WITHOUT_MRK_LAYER_NAME,
            )
            self._save_prefs()
            self._on_refresh()
            html_path = (
                (payload.get("report_payload") or {}).get("html_path")
                if payload.get("report_payload")
                else ""
            )
            summary = (
                f"{STR.SUCCESS_MESSAGE} "
                f"{STR.POINTS}: {payload.get('total_points', 0)} | "
                f"JSON: {payload.get('json_path', '')}"
            )
            if html_path:
                summary += f" | HTML: {html_path}"
                if not ExplorerUtils.open_file(html_path, self.TOOL_KEY):
                    QgisMessageUtil.bar_warning(
                        self.iface,
                        f"{STR.WARNING}: nao foi possivel abrir o HTML automaticamente.",
                    )
            QgisMessageUtil.bar_success(self.iface, summary, duration=8)
        except Exception as e:
            self.logger.error(f"Erro na vetorizacao sem MRK: {e}")
            QgisMessageUtil.modal_error(self.iface, f"{STR.ERROR}: {e}")


def run(iface):
    dlg = ReportMetadataPlugin(iface)
    dlg.setModal(False)
    dlg.show()
    return dlg
