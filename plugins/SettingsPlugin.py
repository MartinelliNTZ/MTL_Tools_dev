# -*- coding: utf-8 -*-
"""
SettingsPlugin - Configurações do MTL Tools

Exibe preferências do aplicativo e configurações de cálculo vetorial.
"""

from qgis.PyQt.QtWidgets import QLabel, QMessageBox
from qgis.PyQt.QtGui import QDesktopServices
from qgis.PyQt.QtCore import QUrl, Qt

from ..plugins.BasePlugin import BasePluginMTL
from ..utils.preferences import load_tool_prefs, save_tool_prefs
from ..utils.tool_keys import ToolKey
from ..core.ui.WidgetFactory import WidgetFactory
from ..core.config.LogUtilsNew import LogUtilsNew
from ..utils.string_utils import StringUtils


class SettingsPlugin(BasePluginMTL):
    """
    Plugin de configurações do MTL Tools.
    
    Permite ao usuário:
    - Acessar preferências do aplicativo
    - Configurar método de cálculo vetorial (Elipsoidal, Cartesiana, Ambos)
    """

    CALCULATION_METHODS = ["Elipsoidal", "Cartesiana", "Ambos"]

    def __init__(self, iface):
        super().__init__(iface.mainWindow())
        self.iface = iface
        self.init(ToolKey.SETTINGS, "SettingsPlugin")
        self.logger.info("SettingsPlugin inicializado")

    def _build_ui(self):
        """Constrói a interface de configurações."""
        self.logger.debug("Construindo interface de configurações")
        
        super()._build_ui(
            title="Configurações MTL Tools",
            icon_path="system.ico",
            instructions_file="settings_help.md"
        )
        
        self.logger.info("Construindo componentes de interface")

        # ========== SEÇÃO 1: Preferências do App ==========
        prefs_label = QLabel("📋 Preferências do Aplicativo")
        prefs_label.setStyleSheet("font-weight: bold; font-size: 11pt;")
        self.layout.add_items([prefs_label])

        # Link clicável para preferências
        pref_link = QLabel(
            '<a href="open_prefs" style="color: #0066cc; text-decoration: underline;">Abrir Pasta de Preferências</a>'
        )
        pref_link.setOpenExternalLinks(False)
        pref_link.setCursor(Qt.PointingHandCursor)
        pref_link.linkActivated.connect(self._on_open_preferences)

        self.layout.add_items([pref_link])
        self.logger.debug("Link de preferências adicionado")

        # ========== SEÇÃO 2: Método de Cálculo Vetorial ==========
        calc_layout, self.radio_calc = WidgetFactory.create_radio_button_grid(
            items=self.CALCULATION_METHODS,
            columns=3,
            title="⚙️ Método de Cálculo Vetorial",
            checked_index=0,
            tool_key=ToolKey.SETTINGS,
            separator_top=True,
            separator_bottom=True,
            parent=self
        )
        self.layout.add_items([calc_layout])
        self.logger.debug("Widget de cálculo vetorial adicionado")

        # ========== BOTÕES DE AÇÃO ==========
        buttons_layout, self.action_buttons = WidgetFactory.create_bottom_action_buttons(
            parent=self,
            run_callback=self.execute_tool,
            close_callback=self.close,
            info_callback=self.show_info_dialog,
            tool_key=ToolKey.SETTINGS,
            run_text = "Salvar"
        )
        self.layout.add_items([buttons_layout])
        self.logger.info("Interface de configurações construída com sucesso")

    def _load_prefs(self):
        """Carrega preferências salvas."""
        self.logger.debug("Carregando preferências")
        self.preferences = load_tool_prefs(ToolKey.SETTINGS)

        # Carregar método de cálculo selecionado
        calc_method = self.preferences.get('calculation_method', 'Elipsoidal')
        try:
            idx = self.CALCULATION_METHODS.index(calc_method)
            self.radio_calc.set_selected_index(idx)
            self.logger.debug(f"Método de cálculo carregado: {calc_method}")
        except (ValueError, IndexError):
            self.logger.warning(f"Método de cálculo inválido: {calc_method}, usando padrão")
            self.radio_calc.set_selected_index(0)

    def _save_prefs(self):
        """Salva preferências."""
        self.logger.debug("Salvando preferências")
        
        # Salvar método de cálculo selecionado
        selected_text = self.radio_calc.get_selected_text()
        self.preferences['calculation_method'] = selected_text
        
        save_tool_prefs(ToolKey.SETTINGS, self.preferences)
        self.logger.info(f"Preferências salvas: cálculo={selected_text}")

    def execute_tool(self):
        """Executa as configurações e fecha o diálogo."""
        self.logger.info("Aplicando configurações")
        self._save_prefs()
        
        selected_method = self.radio_calc.get_selected_text()
        QMessageBox.information(
            self,
            "Configurações Salvas",
            f"Método de cálculo vetorial: {selected_method}\n\n"
            f"As configurações foram salvas com sucesso."
        )
        
        self.logger.info("Configurações aplicadas e salvas")
        self.close()

    def _on_open_preferences(self):
        """Abre a pasta de preferências do MTL Tools."""
        self.logger.debug("Abrindo pasta de preferências")
        
        from ..utils.preferences import PREF_FOLDER
        import os
        
        if os.path.exists(PREF_FOLDER):
            self.logger.info(f"Abrindo pasta: {PREF_FOLDER}")
            QDesktopServices.openUrl(QUrl.fromLocalFile(PREF_FOLDER))
        else:
            self.logger.warning(f"Pasta de preferências não encontrada: {PREF_FOLDER}")
            QMessageBox.warning(
                self,
                "Aviso",
                f"Pasta de preferências não encontrada:\n{PREF_FOLDER}"
            )


def run_settings(iface):
    """Função de entrada do plugin."""
    dlg = SettingsPlugin(iface)
    dlg.setModal(False)
    dlg.show()
    return dlg
