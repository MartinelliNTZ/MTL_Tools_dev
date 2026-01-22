# -*- coding: utf-8 -*-
import os
from qgis.PyQt.QtWidgets import QAction, QMenu
from qgis.PyQt.QtGui import QIcon
from qgis.core import QgsApplication
from qgis.PyQt.QtWidgets import QAction, QMenu, QToolButton, QWidgetAction


from .processing.provider import MTLProvider


class MTL_Tools:
    def __init__(self, iface):
        self.iface = iface
        self.menu = None
        self.toolbar = None
        self.actions = []
        self.provider = None

    # =====================================================
    # INICIAR GUI E PROCESSING
    # =====================================================
    def initGui(self):

        # -------------------------
        # 1) ATIVAR PROCESSING PROVIDER
        # -------------------------
        self.provider = MTLProvider()
        QgsApplication.processingRegistry().addProvider(self.provider)

        # -------------------------
        # 2) CRIAR TOOLBAR EXCLUSIVA
        # -------------------------
        self.toolbar = self.iface.addToolBar("MTL Tools")
        self.toolbar.setObjectName("MTL_Tools_Toolbar")

        # -------------------------
        # 3) MENU PRINCIPAL E SUBMENUS
        # -------------------------
        self.menu = QMenu("MTL Tools", self.iface.mainWindow())
        self.menu.setObjectName("MTL_Tools")
        standard_menu = self.iface.firstRightStandardMenu()
        self.iface.mainWindow().menuBar().insertMenu(standard_menu.menuAction(), self.menu)
        self.menu.clear()
        

    
     

        # Submenus        
        self.agriculture_menu = QMenu("Agricultura de Precisão", self.menu)
        icon = QIcon(os.path.join(os.path.dirname(__file__),"resources", "icons", "agriculture.ico"))
        self.agriculture_menu.setIcon(icon)
        self.layers_menu = QMenu("Camadas", self.menu)
        icon = QIcon(os.path.join(os.path.dirname(__file__),"resources", "icons", "layer.ico"))
        self.layers_menu.setIcon(icon)
        self.layouts_menu = QMenu("Layouts", self.menu)
        icon = QIcon(os.path.join(os.path.dirname(__file__),"resources", "icons", "layout.ico"))
        self.layouts_menu.setIcon(icon)
        self.raster_menu = QMenu("Raster", self.menu)
        icon = QIcon(os.path.join(os.path.dirname(__file__),"resources", "icons", "raster.ico"))
        self.raster_menu.setIcon(icon)
        self.system_menu = QMenu("Sistema", self.menu)
        icon = QIcon(os.path.join(os.path.dirname(__file__),"resources", "icons", "system.ico"))
        self.system_menu.setIcon(icon)
        self.vectors_menu = QMenu("Vetores", self.menu)
        icon = QIcon(os.path.join(os.path.dirname(__file__),"resources", "icons", "vector.ico"))
        self.vectors_menu.setIcon(icon)

        # Adiciona submenus ao menu principal
        self.menu.addMenu(self.agriculture_menu)
        self.menu.addMenu(self.layers_menu)
        self.menu.addMenu(self.layouts_menu)
        self.menu.addMenu(self.raster_menu)
        self.menu.addMenu(self.vectors_menu)
        self.menu.addMenu(self.system_menu)

        # -------------------------
        # 4) CONFIGURAÇÃO DAS AÇÕES (ORDEM NUMÉRICA)
        # -------------------------
        # 1-Export All Layouts
        export_icon = os.path.join(os.path.dirname(__file__),"resources", "icons", "export_icon.ico")
        self.action_export_all = QAction(QIcon(export_icon), "Exportar todos os Layouts", self.iface.mainWindow())
        self.action_export_all.triggered.connect(self.run_export_layouts)

        # 2-Replace in Layouts
        replace_icon = os.path.join(os.path.dirname(__file__),"resources", "icons", "replace_in_layouts.ico")
        self.action_replace_layouts = QAction(QIcon(replace_icon), "Substituir textos nos Layouts", self.iface.mainWindow())
        self.action_replace_layouts.triggered.connect(self.run_replace_layouts)

        # 3-Restart QGIS
        restart_icon = os.path.join(os.path.dirname(__file__),"resources", "icons", "restart_qgis.ico")
        self.action_restart_qgis = QAction(QIcon(restart_icon), "Salvar, Fechar e Reabrir Projeto", self.iface.mainWindow())
        self.action_restart_qgis.triggered.connect(self.run_restart_qgis)

        # 4-Carregar pasta de arquivos
        load_icon = os.path.join(os.path.dirname(__file__),"resources", "icons", "load_folder.ico")
        self.action_load_folder = QAction(QIcon(load_icon), "Carregar pasta de arquivos", self.iface.mainWindow())
        self.action_load_folder.triggered.connect(self.run_load_folder)

        # 5-Gerar Rastro Implemento
        gerar_icon = os.path.join(os.path.dirname(__file__),"resources", "icons", "gerar_rastro.ico")
        self.action_gerar_rastro = QAction(QIcon(gerar_icon), "Gerar Rastro Implemento", self.iface.mainWindow())
        self.action_gerar_rastro.triggered.connect(self.run_gerar_rastro)

        # 6-About Dialog
        about_icon = os.path.join(os.path.dirname(__file__),"resources", "icons", "about.ico")
        self.action_about_dialog = QAction(QIcon(about_icon), "Sobre o MTL Tools", self.iface.mainWindow())
        self.action_about_dialog.triggered.connect(self.run_about_dialog)
        
        # null-base tool
        base_tool_icon = os.path.join(os.path.dirname(__file__),"resources", "icons", "mtl_agro.ico")
        self.action_base_tool = QAction(QIcon(base_tool_icon), "Base Tool", self.iface.mainWindow())
        self.action_base_tool.triggered.connect(self.run_base_tool)


        # 7-Capturar Coordenadas
        coord_icon = os.path.join(os.path.dirname(__file__),"resources", "icons", "coord.ico")
        self.action_coord_click = QAction(QIcon(coord_icon), "Capturar Coordenadas", self.iface.mainWindow())
        self.action_coord_click.triggered.connect(self.run_coord_click)
        
        
        # 8-Calcular campos vetoriais
        vector_field_icon = os.path.join(os.path.dirname(__file__),"resources", "icons", "vector_field.ico")
        self.action_vector_fields = QAction(QIcon(vector_field_icon), "Calcular Campos Vetoriais", self.iface.mainWindow())
        self.action_vector_fields.triggered.connect(self.run_vector_fields)      


        # 09-Obter coordenadas de drone
        drone_coord_icon = os.path.join(os.path.dirname(__file__),"resources", "icons", "drone_cordinates.ico")
        self.action_drone_coords = QAction(QIcon(drone_coord_icon), "Obter Coordenadas de Drone", self.iface.mainWindow())
        self.action_drone_coords.triggered.connect(self.run_drone_coords)
        
        # 10-Realizar multipart de todas as feições
        multipart_icon = os.path.join(os.path.dirname(__file__),"resources", "icons", "vector_multpart.ico")
        self.action_multpart = QAction(QIcon(multipart_icon), "Promover a multiparte", self.iface.mainWindow())
        self.action_multpart.triggered.connect(self.run_multpart)

        # 11-Copiar atributos entre camadas
        copy_atributes_icon = os.path.join(os.path.dirname(__file__),"resources", "icons", "copy_attributes.ico")
        self.action_copy_atributes = QAction(QIcon(copy_atributes_icon), "Copiar Atributos", self.iface.mainWindow())
        self.action_copy_atributes.triggered.connect(self.run_copy_atributes)

        # -------------------------
        # 5) ADICIONAR AÇÕES AO MENU (ORDEM ALFABÉTICA)
        # -------------------------
        # Agricultura de Precisão
        self.agriculture_menu.addAction(self.action_gerar_rastro)
        self.agriculture_menu.addAction(self.action_drone_coords)

        # Camadas
        self.layers_menu.addAction(self.action_load_folder)

        # Layouts
        self.layouts_menu.addAction(self.action_export_all)
        self.layouts_menu.addAction(self.action_replace_layouts)

        # Sistema
        self.system_menu.addAction(self.action_restart_qgis)

        # Vetores
        self.vectors_menu.addAction(self.action_coord_click)
        self.vectors_menu.addAction(self.action_vector_fields)

        # Menu principal
        self.menu.addAction(self.action_about_dialog)
        #self.menu.addAction(self.action_base_tool)

        # -------------------------
        # 6) TOOLBAR
        # -------------------------
 
        # ==================================================
        # BOTÃO SISTEMA NA TOOLBAR (com dropdown)
        # ==================================================
        self._add_toolbar_dropdown(
            title="Sistema",
            main_action=self.action_restart_qgis,
            secondary_actions=[self.action_restart_qgis]
        )       

        # ==================================================
        # BOTÃO LAYOUTS NA TOOLBAR (com dropdown)
        # ==================================================
        self._add_toolbar_dropdown(
            title="Layouts",
            main_action=self.action_export_all,
            secondary_actions=[self.action_replace_layouts]
        )

        # ==================================================
        # BOTÃO CAMDAS NA TOOLBAR (com dropdown)
        # ==================================================
        self._add_toolbar_dropdown(
            title="Vetores",
            main_action=self.action_load_folder,
            secondary_actions=[self.action_load_folder]
        )
        # ==================================================
        # BOTÃO "VETORES" NA TOOLBAR (com dropdown)
        # ==================================================
        self._add_toolbar_dropdown(
            title="Vetores",
            #main_action=self.action_vector_fields,#padrao
            main_action=self.action_copy_atributes,#editavel para debug
            secondary_actions=[     self.action_coord_click,    
                                    self.action_copy_atributes,                                                         
                                    self.action_multpart,]
        )
        # ==================================================
        # BOTÃO "AGRICULTURA DE PRECISÃO" NA TOOLBAR (com dropdown)
        # ==================================================
        self._add_toolbar_dropdown(
            title="Agricultura de Precisão",
            main_action=self.action_drone_coords,
            secondary_actions=[self.action_gerar_rastro]
        )        
        # ==================================================
        # BOTÃO "RASTER" NA TOOLBAR (com dropdown)
        # ==================================================

        self.toolbar.addSeparator()

        # Salva todas as ações para cleanup
        self.actions.extend([
            self.action_export_all,
            self.action_replace_layouts,
            self.action_restart_qgis,
            self.action_load_folder,
            self.action_gerar_rastro,
            self.action_about_dialog,
            self.action_coord_click,
            self.action_vector_fields,
            self.action_drone_coords,
            self.action_multpart,
            self.action_copy_atributes
        ])


    # =====================================================
    # DESCARREGAR PLUGIN
    # =====================================================
    def unload(self):

        # Remover provider do Processing
        if self.provider:
            QgsApplication.processingRegistry().removeProvider(self.provider)

        # Remover ações do menu e toolbar
        for act in self.actions:
            self.iface.removePluginMenu("MTL Tools", act)
            self.iface.removeToolBarIcon(act)

        # Remover toolbar
        if self.toolbar:
            del self.toolbar
            
            
