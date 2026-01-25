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

from ..utils.log_utils import LogUtilsOld
from ..utils.qgis_messagem_util import QgisMessageUtil
from ..utils.preferences import load_tool_prefs, save_tool_prefs
from ..utils.tool_keys import ToolKey
from ..plugins.base_plugin import BasePluginMTL
from ..utils.qgis_messagem_util import QgisMessageUtil
from ..utils.ui_widget_utils import  OldUiWidgetUtils
from ..utils.project_utils import  ProjectUtils
from ..utils.string_utils import StringUtils
from ..utils.vector.VectorLayerGeometry import VectorLayerGeometry
from ..core.config.LogUtils import LogUtils
from ..core.ui.WidgetFactory import WidgetFactory


class GerarRastroDialog(BasePluginMTL):
    #Essa é uma ferramenta de janela com geracao de produtos: do tipo vetoriais.
   
   
    TOOL_KEY = ToolKey.GERAR_RASTRO_IMPLEMENTO

    def __init__(self, iface):
        super().__init__(iface.mainWindow())
        self.iface = iface
        LogUtils.info("Inicializando diálogo Gerar Rastro Implemento", tool=self.TOOL_KEY)
        self.setWindowTitle("MTL Tools — Gerar Rastro Implemento")
        self.setMinimumWidth(360)
        icon_path = os.path.join(os.path.dirname(__file__), "..", "resources","icons", "gerar_rastro.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
            LogUtils.debug(f"Ícone carregado de: {icon_path}", tool=self.TOOL_KEY)

        LogUtils.debug("Construindo interface de usuário", tool=self.TOOL_KEY)
        self._build_ui()
        LogUtils.debug("Carregando preferências do usuário", tool=self.TOOL_KEY)
        self._load_prefs()
        LogUtils.info("Diálogo Gerar Rastro Implemento inicializado com sucesso", tool=self.TOOL_KEY)
        
        
    def _build_ui(self):
        # -------------------------------------------------------
        # LAYOUT
        # -------------------------------------------------------
        layout = QVBoxLayout()
        LogUtils.info("Construindo interface da ferramenta", tool=self.TOOL_KEY)


        #novo
        l1, self.layer_input = WidgetFactory.create_layer_input(
            label_text="Camada de Linhas (INPUT):",
            filters=[QgsMapLayerProxyModel.LineLayer],
            parent=self, separator_top=True
        )
        layout.addLayout(l1)

        LogUtils.debug("Componente de camada de entrada adicionado", tool=self.TOOL_KEY)

        # tamanhoimplemento
        h2, self.spin_tam = WidgetFactory.create_double_spin_input(
            "Tamanho implemento: (sempre em metros)"
        )
        layout.addLayout(h2)
        LogUtils.debug("Componente de tamanho de implemento adicionado", tool=self.TOOL_KEY)
        

        #---------------------------------------

        # salvar em arquivo ou temporário (campo único: arquivo completo)
   
        
        #novo
        save_layout, self.save_selector = WidgetFactory.create_save_file_selector(
            parent=self,
            file_filter=StringUtils.FILTER_VECTOR,
        )
        layout.addLayout(save_layout)
        LogUtils.debug("Componente de salvamento de arquivo adicionado", tool=self.TOOL_KEY)


        # aplicar estilo QML
        #novo
        qml_layout, self.qml_selector = WidgetFactory.create_qml_selector(
            parent=self
        )
        layout.addLayout(qml_layout)

        #----


        LogUtils.debug("Componente de estilo QML adicionado", tool=self.TOOL_KEY)      

        # instruções
        self.instructions_file = os.path.join(
            os.path.dirname(__file__),"..","resources", "instructions", "generate_trail_help.md"# Caminho do arquivo de instruções
        )      
         
        # buttons
        layout.addLayout(
            OldUiWidgetUtils.create_run_close_buttons(
                self.on_run,
                self.close,
                info_callback=lambda: self.show_info_dialog(
            "📘 Instruções – Gerar Rastro de Máquinas"
        )
            )
        )
        
        self.setLayout(layout)
        LogUtils.info("Interface da ferramenta construída com sucesso", tool=self.TOOL_KEY)

    def _load_prefs(self):
        LogUtils.debug("Carregando preferências salvas da ferramenta", tool=self.TOOL_KEY)
        prefs = load_tool_prefs(self.TOOL_KEY)
        last_tam = prefs.get('last_implement_length')
        save_to_folder = prefs.get('save_to_folder', False)
        last_file = prefs.get('last_output_file', '')
        apply_style = prefs.get('apply_style', False)
        last_qml = prefs.get('last_qml_path', '')
        self.qml_selector.set_qml_path(last_qml)
        self.qml_selector.set_enabled(bool(apply_style))

        if last_tam is not None:
            try:
                self.spin_tam.setValue(float(last_tam))
            except Exception:
                pass

        try:            
            self.save_selector.set_enabled(bool(save_to_folder))

            self.save_selector.set_qml_path(last_file)
            LogUtils.debug("Preferências carregadas e aplicadas com sucesso", tool=self.TOOL_KEY)
        except Exception as e:
            LogUtils.warning(f"Erro ao restaurar algumas preferências: {str(e)}", tool=self.TOOL_KEY)
        
    def _save_prefs(self):       
        LogUtils.debug("Salvando preferências da ferramenta", tool=self.TOOL_KEY)
        data = {}
        data['last_implement_length'] = float(self.spin_tam.value())
        data['save_to_folder'] = bool(self.save_selector.is_enabled())
        data['last_output_file'] = self.save_selector.get_qml_path()
        data['apply_style'] = bool(self.qml_selector.is_enabled())
        data['last_qml_path'] = self.qml_selector.get_qml_path()
        
        save_tool_prefs(self.TOOL_KEY, data)
        LogUtils.debug(f"Preferências salvas: tamanho={data['last_implement_length']}m, salvar_arquivo={data['save_to_folder']}", tool=self.TOOL_KEY)

    def on_run(self):
        LogUtils.info("Iniciando processamento: Gerar Rastro Implemento", tool=self.TOOL_KEY)
        layer = self.layer_input.current_layer()

        if not isinstance(layer, QgsVectorLayer):
            LogUtils.warning("Nenhuma camada de linhas válida selecionada", tool=self.TOOL_KEY)
            QgisMessageUtil.bar_warning(
                self.iface,
                "Selecione uma camada de linhas válida."
            )
            return
        #receber valores
        tam = float(self.spin_tam.value())
        save_to_folder = self.save_selector.get_qml_path()
        out_file = self.save_selector.get_qml_path() if save_to_folder else None
        only_selected = self.layer_input.only_selected_enabled()
        LogUtils.info(f"Parâmetros: camada='{layer.name()}', tamanho={tam}m, selecionadas={only_selected}, salvar_arquivo={save_to_folder}", tool=self.TOOL_KEY)
        
        # executar
        out_layer = self.run(
            layer,
            tam,
            only_selected=only_selected,
            save_to_folder=save_to_folder,
            output_path=out_file
        )

        # se cancelou ou falhou
        if out_layer is None:
            LogUtils.error("Processamento cancelado ou falhou", tool=self.TOOL_KEY)
            return

        # aplicar estilo (PADRÃO ÚNICO)  
        if self.qml_selector.is_enabled():
            qml = self.qml_selector.get_qml_path()
            if qml:
                LogUtils.info(f"Aplicando estilo QML: {qml}", tool=self.TOOL_KEY)
                self.apply_qml_style(out_layer, qml)
                LogUtils.debug("Estilo QML aplicado com sucesso", tool=self.TOOL_KEY)



        LogUtils.info("Processamento executado com sucesso", tool=self.TOOL_KEY)
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
        LogUtils.info("1/6] Resolvendo camada de entrada", tool=self.TOOL_KEY)
        layer = (
            input_layer
            if isinstance(input_layer, QgsVectorLayer)
            else QgsProject.instance().mapLayer(input_layer)
        )
        LogUtils.debug(f"Camada resolvida: {layer.name() if layer else 'None'}", tool=self.TOOL_KEY)
        
        if layer.crs().authid() == "EPSG:4326":
            original_tam = tamanhoimplemento
            tamanhoimplemento = tamanhoimplemento / 111120.0
            LogUtils.debug(f"CRS em WGS84 detectado. Tamanho convertido: {original_tam}m → {tamanhoimplemento:.6f}°", tool=self.TOOL_KEY)

        if not isinstance(layer, QgsVectorLayer):
            LogUtils.error("Camada de entrada inválida - não é QgsVectorLayer", tool=self.TOOL_KEY)
            QgisMessageUtil.modal_error(
                self.iface,
                "Camada de entrada inválida."
            )
            return None

        # -------------------------------------------------
        # 2) validar tipo
        # -------------------------------------------------
        LogUtils.info("2/6] Validando tipo de camada", tool=self.TOOL_KEY)
        layer_type = VectorLayerGeometry.get_layer_type(layer)
        LogUtils.debug(f"Tipo de camada detectado: {layer_type}", tool=self.TOOL_KEY)

        if layer_type != QgsWkbTypes.LineGeometry:
            LogUtils.error(f"Tipo de camada inválido. Esperado: LINE, Obtido: {layer_type}", tool=self.TOOL_KEY)
            QgisMessageUtil.modal_error(
                self.iface,
                "A camada de entrada deve ser do tipo LINHA."
            )
            return None
        LogUtils.debug("Camada validada como tipo LINE", tool=self.TOOL_KEY)

        # -------------------------------------------------
        # 3) somente selecionadas
        # -------------------------------------------------
        LogUtils.info("3/6] Processando seleção de feições", tool=self.TOOL_KEY)
        if only_selected:
            LogUtils.debug(f"Filtrando apenas feições selecionadas. Total selecionadas: {layer.selectedFeatureCount()}", tool=self.TOOL_KEY)
            layer_sel, err = VectorLayerGeometry.get_selected_features(layer)
            if err:
                LogUtils.error(f"Erro ao obter feições selecionadas: {err}", tool=self.TOOL_KEY)
                QgisMessageUtil.modal_error(self.iface, err)
                return None
            layer = layer_sel
            LogUtils.debug(f"Usando camada com feições selecionadas: {layer.name()}", tool=self.TOOL_KEY)
        else:
            LogUtils.debug(f"Processando todas as feições da camada. Total: {layer.featureCount()}", tool=self.TOOL_KEY)

        # -------------------------------------------------
        # 4) explode linhas
        # -------------------------------------------------
        LogUtils.info("4/6] Explodindo linhas em segmentos", tool=self.TOOL_KEY)
        LogUtils.debug(f"Iniciando explosão de {layer.featureCount()} feições...", tool=self.TOOL_KEY)
        
        exploded = VectorLayerGeometry.explode_multipart_features(
            layer=layer , external_tool_key=self.TOOL_KEY           
        )

        if exploded is None:
            LogUtils.error("Falha ao explodir linhas", tool=self.TOOL_KEY)
            QgisMessageUtil.modal_error(
                self.iface,
                "Falha ao explodir linhas."
            )
            return None
        
        LogUtils.debug(f"Linhas explodidas com sucesso. Total de segmentos: {exploded.featureCount()}", tool=self.TOOL_KEY)

        # -------------------------------------------------
        # 5) buffer (SEMPRE memory)
        # -------------------------------------------------
        LogUtils.info("5/6] Gerando buffer (rastro)", tool=self.TOOL_KEY)
        distance = float(tamanhoimplemento) / 2.0
        LogUtils.debug(f"Distância de buffer: {distance}m (metade do tamanho: {tamanhoimplemento}m)", tool=self.TOOL_KEY)

        buffer_layer = VectorLayerGeometry.create_buffer_geometry(
            layer=exploded,
            distance=distance,
            output_path=None,  # 👈 SEMPRE memory aqui            
        )

        if buffer_layer is None:
            LogUtils.error("Falha ao gerar buffer", tool=self.TOOL_KEY)
            QgisMessageUtil.modal_error(
                self.iface,
                "Falha ao gerar buffer."
            )
            return None
        
        LogUtils.debug(f"Buffer gerado com sucesso. Total de polígonos: {buffer_layer.featureCount()}", tool=self.TOOL_KEY)
        
        # -------------------------------------------------
        # 6) Salvar resultado
        # -------------------------------------------------
        LogUtils.info("6/6] Salvando resultado", tool=self.TOOL_KEY)
        result = self.save_vector_layer(buffer_layer, output_path, save_to_folder, output_name)
        
        if result:
            LogUtils.info(f"Rastro salvo com sucesso: {result.name()}", tool=self.TOOL_KEY)
        else:
            LogUtils.warning("Resultado em memória (camada não persistida)", tool=self.TOOL_KEY)
        
        return result
        

def run_gerar_rastro(iface):
    dlg = GerarRastroDialog(iface)
    dlg.setModal(False)
    dlg.show()
    return dlg  # 👈 ESSENCIAL

