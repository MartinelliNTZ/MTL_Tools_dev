from qgis.PyQt.QtWidgets import (
    QDialog, QAction,QFileDialog, QLineEdit,QSizeGrip
)
from qgis.core import QgsVectorLayer, QgsWkbTypes, QgsApplication, QgsProject,QgsFeatureRequest
from qgis.PyQt.QtGui import QDesktopServices, QIcon, QCursor
from qgis.PyQt.QtCore import QUrl, Qt, QRect, QPoint

import os
from pathlib import Path
from typing import Optional
import time
from ..utils.project_utils import ProjectUtils
from ..utils.FormatUtils import FormatUtils
from ..utils.vector.VectorLayerSource import VectorLayerSource
from ..core.config.LogUtilsNew import LogUtilsNew
from ..core.ui.WidgetFactory import WidgetFactory
from ..utils.info_dialog import InfoDialog
from ..utils.Preferences import load_tool_prefs, save_tool_prefs
from ..utils.ToolKeys import ToolKey
from ..utils.QgisMessageUtil import QgisMessageUtil
from ..utils.project_utils import  ProjectUtils
from ..utils.string_utils import StringUtils




# -------------------------------------------------------------
#  PLUGIN BasePluginMTL
# -------------------------------------------------------------
class BasePluginMTL(QDialog):
    APP_NAME = StringUtils.APP_NAME
    TOOL_KEY = "base_plugin"  # Identificador padrão
    PLUGIN_NAME = ""
    layout = None
    prefs = None
    """obsolet"""
    logger = None
    preferences = {}
    """Dicionario de status"""
    settings_preferences = {}
    """Preferências globais do aplicativo (MTL Tools Settings)"""



    def init(self, tool_key="base_plugin", class_name="BasePluginMTL", min_width=460, min_height=320, load_settings_prefs=False, build_ui=True):
        """Inicializa o plugin base.
        
        Parameters
        ----------
        tool_key : str
            Identificador único da ferramenta (padrão: base_plugin)
        class_name : str
            Nome da classe para logging (padrão: BasePluginMTL)
        min_width : int
            Largura mínima da janela em pixels (padrão: 460)
        min_height : int
            Altura mínima da janela em pixels (padrão: 320)
        load_settings_prefs : bool
            Se True, carrega preferências globais do MTL Tools Settings (padrão: False)
        build_ui : bool
            Se True, constrói a interface de usuário (padrão: True)
        """
        self.TOOL_KEY = tool_key
        self.logger = LogUtilsNew(tool=self.TOOL_KEY, class_name=class_name, level=LogUtilsNew.DEBUG)
        self.preferences = {}
        self.preferences.clear()
        self.preferences = load_tool_prefs(self.TOOL_KEY)
        
        # Carregar preferências globais do Settings se solicitado
        if load_settings_prefs:
            self.logger.debug("Carregando preferências globais do MTL Tools Settings")
            self.settings_preferences = load_tool_prefs(ToolKey.SETTINGS)
            self.logger.debug(f"Preferências globais carregadas: {list(self.settings_preferences.keys())}")
        else:
            self.settings_preferences = {}
        
        # Construir UI apenas se solicitado
        if build_ui:
            self.logger.debug("Construindo interface de usuário")
            self._build_ui(min_width=min_width, min_height=min_height)
            self.logger.debug("Carregando preferências do usuário. xxd")
            self._load_prefs()
            self.logger.info("Diálogo Gerar Rastro Implemento inicializado com sucesso. xxd")
        else:
            self.logger.debug("Construção de UI desabilitada")

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
        instructions_file: Optional[str] = "standard.md",
        min_width: int = 460,
        min_height: int = 320,
        **kwargs
    ):
        """Constrói a interface do plugin.

        Recebe: title (str|None), icon_path (str), instructions_file (str), min_width (int), min_height (int).
        Retorna: None.
        Faz: configura layout, ícone, tamanho da janela e caminho de instruções.
        """
        if title is not None:
            self.PLUGIN_NAME = title
            self.layout = WidgetFactory.create_main_layout(self, title=title)

        self.logger.debug(f"Construindo UI para plugin: {self.PLUGIN_NAME}")

        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setMinimumSize(min_width, min_height)
        self.setWindowTitle(f"MTL Tools — {self.PLUGIN_NAME}")

        # Size grip (resize visual indicator)
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
            self.logger.debug(f"Ícone carregado de: {icon_path}")

        # instruções
        self.instructions_file = os.path.join(
            os.path.dirname(__file__),
            "..",
            "resources",
            "instructions",
            instructions_file
        )

    def mousePressEvent(self, event):
        """Delega evento de mouse para detecção de bordas e início de resize do MainLayout."""
        if self.layout and hasattr(self.layout, 'handle_mouse_press'):
            if self.layout.handle_mouse_press(event):
                return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """Delega evento de mouse para atualização de cursor e resize do MainLayout.        """
        if self.layout and hasattr(self.layout, 'handle_mouse_move'):
            self.layout.handle_mouse_move(event)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """Delega evento de mouse para finalização de resize do MainLayout."""
        if self.layout and hasattr(self.layout, 'handle_mouse_release'):
            if self.layout.handle_mouse_release(event):
                return
        super().mouseReleaseEvent(event)

    def start_stats(self, input_obj=None,modal_info = "YES"):
        try:
            self.preferences["t0"] = time.time()
            # compute both size and feature count when possible
            self.preferences["current_size"] = ProjectUtils.compute_size(input_obj) if input_obj else 0
            if hasattr(input_obj, "featureCount"):
                try:
                    self.preferences["current_features"] = input_obj.featureCount()
                except Exception:
                    self.preferences["current_features"] = 0
            else:
                self.preferences["current_features"] = 0

            self.preferences["eta"] = 0
            self.preferences["avg_speed"] = self.preferences.get("avg_speed", 0)
            self.preferences["total_bytes"] = self.preferences.get("total_bytes", 0)
            self.preferences["total_time"] = self.preferences.get("total_time", 0)

            if self.preferences["total_time"] > 0:
                self.preferences["avg_speed"] = self.preferences["total_bytes"] / self.preferences["total_time"]
            if self.preferences["avg_speed"] > 0 and self.preferences["current_size"] > 0:
                self.preferences["eta"] = (self.preferences["current_size"] / self.preferences["avg_speed"])+time.time()
            TAM = FormatUtils.bytes(self.preferences["current_size"])
            feats = self.preferences.get("current_features", 0)
            msg = ""
            if self.preferences["eta"] > 0 and self.preferences["current_size"] > 0 and self.preferences["avg_speed"] > 0 :                
                msg = (
                   # f"  Velocidade média: {FormatUtils.speed(self.preferences['avg_speed'])} \n"
                    #f"  Tamanho do arquivo: {TAM} \n"
                    #f"  Feições: {feats} \n"
                    f"  Hora inicial: {FormatUtils.clock(self.preferences['t0'],)} \n"
                    f"  HORA FINAL: {FormatUtils.clock(self.preferences.get('eta',0))}\n"
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
            feats = self.preferences.get("current_features", 0)
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
                f"feats={feats} "
                f"avg={FormatUtils.speed(self.preferences['avg_speed'])}"
            )

            if modal_info == "YES":
                QgisMessageUtil.bar_success(self.iface,f"Estatistivas: {msg} ")
            self.logger.info(msg)
            # atualizar agregados de features e limpar dados transitórios antes de persistir
            feats = self.preferences.get("current_features", 0)
            self.preferences["total_features"] = self.preferences.get("total_features", 0) + feats
            # campos que não devem ser salvos entre execuções
            for key in ("t0", "current_size", "current_features", "eta", "avg_speed"):
                self.preferences.pop(key, None)
            try:
                save_tool_prefs(self.TOOL_KEY, self.preferences)
            except Exception as se:
                self.logger.debug(f"Falha ao salvar prefs estatísticas: {se}")
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
        self.logger.debug(f"Abrindo arquivo: {path}")
        if path and os.path.exists(path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(path))

    def open_folder(self, path):
        """Abre uma pasta no explorador padrão.

        Recebe: path (str).
        Retorna: None.
        Faz: registra e abre a pasta se existir.
        """
        self.logger.debug(f"Abrindo pasta: {path}")
        if path and os.path.exists(path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(path))
    
    def create_action(self, icon_rel_path, text, callback):
        """Cria e registra uma ação no menu do plugin.

        Recebe: icon_rel_path (str), text (str), callback (callable).
        Retorna: QAction criado.
        Faz: cria a QAction, conecta o callback e adiciona ao menu.
        """
        self.logger.debug(f"Criando ação: {text}")
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
        self.logger.debug(f"Obtendo camada vetorial ativa. Require editable: {require_editable}")
        layer = self.iface.activeLayer()

        if not layer or not isinstance(layer, QgsVectorLayer):
            self.logger.debug("Camada ativa inválida ou não é vetorial")
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
        self.logger.debug(f"Verificando feições na camada: {layer.name()}. Total: {layer.featureCount()}")
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
        self.logger.debug(f"Verificando se camada está em edição: {layer.name()}. Editável: {layer.isEditable()}")
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
        self.logger.debug(f"Abrindo diálogo para salvar arquivo")
        f, _ = QFileDialog.getSaveFileName(self, 'Salvar como', target_line_edit.text() or '', filters)
        if f:
            self.logger.debug(f"Arquivo selecionado para salvar: {f}")
            target_line_edit.setText(f)

    def select_file(self, target_line_edit: QLineEdit, filters: str):
        """Abre diálogo para selecionar arquivo existente.

        Recebe: target_line_edit (QLineEdit), filters (str).
        Retorna: None.
        Faz: atualiza `target_line_edit` com o arquivo selecionado.
        """
        self.logger.debug(f"Abrindo diálogo para selecionar arquivo")
        f, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar arquivo",
            "",
            filters
        )
        if f:
            self.logger.debug(f"Arquivo selecionado: {f}")
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
        self.logger.debug(f"Aplicando estilo QML à camada: {layer.name() if isinstance(layer, QgsVectorLayer) else 'inválida'}. Caminho: {qml_path}")

        if not isinstance(layer, QgsVectorLayer):
            return False

        if not qml_path or not os.path.exists(qml_path):
            self.logger.debug(f"Caminho QML inválido ou não existe: {qml_path}")
            return False

        ok = layer.loadNamedStyle(qml_path)
        if isinstance(ok, tuple):
            ok = ok[0]

        if ok:
            layer.triggerRepaint()
            self.logger.debug(f"Estilo QML aplicado com sucesso")

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
     
