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
            browser.document().setMarkdown(md_text)

        else:
            browser.setPlainText(
                f"Arquivo de instruções não encontrado:\n{instructions_path}"
            )

        layout.addWidget(browser)

        btn = QPushButton("Fechar")
        btn.clicked.connect(self.close)
        layout.addWidget(btn, alignment=Qt.AlignRight)
