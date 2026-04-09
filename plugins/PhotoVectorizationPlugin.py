# -*- coding: utf-8 -*-
import os

from ..core.ui.WidgetFactory import WidgetFactory
from ..core.services.PhotoFolderVectorizationService import PhotoFolderVectorizationService
from ..i18n.TranslationManager import STR
from ..plugins.BasePlugin import BasePluginMTL
from ..utils.ExplorerUtils import ExplorerUtils
from ..utils.Preferences import load_tool_prefs, save_tool_prefs
from ..utils.QgisMessageUtil import QgisMessageUtil
from ..utils.ToolKeys import ToolKey


class PhotoVectorizationPlugin(BasePluginMTL):
    """Ferramenta dedicada para geração de vetores a partir de imagens."""

    TOOL_KEY = ToolKey.PHOTO_VECTORIZATION
    PREF_PHOTO_FOLDER = "photo_folder"
    PREF_PHOTO_RECURSIVE = "photo_recursive"
    PREF_PHOTO_GENERATE_REPORT = "photo_generate_report"

    def __init__(self, iface):
        super().__init__(iface.mainWindow())
        self.iface = iface
        self.init(self.TOOL_KEY, self.__class__.__name__)

    def _build_ui(self, **kwargs):
        super()._build_ui(
            title=STR.PHOTO_VECTORIZATION_TITLE,
            icon_path="coord.ico",
            enable_scroll=True,
        )

        folder_layout, self.photo_folder_selector = WidgetFactory.create_path_selector(
            parent=self,
            title=STR.PHOTO_FOLDER,
            mode="folder",
            separator_top=False,
            separator_bottom=False,
        )

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

        buttons_layout, _ = WidgetFactory.create_bottom_action_buttons(
            parent=self,
            run_callback=self.execute_tool,
            close_callback=self.close,
            info_callback=self.show_info_dialog,
            tool_key=self.TOOL_KEY,
            run_text=STR.VECTORIZE_PHOTOS,
        )

        self.layout.add_items(
            [
                folder_layout,
                photo_opts_layout,
                buttons_layout,
            ]
        )

    def _save_prefs(self):
        photo_paths = self.photo_folder_selector.get_paths()
        photo_folder = photo_paths[0] if photo_paths else ""
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
        self._run_photo_vectorization()

    def _run_photo_vectorization(self):
        photo_paths = self.photo_folder_selector.get_paths()
        photo_folder = (photo_paths[0] if photo_paths else "").strip()
        if not photo_folder or not os.path.isdir(photo_folder):
            QgisMessageUtil.modal_warning(self.iface, STR.SELECT_VALID_FOLDER)
            return

        recursive = bool(self.photo_opts_map["photo_recursive"].isChecked())
        generate_report = bool(self.photo_opts_map["photo_generate_report"].isChecked())

        try:
            payload = PhotoFolderVectorizationService(tool_key=self.TOOL_KEY).generate_from_folder(
                base_folder=photo_folder,
                recursive=recursive,
                generate_report=generate_report,
                layer_name=STR.PHOTOS_WITHOUT_MRK_LAYER_NAME,
            )
            self._save_prefs()
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
            self.logger.error(f"Erro ao gerar vetor por fotos: {e}")
            QgisMessageUtil.modal_error(self.iface, f"{STR.ERROR}: {e}")


def run(iface):
    dlg = PhotoVectorizationPlugin(iface)
    dlg.setModal(False)
    dlg.show()
    return dlg
