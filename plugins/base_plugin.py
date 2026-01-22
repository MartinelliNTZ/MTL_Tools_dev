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


from ..utils.crs_utils import get_coord_info
from ..utils.info_dialog import InfoDialog
from ..utils.log_utils import LogUtilsOld
from ..utils.qgis_messagem_util import QgisMessageUtil
from ..utils.preferences import load_tool_prefs, save_tool_prefs
from ..utils.tool_keys import ToolKey
from ..utils.qgis_messagem_util import QgisMessageUtil
from ..utils.ui_widget_utils import  UiWidgetUtils
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
        self.setWindowTitle(f"{self.APP_NAME} — {self.PLUGIN_NAME}")
        self.setMinimumWidth(460)

    def open_file(self, path):
        if path and os.path.exists(path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(path))

    def open_folder(self, path):
        
        if path and os.path.exists(path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(path))
    
    def create_action(self, icon_rel_path, text, callback):
        """
        Cria uma QAction, adiciona ao menu do plugin e registra internamente.

        :param icon_rel_path: Caminho relativo do ícone dentro do plugin
        :type icon_rel_path: str

        :param text: Texto exibido no menu
        :type text: str

        :param callback: Função chamada ao acionar a ação
        :type callback: callable
        """
        icon_path = os.path.join(
            os.path.dirname(self.__class__.__module__.replace('.', os.sep)),
            icon_rel_path
        )

        action = QAction(icon_path, text, self.iface.mainWindow())
        action.triggered.connect(callback)

        self.iface.addPluginToMenu(self.MENU_NAME, action)
        self.actions.append(action)

    def get_active_vector_layer(self, require_editable=False):
        """
        Retorna a camada vetorial ativa no QGIS, validando tipo e estado.

        :param require_editable: Se True, exige que a camada esteja em modo edição
        :type require_editable: bool

        :return: Camada vetorial ativa ou None se inválida
        :rtype: QgsVectorLayer | None
        """
        layer = self.iface.activeLayer()

        if not layer or not isinstance(layer, QgsVectorLayer):
            QgisMessageUtil.bar_critical(
                self.iface,
                "Selecione uma camada vetorial"
            )
            return None


        if require_editable and not self.ensure_editable(layer):
            return None


        return layer

    def ensure_has_features(self, layer):
        """
        Verifica se a camada possui feições.

        :param layer: Camada vetorial a ser validada
        :type layer: QgsVectorLayer

        :return: True se houver feições, False caso contrário
        :rtype: bool
        """
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
        # filters include common vector formats; QGIS will add drivers as available        
        f, _ = QFileDialog.getSaveFileName(self, 'Salvar como', target_line_edit.text() or '', filters)
        if f:
            target_line_edit.setText(f)

    def select_file(self, target_line_edit: QLineEdit, filters: str):
        f, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar arquivo",
            "",
            filters
        )
        if f:
            target_line_edit.setText(f)
              
    def apply_qml_style(
        self,
        layer: QgsVectorLayer,
        qml_path: str
    ) -> bool:

        if not isinstance(layer, QgsVectorLayer):
            return False

        if not qml_path or not os.path.exists(qml_path):
            return False

        ok = layer.loadNamedStyle(qml_path)
        if isinstance(ok, tuple):
            ok = ok[0]

        if ok:
            layer.triggerRepaint()

        return bool(ok)
    
    def save_vector_layer(self,layer, output_path, save_to_folder, output_name = "LAYER_OUTPUT"):
        # -------------------------------------------------
        # 6) salvar em disco (se solicitado)
        # -------------------------------------------------
        final_layer = layer.materialize(
            QgsFeatureRequest()
        )
        layer = None  # liberar memória 


        if save_to_folder and output_path:

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
                LogUtilsOld.log("toolkey", "Overwrite solicitado pelo usuário.")
            
            #-------------------------------------------------
        
            saved_path = VectorUtils.save_layer(
                layer=final_layer,
                output_path=output_path,
                decision=decision
            )

            if not saved_path:
                QgisMessageUtil.bar_critical(
                    self.iface,
                    f'Operação cancelada ou falha ao salvar. Vefifique se o arquivo esta carregado no projeto e tenten novamente.'                    
                )
                return None
            #---------------------------------------------------
            final_layer = QgsVectorLayer(
                saved_path,
                Path(saved_path).stem,
                "ogr"
            )


        if not isinstance(final_layer, QgsVectorLayer) or not final_layer.isValid():
            QgisMessageUtil.modal_error(
                self.iface,
                "Camada salva é inválida."
            )
            return None


        # -------------------------------------------------
        # 7) adicionar ao projeto
        # -------------------------------------------------
        # garantir que o QGIS liberou o lock do arquivo
        if save_to_folder:
            output_name = Path(output_path).stem
        final_layer.setName(output_name)
        QgsProject.instance().addMapLayer(final_layer)

        return final_layer

