# -*- coding: utf-8 -*-
import os

from qgis.PyQt.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QComboBox, QLineEdit,
    QFileDialog, QCheckBox, QMessageBox
)
from qgis.PyQt.QtGui import QIcon
from qgis.core import QgsProject

from ..utils.preferences import load_tool_prefs, save_tool_prefs
from ..utils.tool_keys import ToolKey
from ..utils.info_dialog import InfoDialog
from ..utils.log_utils import LogUtils


class BaseTool(QDialog):
    """
    Ferramenta base (template):
    - Lê camada vetorial
    - Campo texto livre
    - Leitura de pasta
    - Salva vetor em arquivo
    - Aplica QML opcional
    """

    TOOL_KEY = ToolKey.BASE_TOOL

    def __init__(self, iface):
        super().__init__(iface.mainWindow())
        self.iface = iface

        self.setWindowTitle("MTL Tools — Base Tool")
        self.setMinimumWidth(420)

        icon_path = os.path.join(os.path.dirname(__file__), "..", "resources","icons", "mtl_agro.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.instructions_file = os.path.join(
            os.path.dirname(__file__), "instructions", "base_tool.md"
        )

        self._build_ui()
        self._populate_layers()
        self._load_prefs()

    # --------------------------------------------------
    # UI
    # --------------------------------------------------
    def _build_ui(self):
        layout = QVBoxLayout()

        # INFO
        info_layout = QHBoxLayout()
        info_layout.addStretch()
        btn_info = QPushButton("ℹ️")
        btn_info.setFixedWidth(30)
        btn_info.clicked.connect(self.show_info)
        info_layout.addWidget(btn_info)
        layout.addLayout(info_layout)

        # Camada vetorial
        h_layer = QHBoxLayout()
        h_layer.addWidget(QLabel("Camada Vetorial:"))
        self.cmb_layer = QComboBox()
        h_layer.addWidget(self.cmb_layer)
        layout.addLayout(h_layer)

        # Campo texto
        h_text = QHBoxLayout()
        h_text.addWidget(QLabel("Texto livre:"))
        self.txt_text = QLineEdit()
        h_text.addWidget(self.txt_text)
        layout.addLayout(h_text)

        # Pasta
        h_folder = QHBoxLayout()
        h_folder.addWidget(QLabel("Pasta:"))
        self.txt_folder = QLineEdit()
        h_folder.addWidget(self.txt_folder)
        btn_folder = QPushButton("...")
        btn_folder.clicked.connect(self._pick_folder)
        h_folder.addWidget(btn_folder)
        layout.addLayout(h_folder)

        # Salvar arquivo
        self.chk_save = QCheckBox("Salvar resultado em arquivo")
        layout.addWidget(self.chk_save)

        h_out = QHBoxLayout()
        h_out.addWidget(QLabel("Arquivo de saída:"))
        self.txt_output = QLineEdit()
        h_out.addWidget(self.txt_output)
        btn_out = QPushButton("...")
        btn_out.clicked.connect(self._pick_output)
        h_out.addWidget(btn_out)
        layout.addLayout(h_out)

        # QML
        self.chk_qml = QCheckBox("Aplicar estilo QML")
        layout.addWidget(self.chk_qml)

        h_qml = QHBoxLayout()
        h_qml.addWidget(QLabel("QML:"))
        self.txt_qml = QLineEdit()
        h_qml.addWidget(self.txt_qml)
        btn_qml = QPushButton("...")
        btn_qml.clicked.connect(self._pick_qml)
        h_qml.addWidget(btn_qml)
        layout.addLayout(h_qml)

        # Botões
        h_btns = QHBoxLayout()
        h_btns.addStretch()
        btn_run = QPushButton("Executar")
        btn_run.clicked.connect(self.on_run)
        h_btns.addWidget(btn_run)
        btn_close = QPushButton("Fechar")
        btn_close.clicked.connect(self.close)
        h_btns.addWidget(btn_close)
        layout.addLayout(h_btns)

        self.setLayout(layout)

    # --------------------------------------------------
    def show_info(self):
        dlg = InfoDialog(self.instructions_file, self, "📘 Base Tool")
        dlg.exec()

    # --------------------------------------------------
    def _populate_layers(self):
        self.cmb_layer.clear()
        for lyr in QgsProject.instance().mapLayers().values():
            if hasattr(lyr, "wkbType"):
                self.cmb_layer.addItem(lyr.name(), lyr.id())

    # --------------------------------------------------
    def _load_prefs(self):
        prefs = load_tool_prefs(self.TOOL_KEY)
        self.txt_text.setText(prefs.get("text", ""))
        self.txt_folder.setText(prefs.get("folder", ""))
        self.txt_output.setText(prefs.get("output", ""))
        self.txt_qml.setText(prefs.get("qml", ""))
        self.chk_save.setChecked(prefs.get("save", False))
        self.chk_qml.setChecked(prefs.get("apply_qml", False))

        layer_id = prefs.get("layer_id")
        if layer_id:
            idx = self.cmb_layer.findData(layer_id)
            if idx != -1:
                self.cmb_layer.setCurrentIndex(idx)

    # --------------------------------------------------
    def _save_prefs(self):
        data = {
            "layer_id": self.cmb_layer.currentData(),
            "text": self.txt_text.text(),
            "folder": self.txt_folder.text(),
            "output": self.txt_output.text(),
            "qml": self.txt_qml.text(),
            "save": self.chk_save.isChecked(),
            "apply_qml": self.chk_qml.isChecked(),
        }
        save_tool_prefs(self.TOOL_KEY, data)

    def _pick_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Selecionar pasta",
            self.txt_folder.text() or os.path.expanduser("~")
        )
        if folder:
            self.txt_folder.setText(folder)
    def _pick_output(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Salvar arquivo de saída",
            self.txt_output.text() or os.path.expanduser("~"),
            "Shapefile (*.shp);;GeoPackage (*.gpkg)"
        )
        if path:
            self.txt_output.setText(path)
    def _pick_qml(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar arquivo QML",
            self.txt_qml.text() or os.path.expanduser("~"),
            "Estilo QGIS (*.qml)"
        )
        if path:
            self.txt_qml.setText(path)

    # --------------------------------------------------
    def on_run(self):
        try:
            layer_id = self.cmb_layer.currentData()
            if not layer_id:
                QMessageBox.warning(self, "Erro", "Selecione uma camada vetorial.")
                return

            self._save_prefs()

            # LOG
            LogUtils.log(self.TOOL_KEY, "Execução iniciada")
            LogUtils.log(self.TOOL_KEY, f"Layer ID: {layer_id}")
            LogUtils.log(self.TOOL_KEY, f"Salvar: {self.chk_save.isChecked()}")

            # PROCESSAMENTO FUTURO AQUI
            QMessageBox.information(self, "OK", "Ferramenta base executada com sucesso.")

        except Exception as e:
            LogUtils.exception(self.TOOL_KEY, e)
            QMessageBox.critical(self, "Erro", str(e))


# --------------------------------------------------
def run_base_tool(iface):
    dlg = BaseTool(iface)
    dlg.exec()
