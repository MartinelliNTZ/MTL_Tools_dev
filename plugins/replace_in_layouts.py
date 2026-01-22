# -*- coding: utf-8 -*-
import os

from qgis.core import QgsProject
from qgis.PyQt.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QMessageBox, QCheckBox
)
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtCore import Qt, QUrl
from qgis.PyQt.QtGui import QDesktopServices

from ..utils.preferences import load_tool_prefs, save_tool_prefs
from ..utils.info_dialog import InfoDialog
from ..utils.qgis_messagem_util import QgisMessageUtil
from ..utils.ui_widget_utils import UiWidgetUtils
from ..utils.layouts_utils import LayoutsUtils
from ..utils.project_utils import ProjectUtils
from ..utils.tool_keys import ToolKey
from .base_plugin import BasePluginMTL


class ReplaceInLayoutsDialog(BasePluginMTL):

    TOOL_KEY = ToolKey.REPLACE_IN_LAYOUTS

    def __init__(self, iface):
        super().__init__(iface.mainWindow())
        self.iface = iface

        self.setWindowTitle("MTL Tools — Replace Text in Layouts")
        self.setMinimumWidth(520)

        icon_path = os.path.join(
            os.path.dirname(__file__), "..", "resources","icons", "mtl_tools_icon.png"
        )
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.instructions_file = os.path.join(
            os.path.dirname(__file__),
            "instructions",
            "replace_in_layouts_help.md"
        )

        self._build_ui()
        self._load_saved_preferences()

    # -------------------------------------------------
    def _build_ui(self):
        main = QVBoxLayout()

        # INFO
        info_layout = QHBoxLayout()
        info_layout.addStretch()
        btn_info = QPushButton("ℹ️")
        btn_info.setFixedWidth(30)
        btn_info.clicked.connect(
            lambda: self.show_info_dialog(
                "📘 Instruções – Replace Text in Layouts"
            )
        )

        info_layout.addWidget(btn_info)
        main.addLayout(info_layout)

        # CAMPOS
        h1 = QHBoxLayout()
        h1.addWidget(QLabel("Texto a buscar:"))
        self.txt_old = QLineEdit()
        h1.addWidget(self.txt_old)
        main.addLayout(h1)

        h2 = QHBoxLayout()
        h2.addWidget(QLabel("Texto a substituir (novo):"))
        self.txt_new = QLineEdit()
        h2.addWidget(self.txt_new)
        main.addLayout(h2)

        self.chk_case_sensitive = QCheckBox(
            "Diferenciar maiúsculas/minúsculas (case sensitive)"
        )
        main.addWidget(self.chk_case_sensitive)

        self.chk_full_replace = QCheckBox(
            "Substituir o label inteiro quando encontrar o texto (modo chave)"
        )
        main.addWidget(self.chk_full_replace)

        lbl_backup = QLabel(
            "<b>Backup:</b> será criada uma cópia do projeto (.qgz) "
            "na pasta <i>backup</i> ao lado do arquivo do projeto."
        )
        lbl_backup.setWordWrap(True)
        main.addWidget(lbl_backup)

        # BOTÕES
        h_buttons = QHBoxLayout()

        btn_show_proj = QPushButton("Mostrar arquivo do projeto")
        btn_show_proj.clicked.connect(self.show_project_file)
        h_buttons.addWidget(btn_show_proj)

        btn_run = QPushButton("Executar substituição")
        btn_run.clicked.connect(self.on_run_clicked)
        h_buttons.addWidget(btn_run)

        main.addLayout(h_buttons)

        h_close = QHBoxLayout()
        h_close.addStretch()
        btn_close = QPushButton("Fechar")
        btn_close.clicked.connect(self.close)
        h_close.addWidget(btn_close)
        main.addLayout(h_close)

        self.setLayout(main)


    # -------------------------------------------------
    def _load_saved_preferences(self):
        prefs = load_tool_prefs(self.TOOL_KEY)

        self.txt_old.setText(prefs.get("old_text", ""))
        self.txt_new.setText(prefs.get("new_text", ""))
        self.chk_case_sensitive.setChecked(
            prefs.get("case_sensitive", True)
        )
        self.chk_full_replace.setChecked(
            prefs.get("full_replace", False)
        )

    def _save_preferences(self):
        save_tool_prefs(
            self.TOOL_KEY,
            {
                "old_text": self.txt_old.text(),
                "new_text": self.txt_new.text(),
                "case_sensitive": self.chk_case_sensitive.isChecked(),
                "full_replace": self.chk_full_replace.isChecked()
            }
        )



    # -------------------------------------------------
    def on_run_clicked(self):
        old_text = self.txt_old.text().strip()
        new_text = self.txt_new.text()
        case_sensitive = self.chk_case_sensitive.isChecked()
        full_replace = self.chk_full_replace.isChecked()

        if not old_text:
            QgisMessageUtil.bar_warning(
                self.iface,
                "Informe o texto a buscar."
            )
            return

        self._save_preferences()

        if not QgisMessageUtil.confirm_destructive(
            self,
            "Confirme substituições",
            (                
                f"<b>Buscar:</b> <i>{old_text}</i><br>"
                f"<b>Substituir por:</b> <i>{new_text}</i>"
            ),
            red_text="Atenção — operação destrutiva"
        ):
            return


        project = QgsProject.instance()

        try:
            # BACKUP (se possível)
            if ProjectUtils.is_project_saved(project):
                ProjectUtils.create_project_backup(project)

            # PROCESSA LAYOUTS
            result = LayoutsUtils.replace_text_in_layouts(
                project=project,
                tool_key=self.TOOL_KEY,
                old_text=old_text,
                new_text=new_text,
                case_sensitive=case_sensitive,
                full_replace=full_replace
            )
            total = result.get("total_changes", 0)
            layouts = result.get("total_layouts", 0)
            message =f"<b>Layouts analisados:</b> {layouts}<br>" f"<b>Substituições aplicadas:</b> {total}"
            QgisMessageUtil.modal_success(
                self.iface,
                message,
                "Substituição concluída"
            )       
        except Exception as e:
            QMessageBox.critical(
                self,
                "Erro",
                str(e)
            )



# -------------------------------------------------
def run_replace_in_layouts(iface):
    dlg = ReplaceInLayoutsDialog(iface)
    dlg.setModal(False)
    dlg.show()
    return dlg