#===========================FERRAMENTAS INSTANTANEAS DE SISTEMA===================================================================
    # =====================================================
    # EXECUTAR: Restart QGIS
    # =====================================================
    def run_restart_qgis(self):
        from .plugins.restart_qgis import run_restart_qgis
        run_restart_qgis(self.iface)        

#===========================FERRAMENTAS INSTANTANEAS===================================================================
    # =====================================================
    # EXECUTAR: Calcular Campos Vetoriais
    # =====================================================
    def run_vector_fields(self):
        from .plugins.vector_field_plugin import VectorFieldPlugin
        # manter referência viva
        self.vector_field_plugin = VectorFieldPlugin(self.iface)
        self.vector_field_plugin.run_vector_field()
        
    # =====================================================
    # EXECUTAR: Converter para Multipart
    # =====================================================
    def run_multpart(self):
        from .plugins.vector_multpart_plugin import VectorMultipartPlugin
        # manter referência viva
        self.vector_multpart_plugin = VectorMultipartPlugin(self.iface)
        self.vector_multpart_plugin.run_multpart()
 
#===========================FERRAMENTAS INSTANTANEA COM JANELA DE RESULTADOS=======================================================================
       
    # =====================================================
    # EXECUTAR: Obter Coordenadas ao Clicar no Mapa
    # =====================================================
    def run_coord_click(self):
        from .plugins.coord_click_tool import CoordClickTool        
        self.coord_click_tool = CoordClickTool(self.iface)
        self.iface.mapCanvas().setMapTool(self.coord_click_tool)
        

