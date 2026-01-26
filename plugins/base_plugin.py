from qgis.PyQt.QtWidgets import (
    QDialog, QAction,QFileDialog, QLineEdit
)
from qgis.core import QgsVectorLayer, QgsWkbTypes, QgsApplication, QgsProject,QgsFeatureRequest
from qgis.PyQt.QtGui import QDesktopServices
from qgis.PyQt.QtCore import QUrl
import os
from pathlib import Path
from typing import Optional
import time

from ..utils.vector.VectorLayerSource import VectorLayerSource
from ..core.config.LogUtils import LogUtils


from ..utils.crs_utils import get_coord_info
from ..utils.info_dialog import InfoDialog
from ..utils.log_utils import LogUtilsOld
from ..utils.qgis_messagem_util import QgisMessageUtil
from ..utils.preferences import load_tool_prefs, save_tool_prefs
from ..utils.tool_keys import ToolKey
from ..utils.qgis_messagem_util import QgisMessageUtil
from ..utils.project_utils import  ProjectUtils
from ..utils.string_utils import StringUtils
from ..utils.vector_utils import VectorUtils




# -------------------------------------------------------------
#  PLUGIN BasePluginMTL
# -------------------------------------------------------------
class BasePluginMTL(QDialog):
    APP_NAME = StringUtils.APP_NAME
    PLUGIN_NAME = ""
    """
    Classe base para plugins do MTL Tools.

    Centraliza funcionalidades comuns aos plugins, como:
    - Criação de ações de menu
    - Recuperação da camada vetorial ativa
    - Validações básicas de edição e existência de feições

    Deve ser herdada por plugins específicos.
    """
    def _build_ui(self):
        LogUtils.log(f"Construindo UI para plugin: {self.PLUGIN_NAME}", level="DEBUG", tool=ToolKey.BASE_TOOL, class_name="BasePluginMTL")
        self.setWindowTitle(f"{self.APP_NAME} — {self.PLUGIN_NAME}")
        self.setMinimumWidth(460)

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
    
    def save_vector_layer(self,layer, output_path, save_to_folder, output_name = "LAYER_OUTPUT"):
        LogUtils.log(f"Iniciando salvamento de camada. Output: {output_path}. Save to folder: {save_to_folder}", level="DEBUG", tool=ToolKey.BASE_TOOL, class_name="BasePluginMTL")
        # -------------------------------------------------
        # 6) salvar em disco (se solicitado)
        # -------------------------------------------------
        final_layer = layer.materialize(
            QgsFeatureRequest()
        )
        layer = None  # liberar memória 


        if save_to_folder:
 
            decision = None
            if os.path.exists(output_path):
                decision = QgisMessageUtil.ask_overwrite(
                    self.iface,
                    output_path
                )

                if decision == "cancel":
                    return None
                

            if decision == "overwrite":
                ProjectUtils.remove_file_from_project_hard(output_path)
                LogUtils.log(f"Overwrite solicitado pelo usuário para: {output_path}", level="DEBUG", tool=ToolKey.BASE_TOOL, class_name="BasePluginMTL")
            
            #-------------------------------------------------       
         
            LogUtils.log(f"Salvando camada em disco: {output_path} Existe: {os.path.exists(output_path)}. Save to folder: {save_to_folder}. Decision: {decision}. Final layer: {final_layer}", level="DEBUG", tool=ToolKey.BASE_TOOL, class_name="BasePluginMTL")
            saved_path = VectorLayerSource.save_vector_layer_to_file(            
                layer=final_layer,
                output_path=output_path,                
                decision=decision,
                external_tool_key=ToolKey.BASE_TOOL
    
            )

            if not saved_path:
                LogUtils.log(f"Falha ao salvar camada em: {output_path}", level="DEBUG", tool=ToolKey.BASE_TOOL, class_name="BasePluginMTL")
                QgisMessageUtil.bar_critical(
                    self.iface,
                    f'Operação cancelada ou falha ao salvar. Vefifique se o arquivo esta carregado no projeto e tenten novamente.'
                )
                return None
            #---------------------------------------------------
            LogUtils.log(f"Carregando camada salva: {saved_path}", level="DEBUG", tool=ToolKey.BASE_TOOL, class_name="BasePluginMTL")
            final_layer = QgsVectorLayer(
                saved_path,
                Path(saved_path).stem,
                "ogr"
            )


        if not isinstance(final_layer, QgsVectorLayer) or not final_layer.isValid():
            LogUtils.log(f"Camada salva é inválida", level="DEBUG", tool=ToolKey.BASE_TOOL, class_name="BasePluginMTL")
            QgisMessageUtil.modal_error(
                self.iface,
                "Camada salva é inválida."
            )
            return None


        # -------------------------------------------------
        # 7) adicionar ao projeto
        # -------------------------------------------------
        if save_to_folder:
            output_name = Path(output_path).stem
        final_layer.setName(output_name)
        QgsProject.instance().addMapLayer(final_layer)
        LogUtils.log(f"Camada adicionada ao projeto com nome: {output_name}", level="DEBUG", tool=ToolKey.BASE_TOOL, class_name="BasePluginMTL")

        return final_layer

