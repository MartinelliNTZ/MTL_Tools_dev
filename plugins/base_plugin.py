from qgis.PyQt.QtWidgets import (
    QDialog, QAction,QFileDialog, QLineEdit,QSizeGrip
)
from qgis.core import QgsVectorLayer, QgsWkbTypes, QgsApplication, QgsProject,QgsFeatureRequest
from qgis.PyQt.QtGui import QDesktopServices, QIcon
from qgis.PyQt.QtCore import QUrl, Qt

import os
from pathlib import Path
from typing import Optional

from ..utils.vector.VectorLayerSource import VectorLayerSource
from ..core.config.LogUtils import LogUtils
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
    PLUGIN_NAME = ""
    layout = None
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
        if title is not None:
            self.PLUGIN_NAME = title
            self.layout = WidgetFactory.create_main_layout(self, title=title)

        LogUtils.log(
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
            LogUtils.log(
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


    def open_file(self, path):
        LogUtils.log(f"Abrindo arquivo: {path}", level="DEBUG", tool=ToolKey.BASE_TOOL, class_name="BasePluginMTL")
        if path and os.path.exists(path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(path))

    def open_folder(self, path):
        LogUtils.log(f"Abrindo pasta: {path}", level="DEBUG", tool=ToolKey.BASE_TOOL, class_name="BasePluginMTL")
        if path and os.path.exists(path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(path))
    
    def create_action(self, icon_rel_path, text, callback):
        """Cria uma QAction e adiciona ao menu do plugin."""
        LogUtils.log(f"Criando ação: {text}", level="DEBUG", tool=ToolKey.BASE_TOOL, class_name="BasePluginMTL")
        icon_path = os.path.join(
            os.path.dirname(self.__class__.__module__.replace('.', os.sep)),
            icon_rel_path
        )

        action = QAction(icon_path, text, self.iface.mainWindow())
        action.triggered.connect(callback)

        self.iface.addPluginToMenu(self.MENU_NAME, action)
        self.actions.append(action)

    def get_active_vector_layer(self, require_editable=False):
        """Retorna a camada vetorial ativa, opcionalmente exigindo que esteja em edição."""
        LogUtils.log(f"Obtendo camada vetorial ativa. Require editable: {require_editable}", level="DEBUG", tool=ToolKey.BASE_TOOL, class_name="BasePluginMTL")
        layer = self.iface.activeLayer()

        if not layer or not isinstance(layer, QgsVectorLayer):
            LogUtils.log("Camada ativa inválida ou não é vetorial", level="DEBUG", tool=ToolKey.BASE_TOOL, class_name="BasePluginMTL")
            QgisMessageUtil.bar_critical(
                self.iface,
                "Selecione uma camada vetorial"
            )
            return None


        if require_editable and not self.ensure_editable(layer):
            return None


        return layer

    def ensure_has_features(self, layer):
        """Verifica se a camada possui feições."""
        LogUtils.log(f"Verificando feições na camada: {layer.name()}. Total: {layer.featureCount()}", level="DEBUG", tool=ToolKey.BASE_TOOL, class_name="BasePluginMTL")
        if layer.featureCount() == 0:
            QgisMessageUtil.bar_warning(
                self.iface,
                "A camada não possui feições"
            )
            return False

        return True
    
    def get_layer_from_combo(self, combo):
        return QgsProject.instance().mapLayer(combo.currentData())
    
    def ensure_editable(self, layer):
        LogUtils.log(f"Verificando se camada está em edição: {layer.name()}. Editável: {layer.isEditable()}", level="DEBUG", tool=ToolKey.BASE_TOOL, class_name="BasePluginMTL")
        if not layer.isEditable():
            QgisMessageUtil.bar_critical(
                self.iface,
                "A camada precisa estar em edição"
            )
            return False
        return True

    def show_info_dialog(self, title="📘 Instruções"):
        if hasattr(self, "instructions_file"):
            title = f"📘 Instruções – {self.PLUGIN_NAME}"
            InfoDialog(self.instructions_file, self, title).exec() 
            
    def show_project_file(self):
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
        LogUtils.log(f"Abrindo diálogo para salvar arquivo", level="DEBUG", tool=ToolKey.BASE_TOOL, class_name="BasePluginMTL")
        f, _ = QFileDialog.getSaveFileName(self, 'Salvar como', target_line_edit.text() or '', filters)
        if f:
            LogUtils.log(f"Arquivo selecionado para salvar: {f}", level="DEBUG", tool=ToolKey.BASE_TOOL, class_name="BasePluginMTL")
            target_line_edit.setText(f)

    def select_file(self, target_line_edit: QLineEdit, filters: str):
        LogUtils.log(f"Abrindo diálogo para selecionar arquivo", level="DEBUG", tool=ToolKey.BASE_TOOL, class_name="BasePluginMTL")
        f, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar arquivo",
            "",
            filters
        )
        if f:
            LogUtils.log(f"Arquivo selecionado: {f}", level="DEBUG", tool=ToolKey.BASE_TOOL, class_name="BasePluginMTL")
            target_line_edit.setText(f)
              
    def apply_qml_style(
        self,
        layer: QgsVectorLayer,
        qml_path: str
    ) -> bool:
        LogUtils.log(f"Aplicando estilo QML à camada: {layer.name() if isinstance(layer, QgsVectorLayer) else 'inválida'}. Caminho: {qml_path}", level="DEBUG", tool=ToolKey.BASE_TOOL, class_name="BasePluginMTL")

        if not isinstance(layer, QgsVectorLayer):
            return False

        if not qml_path or not os.path.exists(qml_path):
            LogUtils.log(f"Caminho QML inválido ou não existe: {qml_path}", level="DEBUG", tool=ToolKey.BASE_TOOL, class_name="BasePluginMTL")
            return False

        ok = layer.loadNamedStyle(qml_path)
        if isinstance(ok, tuple):
            ok = ok[0]

        if ok:
            layer.triggerRepaint()
            LogUtils.log(f"Estilo QML aplicado com sucesso", level="DEBUG", tool=ToolKey.BASE_TOOL, class_name="BasePluginMTL")

        return bool(ok)
    
    def save_vector_layer(
        self,
        buffer_layer: QgsVectorLayer,
        output_path: Optional[str],
        save_to_folder: bool,
        output_name: str
    ) -> Optional[QgsVectorLayer]:

        return VectorLayerSource.save_layer(
            layer=buffer_layer,
            output_path=output_path,
            save_to_folder=save_to_folder,
            output_name=output_name,
            external_tool_key=self.TOOL_KEY
        )    
    def _on_pipeline_error(self, errors):
        exc = errors[0] if errors else Exception("Erro desconhecido")

        QgisMessageUtil.modal_error(
            self.iface,
            f"Erro durante processamento:\n{exc}"
        )
