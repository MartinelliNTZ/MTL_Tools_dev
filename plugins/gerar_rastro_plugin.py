# -*- coding: utf-8 -*-
from qgis.PyQt.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QDoubleSpinBox, QMessageBox, QCheckBox, QLineEdit, QFileDialog, 
)
from qgis.gui import QgsMapLayerComboBox
from qgis.core import QgsProject, QgsVectorLayer, QgsWkbTypes, QgsMapLayerProxyModel, QgsFeatureRequest
from qgis.PyQt.QtGui import QIcon
import os
from pathlib import Path
from typing import Optional
import time

from ..utils.log_utils import LogUtils
from ..utils.qgis_messagem_util import QgisMessageUtil
from ..utils.preferences import load_tool_prefs, save_tool_prefs
from ..utils.tool_keys import ToolKey
from ..plugins.base_plugin import BasePluginMTL
from ..utils.qgis_messagem_util import QgisMessageUtil
from ..utils.ui_widget_utils import  UiWidgetUtils
from ..utils.project_utils import  ProjectUtils
from ..utils.string_utils import StringUtils
from ..utils.vector_utils import VectorUtils


class GerarRastroDialog(BasePluginMTL):
    #Essa é uma ferramenta de janela com geracao de produtos: do tipo vetoriais.
   
   
    TOOL_KEY = ToolKey.GERAR_RASTRO_IMPLEMENTO

    def __init__(self, iface):
        super().__init__(iface.mainWindow())
        self.iface = iface
        self.setWindowTitle("MTL Tools — Gerar Rastro Implemento")
        self.setMinimumWidth(360)
        icon_path = os.path.join(os.path.dirname(__file__), "..", "icons", "gerar_rastro.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self._build_ui()
        self._load_prefs()
        
        
    def _build_ui(self):
        # -------------------------------------------------------
        # LAYOUT
        # -------------------------------------------------------
        layout = QVBoxLayout()


        # input layer
        layoutH1, self.cmb_layers, self.chk_only_selected = UiWidgetUtils.create_layer_input(
            "Camada de Linhas (INPUT):",[
            QgsMapLayerProxyModel.LineLayer]
        )
        layout.addLayout(layoutH1)

        # tamanhoimplemento
        h2, self.spin_tam = UiWidgetUtils.create_double_spin_input(
            "Tamanho implemento: (sempre em metros)"
        )
        layout.addLayout(h2)
        

        #---------------------------------------

        # salvar em arquivo ou temporário (campo único: arquivo completo)
        save_layout, self.chk_save_file, self.txt_output_file = (
            UiWidgetUtils.create_save_file_selector(
                parent=self
            )
        )
        layout.addLayout(save_layout)

        # aplicar estilo QML
        h_qml, self.chk_apply_style, self.txt_qml = UiWidgetUtils.create_qml_selector(
            parent=self
        )
        layout.addLayout(h_qml)      

        # instruções
        self.instructions_file = os.path.join(
            os.path.dirname(__file__), "instructions", "generate_trail_help.md"# Caminho do arquivo de instruções
        )      
         
        # buttons
        layout.addLayout(
            UiWidgetUtils.create_run_close_buttons(
                self.on_run,
                self.close,
                info_callback=lambda: self.show_info_dialog(
            "📘 Instruções – Gerar Rastro de Máquinas"
        )
            )
        )
        
        self.setLayout(layout)

    def _load_prefs(self):
        prefs = load_tool_prefs(self.TOOL_KEY)
        last_id = prefs.get('last_input_layer_id')
        last_tam = prefs.get('last_tamanhoimplemento')
        save_to_folder = prefs.get('save_to_folder', False)
        last_file = prefs.get('last_output_file', '')
        apply_style = prefs.get('apply_style', False)
        last_qml = prefs.get('last_qml_path', '')
        if last_tam is not None:
            try:
                self.spin_tam.setValue(float(last_tam))
            except Exception:
                pass
        if last_id:
            layer = QgsProject.instance().mapLayer(last_id)
            if layer:
                self.cmb_layers.setLayer(layer)

        try:
            self.chk_save_file.setChecked(bool(save_to_folder))
            self.txt_output_file.setText(last_file)
            self.chk_apply_style.setChecked(bool(apply_style))
            self.txt_qml.setText(last_qml)
        except Exception:
            pass
        

    def _save_prefs(self):       
        layer = self.cmb_layers.currentLayer()
        data = {
            'last_input_layer_id': layer.id() if layer else None,
            'last_tamanhoimplemento': float(self.spin_tam.value())
        }
        data['save_to_folder'] = bool(self.chk_save_file.isChecked())
        data['last_output_file'] = self.txt_output_file.text().strip()
        data['apply_style'] = bool(self.chk_apply_style.isChecked())
        data['last_qml_path'] = self.txt_qml.text().strip()
        
        save_tool_prefs(self.TOOL_KEY, data)

    def on_run(self):
        layer = self.cmb_layers.currentLayer()

        if not isinstance(layer, QgsVectorLayer):
            QgisMessageUtil.bar_warning(
                self.iface,
                "Selecione uma camada de linhas válida."
            )
            return

        tam = float(self.spin_tam.value())
        save_to_folder = self.chk_save_file.isChecked()
        out_file = self.txt_output_file.text().strip() if save_to_folder else None
        only_selected = self.chk_only_selected.isChecked()

        out_layer = self.run(
            layer,
            tam,
            only_selected=only_selected,
            save_to_folder=save_to_folder,
            output_path=out_file
        )

        # se cancelou ou falhou
        if out_layer is None:
            return

        # aplicar estilo (PADRÃO ÚNICO)
        if self.chk_apply_style.isChecked():
            qml = self.txt_qml.text().strip()
            if qml:
                self.apply_qml_style(out_layer, qml)


        QgisMessageUtil.bar_success(
            self.iface,
            "Processamento executado com sucesso."
        )

        self._save_prefs()

          
    def run(
        self,
        input_layer,
        tamanhoimplemento: float,
        *,
        save_to_folder: bool = False,
        output_path: Optional[str] = None,
        output_name: str = "Rastro_Implemento",
        only_selected: bool = False,
        feedback=None
    ) -> Optional[QgsVectorLayer]:


        # -------------------------------------------------
        # 1) resolver camada
        # -------------------------------------------------
        layer = (
            input_layer
            if isinstance(input_layer, QgsVectorLayer)
            else QgsProject.instance().mapLayer(input_layer)
        )
        if layer.crs().authid() == "EPSG:4326":
            tamanhoimplemento = tamanhoimplemento / 111120.0

        if not isinstance(layer, QgsVectorLayer):
            QgisMessageUtil.modal_error(
                self.iface,
                "Camada de entrada inválida."
            )
            return None

        # -------------------------------------------------
        # 2) validar tipo
        # -------------------------------------------------
        if VectorUtils.get_layer_type(layer) != VectorUtils.TYPE_LINE:
            QgisMessageUtil.modal_error(
                self.iface,
                "A camada de entrada deve ser do tipo LINHA."
            )
            return None

        # -------------------------------------------------
        # 3) somente selecionadas
        # -------------------------------------------------
        if only_selected:
            layer_sel, err = VectorUtils.get_selected_features(layer)
            if err:
                QgisMessageUtil.modal_error(self.iface, err)
                return None
            layer = layer_sel

        # -------------------------------------------------
        # 4) explode linhas
        # -------------------------------------------------
        exploded = VectorUtils.explode_lines(
            layer=layer,
            feedback=feedback
        )

        if exploded is None:
            QgisMessageUtil.modal_error(
                self.iface,
                "Falha ao explodir linhas."
            )
            return None

        # -------------------------------------------------
        # 5) buffer (SEMPRE memory)
        # -------------------------------------------------
        distance = float(tamanhoimplemento) / 2.0

        buffer_layer = VectorUtils.buffer_layer(
            layer=exploded,
            distance=distance,
            output_path=None,  # 👈 SEMPRE memory aqui
            feedback=feedback
        )

        if buffer_layer is None:
            QgisMessageUtil.modal_error(
                self.iface,
                "Falha ao gerar buffer."
            )
            return None
        return self.save_vector_layer(buffer_layer, output_path, save_to_folder, output_name)
        

def run_gerar_rastro(iface):
    dlg = GerarRastroDialog(iface)
    dlg.setModal(False)
    dlg.show()
    return dlg  # 👈 ESSENCIAL

