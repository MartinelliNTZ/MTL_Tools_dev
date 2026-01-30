# -*- coding: utf-8 -*-
from qgis.PyQt.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QDoubleSpinBox, QMessageBox, QCheckBox, QLineEdit, QFileDialog, 
)
from qgis.gui import QgsMapLayerComboBox
from qgis.core import QgsProject, QgsVectorLayer, QgsWkbTypes, QgsMapLayerProxyModel, QgsFeatureRequest, QgsApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtCore import Qt
import os
from pathlib import Path
from typing import Optional
import tempfile

from ..utils.vector.VectorLayerSource import VectorLayerSource

from ..utils.qgis_messagem_util import QgisMessageUtil
from ..utils.preferences import load_tool_prefs, save_tool_prefs
from ..utils.tool_keys import ToolKey
from ..plugins.base_plugin import BasePluginMTL
from ..utils.qgis_messagem_util import QgisMessageUtil
from ..utils.project_utils import  ProjectUtils
from ..utils.string_utils import StringUtils
from ..utils.vector.VectorLayerGeometry import VectorLayerGeometry
from ..core.config.LogUtils import LogUtils
from ..core.ui.WidgetFactory import WidgetFactory
from ..core.task.ExplodeHugeLayerTask import ExplodeHugeLayerTask


