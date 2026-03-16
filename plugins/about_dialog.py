# -*- coding: utf-8 -*-
import os
from qgis.PyQt.QtCore import Qt
from ..core.config.LogUtils import LogUtils
from ..plugins.BaseDialog import BaseDialog
from ..core.ui.WidgetFactory import WidgetFactory


class AboutDialog(BaseDialog):

    def __init__(self, iface):
        try:
            super().__init__(iface.mainWindow())

            self.logger = LogUtils(
                tool="untraceable",
                class_name=self.__class__.__name__,
                level=LogUtils.DEBUG,
            )
            self.logger.debug("Inicializando AboutDialog")

            self.setWindowTitle("Sobre o Cadmus")
            self._build_ui(title="Sobre o Cadmus", enable_scroll=False, minimum_size=(420, 520))
            self.logger.debug("AboutDialog _build_ui concluído")

            logo_path = os.path.join(
                os.path.dirname(__file__), "..", "resources", "icons", "mtl_agro.png"
            )

            if os.path.exists(logo_path):
                image_layout, _ = WidgetFactory.create_image_widget(
                    image_path=logo_path,
                    fixed_height=160,
                    parent=self,
                    separator_bottom=True,
                )
                self.layout.addLayout(image_layout)
                self.logger.debug(f"Logo adicionado: {logo_path}")
            else:
                self.logger.warning(f"Logo não encontrado: {logo_path}")

            lbl_title = WidgetFactory.create_label(
                text="<h2>Cadmus</h2>",
                bold=False,
                word_wrap=True,
                parent=self,
                text_format=Qt.RichText,
                alignment=Qt.AlignCenter,
            )
            self.layout.addWidget(lbl_title)
            self.logger.debug("Título adicionado")

            info_text = (
                "<b>Versão:</b> 2.0.4<br>"
                "<b>Atualizada em:</b> 15 de Março de 2026<br>"
                "<b>Criado em:</b> 9 de Dezembro de 2024<br>"
                "<b>Criador:</b> MTL Agricultura e Tecnologia<br>"
                "<b>Local:</b> Palmas - Tocantins - Brasil<br>"
                "<b>Email:</b> <a href=\"mailto:martinelli.matheus11@gmail.com\">martinelli.matheus11@gmail.com</a><br>"
                "<b>Site:</b> <a href=\"https://github.com/MartinelliNTZ/Cadmus\">https://github.com/MartinelliNTZ/Cadmus</a><br>"
                "<b>GitHub:</b> <a href=\"https://github.com/MartinelliNTZ/Cadmus\">https://github.com/MartinelliNTZ/Cadmus</a>"
            )

            lbl_info = WidgetFactory.create_label(
                text=info_text,
                bold=False,
                word_wrap=True,
                parent=self,
                text_format=Qt.RichText,
                text_interaction_flags=Qt.TextBrowserInteraction,
                open_external_links=True,
                alignment=Qt.AlignCenter,
            )
            self.layout.addWidget(lbl_info)
            self.logger.debug("Informações adicionadas")

            close_layout, close_button = WidgetFactory.create_simple_button(
                text="Fechar",
                parent=self,
                separator_top=True,
                separator_bottom=False,
            )
            close_button.clicked.connect(self.close)
            self.layout.addLayout(close_layout)
            self.logger.debug("Botão Fechar adicionado")

            self.logger.debug("AboutDialog UI construída com sucesso")
        except Exception as ex:
            if hasattr(self, 'logger') and self.logger:
                self.logger.error(f"AboutDialog falhou na inicialização: {ex}")
            else:
                print(f"AboutDialog falhou na inicialização: {ex}")
            raise



def run_about_dialog(iface):
    dlg = AboutDialog(iface)
    dlg.setModal(False)
    dlg.show()
    return dlg