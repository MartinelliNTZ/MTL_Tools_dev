from qgis.PyQt.QtWidgets import (
    QDialog, QAction,QFileDialog, QLineEdit,QSizeGrip
)
from qgis.core import QgsVectorLayer, QgsWkbTypes, QgsApplication, QgsProject,QgsFeatureRequest
from qgis.PyQt.QtGui import QDesktopServices, QIcon
from qgis.PyQt.QtCore import QUrl, Qt

import os
from pathlib import Path
from typing import Optional
import time
from ..utils.project_utils import ProjectUtils
from ..utils.FormatUtils import FormatUtils
from ..utils.vector.VectorLayerSource import VectorLayerSource
from ..core.config.LogUtils import LogUtils
from ..core.config.LogUtilsNew import LogUtilsNew
from ..core.ui.WidgetFactory import WidgetFactory
from ..utils.info_dialog import InfoDialog
from ..utils.preferences import load_tool_prefs, save_tool_prefs
from ..utils.tool_keys import ToolKey
from ..utils.qgis_messagem_util import QgisMessageUtil
from ..utils.project_utils import  ProjectUtils
from ..utils.string_utils import StringUtils




# -------------------------------------------------------------
#  PLUGIN BasePluginMTL
# -------------------------------------------------------------
class BasePluginMTL(QDialog):
    APP_NAME = StringUtils.APP_NAME
    TOOL_KEY = ToolKey.BASE_TOOL
    PLUGIN_NAME = ""
    layout = None
    prefs = None
    """obsolet"""
    logger = None
    preferences = {}
    """Dicionario de status"""



    def init(self,tool_key = "ToolKey.BASE_TOOL", class_name = "BasePluginMTL"):
        self.TOOL_KEY = tool_key
        self.logger = LogUtilsNew(tool=self.TOOL_KEY, class_name=class_name, level=LogUtilsNew.DEBUG)
        self.preferences = {}
        self.preferences.clear()
        self.preferences = load_tool_prefs(self.TOOL_KEY)
        self.logger.debug("Construindo interface de usuário")
        self._build_ui()
        self.logger.debug("Carregando preferências do usuário. xxd")
        self._load_prefs()
        self.logger.info("Diálogo Gerar Rastro Implemento inicializado com sucesso. xxd")

    """
    Classe base para plugins do MTL Tools.

    Centraliza funcionalidades comuns aos plugins, como:
    - Criação de ações de menu
    - Recuperação da camada vetorial ativa
    - Validações básicas de edição e existência de feições

    Deve ser herdada por plugins específicos.
    """


    def _build_ui(
        self,
        title: Optional[str] = None,
        icon_path: Optional[str] = "mtl_agro.ico",
        instructions_file: Optional[str] = "standard.md"
    ):
        """Constrói a interface do plugin.

        Recebe: title (str|None), icon_path (str), instructions_file (str).
        Retorna: None.
        Faz: configura layout, ícone, tamanho da janela e caminho de instruções.
        """
        if title is not None:
            self.PLUGIN_NAME = title
            self.layout = WidgetFactory.create_main_layout(self, title=title)

        self.logger.log(
            f"Construindo UI para plugin: {self.PLUGIN_NAME}",
            level="DEBUG",
            tool=ToolKey.BASE_TOOL,
            class_name="BasePluginMTL"
        )

        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setMinimumSize(460, 320)
        self.setWindowTitle(f"MTL Tools — {self.PLUGIN_NAME}")

        # Size grip (resize)
        self.size_grip = QSizeGrip(self.layout._frame)
        self.size_grip.setFixedSize(16, 16)
        self.layout.addWidget(
            self.size_grip,
            alignment=Qt.AlignBottom | Qt.AlignRight
        )

        # Ícone
        icon_path = os.path.join(
            os.path.dirname(__file__), "..", "resources", "icons", icon_path
        )
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
            self.logger.log(
                f"Ícone carregado de: {icon_path}",
                level="DEBUG",
                tool=self.TOOL_KEY,
                class_name="GerarRastroDialog"
            )

        # instruções
        self.instructions_file = os.path.join(
            os.path.dirname(__file__),
            "..",
            "resources",
            "instructions",
            instructions_file
        )

    def start_stats(self, input_obj=None,modal_info = "YES"):
        try:
            self.preferences["t0"] = time.time()
            self.preferences["current_size"] = ProjectUtils.compute_size(input_obj) if input_obj else 0
            self.preferences["eta"] = 0
            self.preferences["avg_speed"] = self.preferences.get("avg_speed", 0)
            self.preferences["total_bytes"] = self.preferences.get("total_bytes", 0)
            self.preferences["total_time"] = self.preferences.get("total_time", 0)

            if self.preferences["total_time"] > 0:
                self.preferences["avg_speed"] = self.preferences["total_bytes"] / self.preferences["total_time"]
            if self.preferences["avg_speed"] > 0 and self.preferences["current_size"] > 0:
                self.preferences["eta"] = (self.preferences["current_size"] / self.preferences["avg_speed"])+time.time()

            msg = ""
            if self.preferences["eta"] > 0 and self.preferences["current_size"] > 0 and self.preferences["avg_speed"] > 0 :                
                msg = (
                    f"  Velocidade média: {FormatUtils.speed(self.preferences['avg_speed'])} \n"
                    f"  Tamanho do arquivo: {FormatUtils.bytes(self.preferences["current_size"])} \n"
                    f"  Hora inicial: {FormatUtils.clock(self.preferences['t0'],)} \n"
                    f"  Hora final: {FormatUtils.clock(self.preferences.get('eta',0))}\n"
                )

                if modal_info == "YES":
                    QgisMessageUtil.bar_info(self.iface, msg, "Estatisticas",duration=10)
                self.logger.info(msg)
        except Exception as e:
            self.logger.error(e)

    def finish_stats(self,modal_info = "YES"):
        self.logger.debug("finish_stats")
        try:
            dt = time.time() - self.preferences["t0"]
            size = self.preferences["current_size"]
            self.logger.info("")
            self.preferences["total_bytes"] = self.preferences.get("total_bytes", 0) + size
            self.preferences["total_time"] = self.preferences.get("total_time", 0) + dt
            self.preferences["runs"] = self.preferences.get("runs", 0) + 1

            if self.preferences["total_time"] > 0:
                self.preferences["avg_speed"] = (
                        self.preferences["total_bytes"] / self.preferences["total_time"]
                )

            msg = (
                f"+{FormatUtils.bytes(size)} "
                f"{dt:.1f}s "
                f"avg={FormatUtils.speed(self.preferences['avg_speed'])}"
            )

            if modal_info == "YES":
                QgisMessageUtil.bar_success(self.iface,f"Estatistivas: {msg} ")
            self.logger.info(msg)
        except Exception as e:
            self.logger.error(f"Erro: {e} Preferences: {self.preferences}")


    #@abstractmethod
    def execute_tool(self):
        """
        Método principal a ser implementado por cada plugin específico.
        Ele é chamado quando o usuário aciona a funcionalidade do plugin (ex: clica em um botão).
        Deve conter a lógica de execução do plugin.
        """
        pass
    
    def run(self):
        """
        Controller para execução do plugin.
        Starta a papeline e gerencia o fluxo de execução, incluindo tratamento de erros.
        Pode ser chamado diretamente ou após a execução do execute_tool().
        """
        pass

    def _on_pipeline_finished(self, context):    
        """Callback para quando a pipeline é finalizada com sucesso."""
        pass

    def _on_pipeline_error(self, errors):
        """Exibe um modal de erro genérico para a pipeline."""
        exc = errors[0] if errors else Exception("Erro desconhecido")

        QgisMessageUtil.modal_error(
            self.iface,
            f"Erro durante processamento:\n{exc}"
        )
    
    def open_file(self, path):
        """Abre um arquivo no explorador padrão.

        Recebe: path (str).
        Retorna: None.
        Faz: registra e abre o arquivo se existir.
        """
        self.logger.log(f"Abrindo arquivo: {path}", level="DEBUG")
        if path and os.path.exists(path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(path))

    def open_folder(self, path):
        """Abre uma pasta no explorador padrão.

        Recebe: path (str).
        Retorna: None.
        Faz: registra e abre a pasta se existir.
        """
        self.logger.log(f"Abrindo pasta: {path}", level="DEBUG")
        if path and os.path.exists(path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(path))
    
    def create_action(self, icon_rel_path, text, callback):
        """Cria e registra uma ação no menu do plugin.

        Recebe: icon_rel_path (str), text (str), callback (callable).
        Retorna: QAction criado.
        Faz: cria a QAction, conecta o callback e adiciona ao menu.
        """
        self.logger.log(f"Criando ação: {text}", level="DEBUG")
        icon_path = os.path.join(
            os.path.dirname(self.__class__.__module__.replace('.', os.sep)),
            icon_rel_path
        )

        action = QAction(icon_path, text, self.iface.mainWindow())
        action.triggered.connect(callback)

        self.iface.addPluginToMenu(self.MENU_NAME, action)
        self.actions.append(action)

    def get_active_vector_layer(self, require_editable=False):
        """Obtém a camada vetorial ativa.

        Recebe: require_editable (bool).
        Retorna: QgsVectorLayer ou None.
        Faz: valida tipo da camada e, se solicitado, se está em edição.
        """
        self.logger.log(f"Obtendo camada vetorial ativa. Require editable: {require_editable}", level="DEBUG")
        layer = self.iface.activeLayer()

        if not layer or not isinstance(layer, QgsVectorLayer):
            self.logger.log("Camada ativa inválida ou não é vetorial", level="DEBUG")
            QgisMessageUtil.bar_critical(
                self.iface,
                "Selecione uma camada vetorial"
            )
            return None


        if require_editable and not self.ensure_editable(layer):
            return None


        return layer

    def ensure_has_features(self, layer):
        """Valida se a camada tem feições.

        Recebe: layer (QgsVectorLayer).
        Retorna: bool.
        Faz: verifica contagem de feições e mostra aviso se estiver vazia.
        """
        self.logger.log(f"Verificando feições na camada: {layer.name()}. Total: {layer.featureCount()}", level="DEBUG")
        if layer.featureCount() == 0:
            QgisMessageUtil.bar_warning(
                self.iface,
                "A camada não possui feições"
            )
            return False

        return True
    
    def get_layer_from_combo(self, combo):
        """DEPRECADO: """
        """Retorna camada a partir de um combo (QComboBox).

        Recebe: combo (widget com currentData() contendo id de camada).
        Retorna: QgsMapLayer ou None.
        Faz: obtém a camada no projeto pelo id armazenado no combo.
        """
        return QgsProject.instance().mapLayer(combo.currentData())
    
    def ensure_editable(self, layer):
        """Verifica se a camada está em modo edição.

        Recebe: layer (QgsVectorLayer).
        Retorna: bool.
        Faz: mostra erro e retorna False se não estiver em edição.
        """
        self.logger.log(f"Verificando se camada está em edição: {layer.name()}. Editável: {layer.isEditable()}", level="DEBUG")
        if not layer.isEditable():
            QgisMessageUtil.bar_critical(
                self.iface,
                "A camada precisa estar em edição"
            )
            return False
        return True

    def show_info_dialog(self, title="📘 Instruções"):
        """Mostra diálogo de instruções do plugin.

        Recebe: title (str opcional).
        Retorna: None.
        Faz: abre `InfoDialog` com o arquivo de instruções, se existir.
        """
        if hasattr(self, "instructions_file"):
            title = f"📘 Instruções – {self.PLUGIN_NAME}"
            InfoDialog(self.instructions_file, self, title).exec() 
            
    def show_project_file(self):
        """Exibe o caminho do arquivo do projeto atual.

        Recebe: self.
        Retorna: None.
        Faz: mostra mensagem se projeto não salvo ou modal com o arquivo salvo.
        """
        project = QgsProject.instance()
        fname = project.fileName()

        if not fname:
            QgisMessageUtil.bar_info(
                self.iface,
                "O projeto atual ainda não foi salvo em disco.",
                "Projeto não salvo"
            )
            return

        QgisMessageUtil.modal_result_with_folder(
            self.iface,
            "Arquivo do Projeto",
            "Arquivo atual:",
            fname
        )
    
    def select_file_to_save(self,  target_line_edit: QLineEdit, filters: str):
        """Abre diálogo para escolher caminho de salvamento.

        Recebe: target_line_edit (QLineEdit), filters (str).
        Retorna: None.
        Faz: atualiza `target_line_edit` com o caminho escolhido.
        """
        self.logger.log(f"Abrindo diálogo para salvar arquivo", level="DEBUG")
        f, _ = QFileDialog.getSaveFileName(self, 'Salvar como', target_line_edit.text() or '', filters)
        if f:
            self.logger.log(f"Arquivo selecionado para salvar: {f}", level="DEBUG")
            target_line_edit.setText(f)

    def select_file(self, target_line_edit: QLineEdit, filters: str):
        """Abre diálogo para selecionar arquivo existente.

        Recebe: target_line_edit (QLineEdit), filters (str).
        Retorna: None.
        Faz: atualiza `target_line_edit` com o arquivo selecionado.
        """
        self.logger.log(f"Abrindo diálogo para selecionar arquivo", level="DEBUG")
        f, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar arquivo",
            "",
            filters
        )
        if f:
            self.logger.log(f"Arquivo selecionado: {f}", level="DEBUG")
            target_line_edit.setText(f)
              
    def apply_qml_style(
        self,
        layer: QgsVectorLayer,
        qml_path: str
    ) -> bool:
        """Aplica um arquivo QML como estilo na camada.

        Recebe: layer (QgsVectorLayer), qml_path (str).
        Retorna: bool (sucesso).
        Faz: valida entrada, carrega estilo e repinta a camada.
        """
        self.logger.log(f"Aplicando estilo QML à camada: {layer.name() if isinstance(layer, QgsVectorLayer) else 'inválida'}. Caminho: {qml_path}", level="DEBUG")

        if not isinstance(layer, QgsVectorLayer):
            return False

        if not qml_path or not os.path.exists(qml_path):
            self.logger.log(f"Caminho QML inválido ou não existe: {qml_path}", level="DEBUG")
            return False

        ok = layer.loadNamedStyle(qml_path)
        if isinstance(ok, tuple):
            ok = ok[0]

        if ok:
            layer.triggerRepaint()
            self.logger.log(f"Estilo QML aplicado com sucesso", level="DEBUG")

        return bool(ok)
    
    def save_vector_layer(
        self,
        buffer_layer: QgsVectorLayer,
        output_path: Optional[str],
        save_to_folder: bool,
        output_name: str
    ) -> Optional[QgsVectorLayer]:
        """DEPRECADO: Use SaveVectorTask."""

        return VectorLayerSource.save_vector_layer(
            layer=buffer_layer,
            output_path=output_path,
            save_to_folder=save_to_folder,
            output_name=output_name,
            external_tool_key=self.TOOL_KEY
        )   
     
