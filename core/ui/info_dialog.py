import os
from qgis.PyQt.QtWidgets import (
    QDialog, QVBoxLayout, QPushButton, QTextBrowser
)
from qgis.PyQt.QtCore import Qt


class InfoDialog(QDialog):
    def __init__(self, instructions_path: str, parent=None, title="MTL Tools"):
        super().__init__(parent)

        self.setWindowTitle(title)
        self.setMinimumWidth(700)
        self.setMinimumHeight(550)

        layout = QVBoxLayout(self)

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

        layout.addWidget(browser)

        btn = QPushButton("Fechar")
        btn.clicked.connect(self.close)
        layout.addWidget(btn, alignment=Qt.AlignRight)

    def _markdown_to_html(self, text: str) -> str:
        """
        Conversão simples de Markdown para HTML
        Compatível com QGIS 3.16 (sem setMarkdown)
        """

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
