import os

from ...core.config.LogUtils import LogUtils
from ...plugins.BaseDialog import BaseDialog
from qgis.PyQt.QtWidgets import (
    QDialog, QVBoxLayout, QPushButton, QTextBrowser
)
from qgis.PyQt.QtCore import Qt


class InfoDialog(BaseDialog):
    def __init__(self, instructions_path: str, parent=None, title="MTL Tools"):
        super().__init__(parent)
        self.logger = LogUtils(tool="Untraceable", class_name=self.__class__.__name__, level=LogUtils.DEBUG)
        self.logger.debug(f"Inicializando InfoDialog com arquivo: {instructions_path}")

        # Use BaseDialog layout builder so dialogs share the same shell
        self._build_ui(title=title, enable_scroll=False)

        # prefer explicit window title and sensible minimum size
        self.setWindowTitle(title)
        self.setMinimumWidth(700)
        self.setMinimumHeight(550)

        browser = QTextBrowser()
        browser.setOpenExternalLinks(True)

        if os.path.exists(instructions_path):
            with open(instructions_path, "r", encoding="utf-8") as f:
                md_text = f.read()

            # 🔥 Renderização Markdown NATIVA do Qt
            doc = browser.document()
            if hasattr(doc, "setMarkdown"):
                # QGIS mais novo (Qt >= 5.14)
                doc.setMarkdown(md_text)
            else:
                # QGIS 3.16 fallback
                html = self._markdown_to_html(md_text)
                browser.setHtml(html)

        else:
            browser.setPlainText(
                f"Arquivo de instruções não encontrado:\n{instructions_path}"
            )

        # add browser and close button to the shared layout
        if hasattr(self, 'layout') and self.layout is not None:
            self.layout.addWidget(browser)
            btn = QPushButton("Fechar")
            btn.clicked.connect(self.close)
            self.layout.addWidget(btn, alignment=Qt.AlignRight)
            self.logger.debug(f"InfoDialog UI construída com sucesso usando BaseDialog layout.")
        else:
            # fallback: use a local layout if BaseDialog failed to create one
            layout = QVBoxLayout(self)
            layout.addWidget(browser)
            btn = QPushButton("Fechar")
            btn.clicked.connect(self.close)
            layout.addWidget(btn, alignment=Qt.AlignRight)
            self.logger.warning("BaseDialog layout não encontrado. Usando layout local para InfoDialog.")

    def _markdown_to_html(self, text: str) -> str:
        """
        Conversão simples de Markdown para HTML
        Compatível com QGIS 3.16 (sem setMarkdown)
        """
        self.logger.debug("Convertendo Markdown para HTML (fallback)")
        import re

        html = text

        # Títulos
        html = re.sub(r"^###### (.*)", r"<h6>\1</h6>", html, flags=re.MULTILINE)
        html = re.sub(r"^##### (.*)", r"<h5>\1</h5>", html, flags=re.MULTILINE)
        html = re.sub(r"^#### (.*)", r"<h4>\1</h4>", html, flags=re.MULTILINE)
        html = re.sub(r"^### (.*)", r"<h3>\1</h3>", html, flags=re.MULTILINE)
        html = re.sub(r"^## (.*)", r"<h2>\1</h2>", html, flags=re.MULTILINE)
        html = re.sub(r"^# (.*)", r"<h1>\1</h1>", html, flags=re.MULTILINE)

        # Negrito
        html = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", html)

        # Itálico
        html = re.sub(r"\*(.*?)\*", r"<i>\1</i>", html)

        # Quebra de linha
        html = html.replace("\n", "<br>")

        return f"<html><body>{html}</body></html>"
