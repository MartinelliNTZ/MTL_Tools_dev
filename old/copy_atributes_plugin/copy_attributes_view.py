# -*- coding: utf-8 -*-
import os
from qgis.PyQt.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QComboBox, QListWidget, QListWidgetItem, QCheckBox
)
from qgis.PyQt.QtCore import Qt
from qgis.core import QgsProject, QgsVectorLayer

from ...utils.log_utils import LogUtils
from ...utils.qgis_messagem_util import QgisMessageUtil
from ...utils.info_dialog import InfoDialog
from ..copy_attributes_plugin import CopyAttributesController


class CopyAttributesView(QDialog):

    TOOL_KEY = "copy_attributes"

    def __init__(self, iface):
        super().__init__(iface.mainWindow())
        self.iface = iface

        self.setWindowTitle("MTL Tools — Copiar Atributos entre Camadas")
        self.setMinimumWidth(420)

        layout = QVBoxLayout(self)

        # INFO
        info_bar = QHBoxLayout()
        info_bar.addStretch()
        btn_info = QPushButton("ℹ️")
        btn_info.setFixedWidth(30)
        btn_info.clicked.connect(self.show_info)
        info_bar.addWidget(btn_info)
        layout.addLayout(info_bar)

        self.instructions_file = os.path.join(
            os.path.dirname(__file__),
            "instructions",
            "copy_attributes_help.md"
        )

        # CAMADAS
        self.cmb_target = QComboBox()
        self.cmb_source = QComboBox()

        layout.addWidget(QLabel("Camada destino:"))
        layout.addWidget(self.cmb_target)
        layout.addWidget(QLabel("Camada origem:"))
        layout.addWidget(self.cmb_source)

        # ATRIBUTOS
        self.chk_all = QCheckBox("Usar todos os atributos")
        self.lst_fields = QListWidget()

        layout.addWidget(self.chk_all)
        layout.addWidget(self.lst_fields)

        # BOTÕES
        hb = QHBoxLayout()
        hb.addStretch()
        btn_run = QPushButton("Executar")
        btn_run.clicked.connect(self.on_run)
        btn_close = QPushButton("Fechar")
        btn_close.clicked.connect(self.close)
        hb.addWidget(btn_run)
        hb.addWidget(btn_close)
        layout.addLayout(hb)

        self._populate_layers()
        self.cmb_source.currentIndexChanged.connect(self._populate_fields)
        self.chk_all.toggled.connect(self.lst_fields.setDisabled)

    def show_info(self):
        InfoDialog(self.instructions_file, self, "📘 Instruções").exec()

    def _populate_layers(self):
        self.cmb_target.clear()
        self.cmb_source.clear()

        for lyr in QgsProject.instance().mapLayers().values():
            if isinstance(lyr, QgsVectorLayer):
                self.cmb_target.addItem(lyr.name(), lyr.id())
                self.cmb_source.addItem(lyr.name(), lyr.id())

        self._populate_fields()

    def _populate_fields(self):
        self.lst_fields.clear()
        layer = QgsProject.instance().mapLayer(self.cmb_source.currentData())
        if not layer:
            return

        for f in layer.fields():
            item = QListWidgetItem(f.name())
            item.setCheckState(Qt.Checked)
            self.lst_fields.addItem(item)

    def on_run(self):
        target = QgsProject.instance().mapLayer(self.cmb_target.currentData())
        source = QgsProject.instance().mapLayer(self.cmb_source.currentData())

        if not target or not source:
            return

        fields = None
        if not self.chk_all.isChecked():
            fields = [
                self.lst_fields.item(i).text()
                for i in range(self.lst_fields.count())
                if self.lst_fields.item(i).checkState() == Qt.Checked
            ]

        LogUtils.log(self.TOOL_KEY, "Iniciando cópia de atributos")

        model = CopyAttributesModel(self.iface)
        ok = model.run(target, source, fields)

        if ok:
            QgisMessageUtil.bar_success(
                self.iface,
                "Atributos processados com sucesso (alterações não salvas)"
            )