class GerarRastroDialog(BasePluginMTL):
    #Essa é uma ferramenta de janela com geracao de produtos: do tipo vetoriais.
   
   
    TOOL_KEY = ToolKey.GERAR_RASTRO_IMPLEMENTO

    def __init__(self, iface):
        super().__init__(iface.mainWindow())        
        self.iface = iface
        LogUtils.log("Inicializando diálogo Gerar Rastro Implemento", level="INFO", tool=self.TOOL_KEY)  
        LogUtils.log("Construindo interface de usuário", level="DEBUG", tool=self.TOOL_KEY, class_name="GerarRastroDialog")
        self._build_ui()
        LogUtils.log("Carregando preferências do usuário", level="DEBUG", tool=self.TOOL_KEY, class_name="GerarRastroDialog")
        self._load_prefs()
        LogUtils.log("Diálogo Gerar Rastro Implemento inicializado com sucesso", level="INFO", tool=self.TOOL_KEY, class_name="GerarRastroDialog")
        self._tasks = []

        
        
    def _build_ui(self):
        super()._build_ui(title = "Gerar Rastro de Máquinas",icon_path="gerar_rastro.ico",instructions_file="generate_trail_help.md")  
        LogUtils.log("Construindo interface da ferramenta", level="INFO", tool=self.TOOL_KEY, class_name="GerarRastroDialog")


        #novo
        layer_layout, self.layer_input = WidgetFactory.create_layer_input(
            label_text="Camada de Linhas (INPUT):",
            filters=[QgsMapLayerProxyModel.LineLayer],
            parent=self,
            allow_empty=False
        )
        LogUtils.log("Componente de camada de entrada adicionado", level="DEBUG", tool=self.TOOL_KEY, class_name="GerarRastroDialog")

        # tamanhoimplemento
        tam_layout, self.spin_tam = WidgetFactory.create_double_spin_input(
            "Tamanho implemento: (sempre em metros)",separator_bottom=False,
        )
        LogUtils.log("Componente de tamanho de implemento adicionado", level="DEBUG", tool=self.TOOL_KEY, class_name="GerarRastroDialog")
        

        #---------------------------------------

        # salvar em arquivo ou temporário (campo único: arquivo completo)
        save_layout, self.save_selector = WidgetFactory.create_save_file_selector(
            parent=self,            file_filter=StringUtils.FILTER_VECTOR,            separator_top=True
        )
        LogUtils.log("Componente de salvamento de arquivo adicionado", level="DEBUG", tool=self.TOOL_KEY, class_name="GerarRastroDialog")


        # aplicar estilo QML
        qml_layout, self.qml_selector = WidgetFactory.create_qml_selector(            parent=self        )       
        LogUtils.log("Componente de estilo QML adicionado", level="DEBUG", tool=self.TOOL_KEY, class_name="GerarRastroDialog")     

        # buttons
        buttons_layout, self.action_buttons = WidgetFactory.create_bottom_action_buttons(
            parent=self,            run_callback=self.on_run,            close_callback=self.close, 
            info_callback=self.show_info_dialog,            tool_key=self.TOOL_KEY,        ) 
        
        #-----------------------------------------------------------------------       
        self.layout.add_items([layer_layout,tam_layout, save_layout, qml_layout,  buttons_layout])
        self.setLayout(self.layout)
        LogUtils.log("Interface da ferramenta construída com sucesso", level="INFO", tool=self.TOOL_KEY, class_name="GerarRastroDialog")

    def _load_prefs(self):
        LogUtils.log(f"Carregando preferências salvas da ferramenta. Self={self}", level="DEBUG", tool=self.TOOL_KEY, class_name="GerarRastroDialog")
        prefs = load_tool_prefs(self.TOOL_KEY)
        last_tam = prefs.get('last_implement_length')
        save_to_folder = prefs.get('save_to_folder', False)
        last_file = prefs.get('last_output_file', '')
        apply_style = prefs.get('apply_style', False)
        last_qml = prefs.get('last_qml_path', '')
        self.qml_selector.set_file_path(last_qml)
        self.qml_selector.set_enabled(bool(apply_style))

        if last_tam is not None:
            try:
                self.spin_tam.setValue(float(last_tam))
            except Exception:
                pass

        try:            
            self.save_selector.set_enabled(bool(save_to_folder))

            self.save_selector.set_file_path(last_file)
            LogUtils.log("Preferências carregadas e aplicadas com sucesso", level="DEBUG", tool=self.TOOL_KEY, class_name="GerarRastroDialog")
        except Exception as e:
            LogUtils.log(f"Erro ao restaurar algumas preferências: {str(e)}", level="WARNING", tool=self.TOOL_KEY, class_name="GerarRastroDialog")
        
    def _save_prefs(self):       
        LogUtils.log("Salvando preferências da ferramenta", level="DEBUG", tool=self.TOOL_KEY, class_name="GerarRastroDialog")
        data = {}
        data['last_implement_length'] = float(self.spin_tam.value())
        data['save_to_folder'] = bool(self.save_selector.is_enabled())
        data['last_output_file'] = self.save_selector.get_file_path()
        data['apply_style'] = bool(self.qml_selector.is_enabled())
        data['last_qml_path'] = self.qml_selector.get_file_path()
        
        save_tool_prefs(self.TOOL_KEY, data)
        LogUtils.log(f"Preferências salvas: tamanho={data['last_implement_length']}m, salvar_arquivo={data['save_to_folder']}", level="DEBUG", tool=self.TOOL_KEY, class_name="GerarRastroDialog")

    def on_run(self):
        self._save_prefs()
        LogUtils.log("Iniciando processamento: Gerar Rastro Implemento", level="INFO", tool=self.TOOL_KEY, class_name="GerarRastroDialog")
        layer = self.layer_input.current_layer()

        if not isinstance(layer, QgsVectorLayer):
            LogUtils.log("Nenhuma camada de linhas válida selecionada", level="WARNING", tool=self.TOOL_KEY, class_name="GerarRastroDialog")
            QgisMessageUtil.bar_warning(                self.iface,                "Selecione uma camada de linhas válida."            )
            return
        #receber valores
        tam = float(self.spin_tam.value())
        save_to_folder = self.save_selector.is_enabled()
        out_file = self.save_selector.get_file_path().strip() if save_to_folder else ""
        
        # Validar: output_path deve ser None se não for um caminho válido
        # (vazio, começa com "memory", ou contém caracteres inválidos de caminho)
        if save_to_folder and out_file and not out_file.startswith("memory"):
            output_path = out_file
        else:
            save_to_folder = False  # Forçar salvar em memória se arquivo inválido
            output_path = None
        
        only_selected = self.layer_input.only_selected_enabled()
        LogUtils.log(f"Parâmetros: camada='{layer.name()}', tamanho={tam}m, selecionadas={only_selected}, salvar_arquivo={save_to_folder}", level="INFO", tool=self.TOOL_KEY, class_name="GerarRastroDialog")
        
        # executar
        out_layer = self.run(
            layer,
            tam,
            only_selected=only_selected,
            save_to_folder=save_to_folder,
            output_path=output_path
        )

        # se cancelou ou falhou
        if out_layer is None:
            LogUtils.log(
                "Processamento iniciado em background",
                level="INFO", tool=self.TOOL_KEY, class_name="GerarRastroDialog"
            )
            return

        # aplicar estilo (PADRÃO ÚNICO)  
        if self.qml_selector.is_enabled():
            qml = self.qml_selector.get_file_path()
            if qml:
                LogUtils.log(f"Aplicando estilo QML: {qml}", level="INFO", tool=self.TOOL_KEY, class_name="GerarRastroDialog")
                self.apply_qml_style(out_layer, qml)
                LogUtils.log("Estilo QML aplicado com sucesso", level="DEBUG", tool=self.TOOL_KEY, class_name="GerarRastroDialog")



        LogUtils.log("Processamento executado com sucesso", level="INFO", tool=self.TOOL_KEY, class_name="GerarRastroDialog")
        QgisMessageUtil.bar_success(
            self.iface,
            "Processamento executado com sucesso."
        )

        self._save_prefs()
        
    def _resolve_input_layer(self, input_layer, tamanhoimplemento: float) -> tuple[Optional[QgsVectorLayer], float]:
        """Etapa 1: Resolver camada de entrada e converter tamanho se necessário"""
        LogUtils.log("1/6] Resolvendo camada de entrada", level="INFO", tool=self.TOOL_KEY, class_name="GerarRastroDialog")
        layer = (
            input_layer
            if isinstance(input_layer, QgsVectorLayer)
            else QgsProject.instance().mapLayer(input_layer)
        )
        LogUtils.log(f"Camada resolvida: {layer.name() if layer else 'None'}", level="DEBUG", tool=self.TOOL_KEY, class_name="GerarRastroDialog")
        
        if layer.crs().authid() == "EPSG:4326":
            original_tam = tamanhoimplemento
            tamanhoimplemento = tamanhoimplemento / 111120.0
            LogUtils.log(f"CRS em WGS84 detectado. Tamanho convertido: {original_tam}m → {tamanhoimplemento:.6f}°", level="DEBUG", tool=self.TOOL_KEY, class_name="GerarRastroDialog")

        if not isinstance(layer, QgsVectorLayer):
            LogUtils.log("Camada de entrada inválida - não é QgsVectorLayer", level="ERROR", tool=self.TOOL_KEY, class_name="GerarRastroDialog")
            QgisMessageUtil.modal_error(
                self.iface,
                "Camada de entrada inválida."
            )
            return None, tamanhoimplemento
        
        return layer, tamanhoimplemento

    def _validate_layer_type(self, layer: QgsVectorLayer) -> bool:
        """Etapa 2: Validar tipo de camada (deve ser LINE)"""
        LogUtils.log("2/6] Validando tipo de camada", level="INFO", tool=self.TOOL_KEY, class_name="GerarRastroDialog")
        layer_type = VectorLayerGeometry.get_layer_type(layer)
        LogUtils.log(f"Tipo de camada detectado: {layer_type}", level="DEBUG", tool=self.TOOL_KEY, class_name="GerarRastroDialog")

        if layer_type != QgsWkbTypes.LineGeometry:
            LogUtils.log(f"Tipo de camada inválido. Esperado: LINE, Obtido: {layer_type}", level="ERROR", tool=self.TOOL_KEY, class_name="GerarRastroDialog")
            QgisMessageUtil.modal_error(
                self.iface,
                "A camada de entrada deve ser do tipo LINHA."
            )
            return False
        LogUtils.log("Camada validada como tipo LINE", level="DEBUG", tool=self.TOOL_KEY, class_name="GerarRastroDialog")
        return True

    def _process_selection(self, layer: QgsVectorLayer, only_selected: bool) -> Optional[QgsVectorLayer]:
        """Etapa 3: Processar seleção de feições"""
        LogUtils.log("3/6] Processando seleção de feições", level="INFO", tool=self.TOOL_KEY, class_name="GerarRastroDialog")
        if only_selected:
            LogUtils.log(f"Filtrando apenas feições selecionadas. Total selecionadas: {layer.selectedFeatureCount()}", level="DEBUG", tool=self.TOOL_KEY, class_name="GerarRastroDialog")
            layer_sel, err = VectorLayerGeometry.get_selected_features(layer)
            if err:
                LogUtils.log(f"Erro ao obter feições selecionadas: {err}", level="ERROR", tool=self.TOOL_KEY, class_name="GerarRastroDialog")
                QgisMessageUtil.modal_error(self.iface, err)
                return None
            layer = layer_sel
            LogUtils.log(f"Usando camada com feições selecionadas: {layer.name()}", level="DEBUG", tool=self.TOOL_KEY, class_name="GerarRastroDialog")
        else:
            LogUtils.log(f"Processando todas as feições da camada. Total: {layer.featureCount()}", level="DEBUG", tool=self.TOOL_KEY, class_name="GerarRastroDialog")
        
        return layer

    def _explode_lines(self, layer: QgsVectorLayer) -> Optional[QgsVectorLayer]:
        """Etapa 4: Explodir linhas em segmentos"""
        LogUtils.log("4/6] Explodindo linhas em segmentos", level="INFO", tool=self.TOOL_KEY, class_name="GerarRastroDialog")
        LogUtils.log(f"Iniciando explosão de {layer.featureCount()} feições...", level="DEBUG", tool=self.TOOL_KEY, class_name="GerarRastroDialog")
        
        exploded = VectorLayerGeometry.explode_multipart_features(
            layer=layer , external_tool_key=self.TOOL_KEY           
        )

        if exploded is None:
            LogUtils.log("Falha ao explodir linhas", level="ERROR", tool=self.TOOL_KEY, class_name="GerarRastroDialog")
            QgisMessageUtil.modal_error(
                self.iface,
                "Falha ao explodir linhas."
            )
            return None
        
        LogUtils.log(f"Linhas explodidas com sucesso. Total de segmentos: {exploded.featureCount()}", level="DEBUG", tool=self.TOOL_KEY, class_name="GerarRastroDialog")
        return exploded

    def _generate_buffer(self, exploded: QgsVectorLayer, tamanhoimplemento: float) -> Optional[QgsVectorLayer]:
        """Etapa 5: Gerar buffer (rastro)"""
        LogUtils.log("5/6] Gerando buffer (rastro)", level="INFO", tool=self.TOOL_KEY, class_name="GerarRastroDialog")
        distance = float(tamanhoimplemento) / 2.0
        LogUtils.log(f"Distância de buffer: {distance}m (metade do tamanho: {tamanhoimplemento}m)", level="DEBUG", tool=self.TOOL_KEY, class_name="GerarRastroDialog")

        buffer_layer = VectorLayerGeometry.create_buffer_geometry(
            layer=exploded,
            distance=distance,
            output_path=None,  # 👈 SEMPRE memory aqui            
        )

        if buffer_layer is None:
            LogUtils.log("Falha ao gerar buffer", level="ERROR", tool=self.TOOL_KEY, class_name="GerarRastroDialog")
            QgisMessageUtil.modal_error(
                self.iface,
                "Falha ao gerar buffer."
            )
            return None
        
        LogUtils.log(f"Buffer gerado com sucesso. Total de polígonos: {buffer_layer.featureCount()}", level="DEBUG", tool=self.TOOL_KEY, class_name="GerarRastroDialog")
        return buffer_layer

    def _save_result(self, buffer_layer: QgsVectorLayer, output_path: Optional[str], save_to_folder: bool, output_name: str) -> Optional[QgsVectorLayer]:
        """Etapa 6: Salvar resultado"""
        LogUtils.log("6/6] Salvando resultado", level="INFO", tool=self.TOOL_KEY, class_name="GerarRastroDialog")
        result = self.save_vector_layer(buffer_layer, output_path, save_to_folder, output_name)
        
        if result:
            LogUtils.log(f"Rastro salvo com sucesso: {result.name()}", level="INFO", tool=self.TOOL_KEY, class_name="GerarRastroDialog")
        else:
            LogUtils.log("Resultado em memória (camada não persistida)", level="WARNING", tool=self.TOOL_KEY, class_name="GerarRastroDialog")
        
        return result

    def run(
        self,
        input_layer,
        tamanhoimplemento: float,
        *,
        save_to_folder: bool = False,
        output_path: Optional[str] = None,
        output_name: str = "Rastro_Implemento",
        only_selected: bool = False,
    ) -> Optional[QgsVectorLayer]:

        # Etapa 1: Resolver camada
        layer, tamanhoimplemento = self._resolve_input_layer(input_layer, tamanhoimplemento)
        if layer is None:
            return None

        # Etapa 2: Validar tipo
        if not self._validate_layer_type(layer):
            return None

        # Etapa 3: Processar seleção
        layer = self._process_selection(layer, only_selected)
        if layer is None:
            return None
        
        # Etapa 4: Explodir linhas (ASYNC)
        self._explode_lines_async(
            layer=layer,
            tamanhoimplemento=tamanhoimplemento,
            output_path=output_path,
            save_to_folder=save_to_folder,
            output_name=output_name,
        )

        return None  # fluxo continua no callback

    def _load_exploded_layer(self, path: str) -> Optional[QgsVectorLayer]:
        if not path or not os.path.exists(path):
            LogUtils.log(
                f"Arquivo explodido não encontrado: {path}",
                level="ERROR",
                tool=self.TOOL_KEY,
                class_name="GerarRastroDialog"
            )
            return None

        layer = QgsVectorLayer(path, "exploded_lines", "ogr")
        if not layer.isValid():
            LogUtils.log(
                f"Camada explodida inválida: {path}",
                level="ERROR",
                tool=self.TOOL_KEY,
                class_name="GerarRastroDialog"
            )
            return None

        LogUtils.log(
            f"Camada explodida carregada com sucesso: {layer.featureCount()} feições",
            level="DEBUG",
            tool=self.TOOL_KEY,
            class_name="GerarRastroDialog"
        )
        return layer

    def _explode_lines_async(
        self,
        layer: QgsVectorLayer,
        tamanhoimplemento: float,
        output_path: Optional[str],
        save_to_folder: bool,
        output_name: str,
    ) -> None:

        """Etapa 4: Explodir linhas em segmentos (ASYNC)"""

        LogUtils.log(
            "4/6] Explodindo linhas em segmentos (async)",
            level="INFO",
            tool=self.TOOL_KEY,
            class_name="GerarRastroDialog"
        )

        tmp_dir = tempfile.mkdtemp(prefix="explode_")
        input_path = os.path.join(tmp_dir, "input.gpkg")
        output_path = os.path.join(tmp_dir, "exploded.gpkg")

        input_path = VectorLayerSource.save_vector_layer_to_file(
            layer=layer,
            output_path=input_path,
            decision="overwrite",
            external_tool_key=self.TOOL_KEY
        )
        LogUtils.log(
                f"Camada de entrada exportada para arquivo temporário: {input_path}, output_path={output_path}, tmp_dir={tmp_dir}",
                level="DEBUG",
                tool=self.TOOL_KEY,
                class_name="GerarRastroDialog"
            )

        if input_path is None:
            LogUtils.log(
                "Falha ao exportar camada de entrada para processamento",
                level="CRITICAL",
                tool=self.TOOL_KEY,
                class_name="GerarRastroDialog"
            )
            return None

        task = ExplodeHugeLayerTask(
            input_path=input_path,
            output_path=output_path,
            tool_key=self.TOOL_KEY
        )
        


        task.on_success = lambda out_path: self._continue_after_explode(
            exploded=self._load_exploded_layer(out_path),
            tamanhoimplemento=tamanhoimplemento,
            output_path=output_path,
            save_to_folder=save_to_folder,
            output_name=output_name
        )
        task.on_error = lambda exc: QgisMessageUtil.modal_error(
            self.iface,
            f"Falha ao explodir linhas:\n{exc}"
        )
        self._tasks.append(task)  
        QgsApplication.taskManager().addTask(task)    
        
    def _continue_after_explode(
        self,
        exploded: Optional[QgsVectorLayer],
        tamanhoimplemento: float,
        output_path: Optional[str],
        save_to_folder: bool,
        output_name: str
    ):
        if exploded is None:
            QgisMessageUtil.modal_error(
                self.iface,
                "Falha ao carregar camada explodida."
            )
            return


        LogUtils.log(
            "Explosão concluída, continuando processamento",
            level="INFO",
            tool=self.TOOL_KEY,
            class_name="GerarRastroDialog"
        )

        buffer_layer = self._generate_buffer(exploded, tamanhoimplemento)
        if buffer_layer is None:
            return

        result = self._save_result(
            buffer_layer,
            output_path,
            save_to_folder,
            output_name
        )

        if result:
            QgisMessageUtil.bar_success(
                self.iface,
                "Processamento executado com sucesso."
            )


def run_gerar_rastro(iface):
    dlg = GerarRastroDialog(iface)
    dlg.setModal(False)
    dlg.show()
    return dlg  # 👈 ESSENCIAL