#===========================FERRAMENTAS DE JANELA COM SAIDA QGIS=======================================================================
    # =====================================================
    # EXECUTAR: Export All Layouts
    # ===============================================   ======
    def run_export_layouts(self):
        from .plugins.export_all_layouts import ExportAllLayoutsDialog
        dlg = ExportAllLayoutsDialog(self.iface)
        dlg.exec()

    # =====================================================
    # EXECUTAR: Gerar Rastro Implemento (painel)
    # =====================================================
    def run_gerar_rastro(self):
        from .plugins.gerar_rastro_plugin import run_gerar_rastro
        self.gerar_rastro_dlg = run_gerar_rastro(self.iface)
        
    # =====================================================
    # EXECUTAR: Obter Coordenadas de Drone
    # =====================================================
    def run_drone_coords(self):
        from .plugins.drone_cordinates import run_drone_cordinates
        self.drone_cordinates_dlg =run_drone_cordinates(self.iface)


       


#===========================FERRAMENTAS DE JANELA SEM SAIDAS=======================================================================
    # =====================================================
    # EXECUTAR: Replace Text in Layouts
    # =====================================================
    def run_replace_layouts(self):
        from .plugins.replace_in_layouts import run_replace_in_layouts
        self.replace_layouts_dlg =run_replace_in_layouts(self.iface)


    # =====================================================
    # EXECUTAR: Load Folder Layers
    # =====================================================
    def run_load_folder(self):
        from .plugins.load_folder_layers import run_load_folder_layers
        run_load_folder_layers(self.iface)

 
    # =====================================================
    # EXECUTAR: About Dialog
    # =====================================================
    def run_about_dialog(self):
        from .plugins.about_dialog import run_about_dialog
        run_about_dialog(self.iface)
        
    # =====================================================
    # EXECUTAR: Base Tool
    # =====================================================
    def run_base_tool(self):
        from .plugins.base_tool import run_base_tool
        run_base_tool(self.iface)
        
    # =====================================================
    # EXECUTAR: Copiar Atributos entre Camadas
    # =====================================================
    def run_copy_atributes(self):
        from .plugins.copy_attributes_plugin import run_copy_attributes
        self.copy_attributes_dlg = run_copy_attributes(self.iface)

        

        
    
        
        
    def _add_toolbar_dropdown(self, title, main_action, secondary_actions=None, icon=None, separator=True):
        """
        Cria um botão dropdown na toolbar com ações principais e secundárias.
        
        :param title: Texto do botão
        :param main_action: QAction que será a ação principal (clicando no botão)
        :param secondary_actions: lista de QActions adicionais no menu dropdown
        :param icon: QIcon opcional para o botão (se None, usa ícone da ação principal)
        :param separator: bool, adiciona separador após o botão
        :return: QWidgetAction criado e adicionado à toolbar
        """
        if secondary_actions is None:
            secondary_actions = []

        # 1️⃣ Criar o botão principal
        button = QToolButton()
        button.setText(title)
        button.setIcon(icon or main_action.icon())

        # 2️⃣ Criar menu dropdown
        menu = QMenu(self.iface.mainWindow())
        menu.addAction(main_action)  # ação principal no topo
        for act in secondary_actions:
            menu.addAction(act)

        # 3️⃣ Configurar o botão
        button.setMenu(menu)
        button.setDefaultAction(main_action)
        button.setPopupMode(QToolButton.MenuButtonPopup)
        #button.clicked.connect(main_action.trigger)

        # 4️⃣ Transformar em widget e adicionar à toolbar
        widget_action = QWidgetAction(self.toolbar)
        widget_action.setDefaultWidget(button)
        self.toolbar.addAction(widget_action)

        # 5️⃣ Separador opcional
        if separator:
            self.toolbar.addSeparator()

        return widget_action



