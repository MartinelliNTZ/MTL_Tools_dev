import os
import re


from qgis.core import QgsProject, QgsLayoutExporter
from qgis.PyQt.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QCheckBox, QFileDialog, QLineEdit, QMessageBox, QProgressDialog
)
from qgis.PyQt.QtCore import QUrl, Qt, QCoreApplication
from qgis.PyQt.QtGui import QIcon

# Importações do sistema de preferências
from ..utils.preferences import load_tool_prefs, save_tool_prefs
from ..utils.info_dialog import InfoDialog
from ..utils import pdf_png_merge_utils as merge_utils
from ..utils.qgis_messagem_util import QgisMessageUtil
from ..utils.tool_keys import ToolKey




class ExportAllLayoutsDialog(QDialog):

    TOOL_KEY = ToolKey.EXPORT_ALL_LAYOUTS

    def __init__(self, iface):
        super().__init__(iface.mainWindow())
        self.iface = iface

        self.setWindowTitle("MTL Tools - Export All Layouts")
        self.setMinimumWidth(450)

        icon_path = os.path.join(os.path.dirname(__file__),"..", "resources","icons", "export_icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        layout = QVBoxLayout()
               # -------------------------------------------------------
        # INFO BUTTON (canto superior direito)
        # -------------------------------------------------------
        info_layout = QHBoxLayout()
        info_layout.addStretch()

        btn_info = QPushButton("ℹ️")
        btn_info.setFixedWidth(30)
        btn_info.clicked.connect(self.show_info)
        info_layout.addWidget(btn_info)
        # Caminho do arquivo de instruções
        self.instructions_file = os.path.join(
            os.path.dirname(__file__),"..","resources", "instructions", "export_all_layouts_help.md"
        )

        layout.addLayout(info_layout)

        # ---------------------------------------------------
        # CHECKBOXES
        # ---------------------------------------------------
        self.chk_pdf = QCheckBox("Exportar PDF")
        self.chk_png = QCheckBox("Exportar PNG")
        self.chk_merge_pdf = QCheckBox("Unir todos PDFs exportados em um PDF final")
        self.chk_merge_png = QCheckBox("Unir PNGs em um único PDF")
        self.chk_substituir = QCheckBox("Substituir arquivos existentes")

        # Defaults antes de carregar prefs
        self.chk_pdf.setChecked(True)
        self.chk_png.setChecked(True)

        layout.addWidget(self.chk_pdf)
        layout.addWidget(self.chk_png)
        layout.addWidget(self.chk_merge_pdf)
        layout.addWidget(self.chk_merge_png)
        layout.addWidget(self.chk_substituir)

        # Campo Max Width
        h_max = QHBoxLayout()
        self.txt_max_width = QLineEdit("3500")
        h_max.addWidget(QLabel("Max Width para unir PNG:"))
        h_max.addWidget(self.txt_max_width)
        layout.addLayout(h_max)

        # ---------------------------------------------------
        # Pasta de saída
        # ---------------------------------------------------
        h_pasta = QHBoxLayout()
        self.txt_pasta = QLineEdit()

        btn_pasta = QPushButton("Selecionar pasta")
        btn_pasta.clicked.connect(self.selecionar_pasta)

        btn_proj = QPushButton("Usar pasta do projeto")
        btn_proj.clicked.connect(self.definir_pasta_projeto)

        h_pasta.addWidget(QLabel("Pasta saída:"))
        h_pasta.addWidget(self.txt_pasta)
        h_pasta.addWidget(btn_pasta)
        h_pasta.addWidget(btn_proj)

        layout.addLayout(h_pasta)

        # ---------------------------------------------------
        # Exportar
        # ---------------------------------------------------
        btn_exportar = QPushButton("Exportar")
        btn_exportar.clicked.connect(self.exportar)
        layout.addWidget(btn_exportar)

        self.setLayout(layout)

        # 🔥 Carregar preferências:
        self.carregar_preferencias()
    # -------------------------------------------------------------
    #  INFO WINDOW
    # -------------------------------------------------------------
    def show_info(self):
        dlg = InfoDialog(self.instructions_file, self, "📘 Instruções – Exportar todos os layouts")
        dlg.exec()
    # ============================================================
    #  CARREGAR / SALVAR PREFERÊNCIAS
    # ============================================================
    def carregar_preferencias(self):

        prefs = load_tool_prefs(self.TOOL_KEY)

        self.chk_pdf.setChecked(prefs.get("chk_pdf", True))
        self.chk_png.setChecked(prefs.get("chk_png", True))
        self.chk_merge_pdf.setChecked(prefs.get("chk_merge_pdf", False))
        self.chk_merge_png.setChecked(prefs.get("chk_merge_png", False))
        self.chk_substituir.setChecked(prefs.get("chk_substituir", False))

        self.txt_max_width.setText(str(prefs.get("max_width", 3500)))

        pasta_default = os.path.join(QgsProject.instance().homePath(), "exports")
        self.txt_pasta.setText(prefs.get("pasta_saida", pasta_default))

    def salvar_preferencias(self):

        prefs = {
            "chk_pdf": self.chk_pdf.isChecked(),
            "chk_png": self.chk_png.isChecked(),
            "chk_merge_pdf": self.chk_merge_pdf.isChecked(),
            "chk_merge_png": self.chk_merge_png.isChecked(),
            "chk_substituir": self.chk_substituir.isChecked(),
            "max_width": int(self.txt_max_width.text()),
            "pasta_saida": self.txt_pasta.text().strip()
        }

        save_tool_prefs(self.TOOL_KEY, prefs)

    # ======================================================
    def definir_pasta_projeto(self):
        self.txt_pasta.setText(os.path.join(QgsProject.instance().homePath(), "exports"))

    def selecionar_pasta(self):
        pasta = QFileDialog.getExistingDirectory(self, "Escolha uma pasta")
        if pasta:
            self.txt_pasta.setText(pasta)

    # ======================================================
    # EXPORTAR
    # ======================================================
    def exportar(self):

        # 🔥 Salva prefs antes de qualquer coisa
        self.salvar_preferencias()

        export_pdf = self.chk_pdf.isChecked()
        export_png = self.chk_png.isChecked()
        merge_pdf = self.chk_merge_pdf.isChecked()
        merge_png = self.chk_merge_png.isChecked()
        substituir = self.chk_substituir.isChecked()

        max_width = int(self.txt_max_width.text())
        pasta = self.txt_pasta.text().strip()
        os.makedirs(pasta, exist_ok=True)

        project = QgsProject.instance()
        layouts = project.layoutManager().layouts()

        pdf_list = []
        png_list = []

        total = len(layouts)
        progress = QProgressDialog("Exportando layouts...", "Cancelar", 0, total, self)
        progress.setWindowModality(Qt.WindowModal)

        erros = []
        sucesso = 0

        for i, layout in enumerate(layouts):

            progress.setValue(i)
            QCoreApplication.processEvents()

            if progress.wasCanceled():
                break

            nome = re.sub(r'[<>:\"/\\|?*]', '', layout.name().strip())
            pdf_path = os.path.join(pasta, f"{nome}.pdf")
            png_path = os.path.join(pasta, f"{nome}.png")

            # Evitar sobrescrita
            if not substituir:
                base = nome
                count = 1
                while os.path.exists(pdf_path) or os.path.exists(png_path):
                    nome = f"{base}_{count}"
                    pdf_path = os.path.join(pasta, f"{nome}.pdf")
                    png_path = os.path.join(pasta, f"{nome}.png")
                    count += 1

            try:
                exporter = QgsLayoutExporter(layout)
                ok_pdf = ok_png = True

                if export_pdf:
                    r = exporter.exportToPdf(pdf_path, QgsLayoutExporter.PdfExportSettings())
                    ok_pdf = (r == QgsLayoutExporter.Success)
                    if ok_pdf:
                        pdf_list.append(pdf_path)

                if export_png:
                    r = exporter.exportToImage(png_path, QgsLayoutExporter.ImageExportSettings())
                    ok_png = (r == QgsLayoutExporter.Success)
                    if ok_png:
                        png_list.append(png_path)

                if ok_pdf and ok_png:
                    sucesso += 1
                else:
                    erros.append(nome)

            except Exception as e:
                erros.append(f"{nome} → {e}")

        progress.setValue(total)
        # =========================
        # VERIFICA DEPENDÊNCIAS (COM PERGUNTA AO USUÁRIO)
        # =========================

        # ----- PDF MERGE -----
        if merge_pdf and not merge_utils.HAS_PYPDF2:

            resp = QMessageBox.question(
                self,
                "Biblioteca necessária",
                "Para unir PDFs é necessário instalar o pacote PyPDF2.\n\nDeseja instalar agora?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )

            if resp == QMessageBox.Yes:
                cmd_path = os.path.join(os.path.dirname(__file__), "..", "lib", "install_pypdf2.bat")
                os.startfile(cmd_path)
                QMessageBox.information(
                    self,
                    "Instalação iniciada",
                    "Uma janela separada foi aberta para instalar PyPDF2.\n"
                    "Após concluir, reinicie o QGIS e execute novamente a união."
                )
                merge_pdf = False

            else:
                merge_pdf = False  # usuário recusou instalar


        # ----- PNG MERGE -----
        if merge_png and not merge_utils.HAS_PIL:

            resp = QMessageBox.question(
                self,
                "Biblioteca necessária",
                "Para unir PNGs em PDF é necessário instalar o pacote Pillow.\n\nDeseja instalar agora?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )

            if resp == QMessageBox.Yes:
                cmd_path = os.path.join(os.path.dirname(__file__), "..", "lib", "install_pillow.cmd")
                os.startfile(cmd_path)
                QMessageBox.information(
                    self,
                    "Instalação iniciada",
                    "Uma janela separada foi aberta para instalar Pillow.\n"
                    "Após concluir, reinicie o QGIS e execute novamente a união."
                )
                merge_png = False

            else:
                merge_png = False

        # =========================
        # UNIÃO
        # =========================
        if merge_pdf and pdf_list:
            ok, msg_text = merge_utils.merge_pdfs(
                pdf_list,
                os.path.join(pasta, "_PDF_UNICO_FINAL.pdf")
            )
            if not ok:
                erros.append(msg_text)

        if merge_png and png_list:
            ok, msg_text = merge_utils.merge_pngs_to_pdf(
                png_list,
                os.path.join(pasta, "_PNG_MERGED_FINAL.pdf"),
                max_width
            )
            if not ok:
                erros.append(msg_text)

        # MENSAGEM FINAL
        pasta_url = QUrl.fromLocalFile(pasta).toString()

        texto = ""
        if erros:
            texto += "<b>Erros:</b><br>" + "<br>".join(erros)
        texto += (
            f"<b>{sucesso}</b> layout(s) exportados com sucesso!<br><br>"
           
        )
        QgisMessageUtil.modal_result_with_folder(
            self.iface, "Exportação de Layouts Concluída", f"{texto}", pasta
        )
