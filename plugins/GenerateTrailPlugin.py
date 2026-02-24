# -*- coding: utf-8 -*-
from qgis.core import QgsProject, QgsVectorLayer, QgsWkbTypes, QgsMapLayerProxyModel, QgsApplication
from typing import Optional, Tuple
from ..plugins.BasePlugin import BasePluginMTL
from ..utils.qgis_messagem_util import QgisMessageUtil
from ..utils.string_utils import StringUtils
from ..utils.vector.VectorLayerGeometry import VectorLayerGeometry
from ..utils.vector.VectorLayerProjection import VectorLayerProjection
from ..utils.vector.VectorLayerSource import VectorLayerSource
from ..utils.preferences import load_tool_prefs, save_tool_prefs
from ..utils.tool_keys import ToolKey
from ..core.config.LogUtils import LogUtils
from ..core.ui.WidgetFactory import WidgetFactory
from ..core.engine_tasks.AsyncPipelineEngine import AsyncPipelineEngine
from ..core.engine_tasks.BufferStep import BufferStep
from ..core.engine_tasks.ExecutionContext import ExecutionContext
from ..core.engine_tasks.ExplodeStep import ExplodeStep
from ..core.engine_tasks.SaveVectorStep import SaveVectorStep



class GenerateTrailPlugin(BasePluginMTL):
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
            parent=self,            run_callback=self.execute_tool,            close_callback=self.close, 
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

    def execute_tool(self):
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
        
    def _resolve_input_layer(self, input_layer, tamanhoimplemento: float) -> Tuple[Optional[QgsVectorLayer], float]:
        """Etapa 1: Resolver camada de entrada e converter tamanho se necessário"""
        layer = (
            input_layer
            if isinstance(input_layer, QgsVectorLayer)
            else QgsProject.instance().mapLayer(input_layer)
        )
        LogUtils.log(f"Camada resolvida: {layer.name() if layer else 'None'}", level="DEBUG", tool=self.TOOL_KEY, class_name="GerarRastroDialog")
        tamanhoimplemento = VectorLayerProjection.convert_distance_to_layer_units(
            layer,
            tamanhoimplemento
        )
        if not isinstance(layer, QgsVectorLayer):
            LogUtils.log("Camada de entrada inválida - não é QgsVectorLayer", level="ERROR", tool=self.TOOL_KEY, class_name="GerarRastroDialog")
            QgisMessageUtil.modal_error(
                self.iface,
                "Camada de entrada inválida."
            )
            return None, tamanhoimplemento
        
        return layer, tamanhoimplemento

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

        layer, tamanhoimplemento = self._resolve_input_layer(input_layer, tamanhoimplemento)
        if layer is None:
            return None

        ok, error = VectorLayerSource.validate_layer(
            layer,
            expected_geometry=QgsWkbTypes.LineGeometry
        )

        if not ok:
            QgisMessageUtil.modal_error(self.iface, error)
            return None

        layer = self._process_selection(layer, only_selected)
        if layer is None:
            return None
        

        context = ExecutionContext()
        context.set("layer", layer)
        context.set("tamanhoimplemento", tamanhoimplemento)
        context.set("save_to_folder", save_to_folder)
        context.set("output_path", output_path)
        context.set("output_name", output_name)
        context.set("tool_key", self.TOOL_KEY)

        buffer_distance = float(tamanhoimplemento) / 2.0

        context.set("buffer_distance", buffer_distance)
        context.set("buffer_dissolve", False)

        engine = AsyncPipelineEngine(
            steps=[
                ExplodeStep(),
                BufferStep(),
                SaveVectorStep()
            ],
            context=context,
          #  iface=self.iface,
            on_finished=self._on_pipeline_finished,
            on_error=self._on_pipeline_error
        )

        engine.start()
        return None

    def _on_pipeline_finished(self, context):

        final_layer = context.get("layer")

        LogUtils.log(
            f"Layer: {final_layer}",
            level="WARNING",
            tool=self.TOOL_KEY,
            class_name="GerarRastroDialog"
        )

        LogUtils.log(
            f"Is valid: {final_layer.isValid() if final_layer else None}",
            level="WARNING",
            tool=self.TOOL_KEY,
            class_name="GerarRastroDialog"
        )

        LogUtils.log(
            f"Provider: {final_layer.providerType() if final_layer else None}",
            level="WARNING",
            tool=self.TOOL_KEY,
            class_name="GerarRastroDialog"
        )
        if not final_layer:
            QgisMessageUtil.modal_error(
                self.iface,
                "Erro: camada final não encontrada no contexto."
            )
            return

        # Garantir que está no projeto
        if not QgsProject.instance().mapLayer(final_layer.id()):
            QgsProject.instance().addMapLayer(final_layer)

        # Aplicar estilo se necessário
        if self.qml_selector.is_enabled():
            qml = self.qml_selector.get_file_path()
            if qml:
                self.apply_qml_style(final_layer, qml)

        QgisMessageUtil.bar_success(
            self.iface,
            "Processamento executado com sucesso."
        )

def run_gerar_rastro(iface):
    dlg = GenerateTrailPlugin(iface)
    dlg.setModal(False)
    dlg.show()
    return dlg  # 👈 ESSENCIAL

