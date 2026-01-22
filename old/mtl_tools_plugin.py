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
        icon = QIcon(os.path.join(os.path.dirname(__file__), "icons", "agriculture.png"))
        self.agriculture_menu.setIcon(icon)
        self.layers_menu = QMenu("Camadas", self.menu)
        icon = QIcon(os.path.join(os.path.dirname(__file__), "icons", "layer.png"))
        self.layers_menu.setIcon(icon)
        self.layouts_menu = QMenu("Layouts", self.menu)
        icon = QIcon(os.path.join(os.path.dirname(__file__), "icons", "layout.png"))
        self.layouts_menu.setIcon(icon)
        self.raster_menu = QMenu("Raster", self.menu)
        icon = QIcon(os.path.join(os.path.dirname(__file__), "icons", "raster.png"))
        self.raster_menu.setIcon(icon)
        self.system_menu = QMenu("Sistema", self.menu)
        icon = QIcon(os.path.join(os.path.dirname(__file__), "icons", "system.png"))
        self.system_menu.setIcon(icon)
        self.vectors_menu = QMenu("Vetores", self.menu)
        icon = QIcon(os.path.join(os.path.dirname(__file__), "icons", "vector.png"))
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
        # Export All Layouts
        export_icon = os.path.join(os.path.dirname(__file__), "icons", "export_icon.png")
        self.action_export_all = QAction(QIcon(export_icon), "Exportar todos os Layouts", self.iface.mainWindow())
        self.action_export_all.triggered.connect(self.run_export_layouts)

        # Replace in Layouts
        replace_icon = os.path.join(os.path.dirname(__file__), "icons", "replace_in_layouts.png")
        self.action_replace_layouts = QAction(QIcon(replace_icon), "Substituir textos nos Layouts", self.iface.mainWindow())
        self.action_replace_layouts.triggered.connect(self.run_replace_layouts)

        # Restart QGIS
        restart_icon = os.path.join(os.path.dirname(__file__), "icons", "restart_qgis.png")
        self.action_restart_qgis = QAction(QIcon(restart_icon), "Salvar, Fechar e Reabrir Projeto", self.iface.mainWindow())
        self.action_restart_qgis.triggered.connect(self.run_restart_qgis)

        # Carregar pasta de arquivos
        load_icon = os.path.join(os.path.dirname(__file__), "icons", "load_folder.png")
        self.action_load_folder = QAction(QIcon(load_icon), "Carregar pasta de arquivos", self.iface.mainWindow())
        self.action_load_folder.triggered.connect(self.run_load_folder)

        # Gerar Rastro Implemento
        gerar_icon = os.path.join(os.path.dirname(__file__), "icons", "gerar_rastro.png")
        self.action_gerar_rastro = QAction(QIcon(gerar_icon), "Gerar Rastro Implemento", self.iface.mainWindow())
        self.action_gerar_rastro.triggered.connect(self.run_gerar_rastro)

        # About Dialog
        about_icon = os.path.join(os.path.dirname(__file__), "icons", "about.png")
        self.action_about_dialog = QAction(QIcon(about_icon), "Sobre o MTL Tools", self.iface.mainWindow())
        self.action_about_dialog.triggered.connect(self.run_about_dialog)
        # base tool
        base_tool_icon = os.path.join(os.path.dirname(__file__), "icons", "mtl_agro.png")
        self.action_base_tool = QAction(QIcon(base_tool_icon), "Sobre o MTL Tools", self.iface.mainWindow())
        self.action_base_tool.triggered.connect(self.run_base_tool)


        # Capturar Coordenadas
        coord_icon = os.path.join(os.path.dirname(__file__), "icons", "coord.png")
        self.action_coord_click = QAction(QIcon(coord_icon), "Capturar Coordenadas", self.iface.mainWindow())
        self.action_coord_click.triggered.connect(self.run_coord_click)
        
        
        # Calcular campos vetoriais
        vector_field_icon = os.path.join(os.path.dirname(__file__), "icons", "vector_field.png")
        self.action_vector_fields = QAction(QIcon(vector_field_icon), "Calcular Campos Vetoriais", self.iface.mainWindow())
        self.action_vector_fields.triggered.connect(self.run_vector_fields)      


        # Obter coordenadas de drone
        drone_coord_icon = os.path.join(os.path.dirname(__file__), "icons", "drone_cordinates.png")
        self.action_drone_coords = QAction(QIcon(drone_coord_icon), "Obter Coordenadas de Drone", self.iface.mainWindow())
        self.action_drone_coords.triggered.connect(self.run_drone_coords)

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
        self.menu.addAction(self.action_base_tool)

        # -------------------------
        # 6) TOOLBAR
        # -------------------------
        # Sistema
        self.toolbar.addAction(self.action_restart_qgis)

        # Layouts (com dropdown)
        layouts_button = QToolButton()
        layouts_button.setText("Layouts")
        layouts_button.setIcon(self.action_export_all.icon())
        layouts_menu_for_toolbar = QMenu(self.iface.mainWindow())
        layouts_menu_for_toolbar.addAction(self.action_export_all)
        layouts_menu_for_toolbar.addAction(self.action_replace_layouts)
        layouts_button.setMenu(layouts_menu_for_toolbar)
        layouts_button.setPopupMode(QToolButton.MenuButtonPopup)
        layouts_button.clicked.connect(self.run_export_layouts)
        layouts_widget_action = QWidgetAction(self.toolbar)
        layouts_widget_action.setDefaultWidget(layouts_button)
        self.toolbar.addAction(layouts_widget_action)

        # Camadas
        self.toolbar.addAction(self.action_load_folder)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.action_drone_coords)
        self.toolbar.addSeparator()

        # --------------------------------------------------
        # Vetores (com dropdown)
        # --------------------------------------------------
        vectors_button = QToolButton()
        vectors_button.setText("Vetores")
        vectors_button.setIcon(self.action_vector_fields.icon())

        vectors_menu_for_toolbar = QMenu(self.iface.mainWindow())
        vectors_menu_for_toolbar.addAction(self.action_vector_fields)  # principal
        vectors_menu_for_toolbar.addAction(self.action_coord_click)

        vectors_button.setMenu(vectors_menu_for_toolbar)
        vectors_button.setDefaultAction(self.action_vector_fields)  # 👈 ESSENCIAL
        vectors_button.setPopupMode(QToolButton.MenuButtonPopup)


        vectors_widget_action = QWidgetAction(self.toolbar)
        vectors_widget_action.setDefaultWidget(vectors_button)
        self.toolbar.addAction(vectors_widget_action)

        self.toolbar.addSeparator()


        # --------------------------------------------------
        # Agricultura de Precisão (com dropdown)
        # --------------------------------------------------
        agro_button = QToolButton()
        agro_button.setText("Agricultura de Precisão")
        agro_button.setIcon(self.action_gerar_rastro.icon())

        agro_menu_for_toolbar = QMenu(self.iface.mainWindow())
        agro_menu_for_toolbar.addAction(self.action_gerar_rastro)

        agro_button.setMenu(agro_menu_for_toolbar)
        agro_button.setPopupMode(QToolButton.MenuButtonPopup)
        agro_button.clicked.connect(self.action_gerar_rastro.trigger)

        agro_widget_action = QWidgetAction(self.toolbar)
        agro_widget_action.setDefaultWidget(agro_button)
        self.toolbar.addAction(agro_widget_action)

        self.toolbar.addSeparator()

        # Raster (espaço reservado)
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
            self.action_drone_coords
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

    # =====================================================
    # EXECUTAR: Export All Layouts
    # ===============================================   ======
    def run_export_layouts(self):
        from .plugins.export_all_layouts import ExportAllLayoutsDialog
        dlg = ExportAllLayoutsDialog(self.iface)
        dlg.exec()

    # =====================================================
    # EXECUTAR: Replace Text in Layouts
    # =====================================================
    def run_replace_layouts(self):
        from .plugins.replace_in_layouts import run_replace_in_layouts
        run_replace_in_layouts(self.iface)

    # =====================================================
    # EXECUTAR: Restart QGIS
    # =====================================================
    def run_restart_qgis(self):
        from .plugins.restart_qgis import run_restart_qgis
        run_restart_qgis(self.iface)

    # =====================================================
    # EXECUTAR: Load Folder Layers
    # =====================================================
    def run_load_folder(self):
        from .plugins.load_folder_layers import run_load_folder_layers
        run_load_folder_layers(self.iface)

    # =====================================================
    # EXECUTAR: Gerar Rastro Implemento (painel)
    # =====================================================
    def run_gerar_rastro(self):
        from .plugins.gerar_rastro_plugin import run_gerar_rastro
        self.gerar_rastro_dlg = run_gerar_rastro(self.iface)

        
    # =====================================================
    # EXECUTAR: About Dialog
    # =====================================================
    def run_about_dialog(self):
        from .plugins.about_dialog import run_about_dialog
        run_about_dialog(self.iface)
        
    # =====================================================
    # EXECUTAR: Obter Coordenadas ao Clicar no Mapa
    # =====================================================
    def run_coord_click(self):
        from .plugins.coord_click_tool import CoordClickTool

        # manter referência viva
        self.coord_click_tool = CoordClickTool(self.iface)

        self.iface.mapCanvas().setMapTool(self.coord_click_tool)
        
    # =====================================================
    # EXECUTAR: Calcular Campos Vetoriais
    # =====================================================
    def run_vector_fields(self):
        from .plugins.vector_field_plugin import VectorFieldPlugin
        # manter referência viva
        self.vector_field_plugin = VectorFieldPlugin(self.iface)
        self.vector_field_plugin.run_vector_field()
        
    # =====================================================
    # EXECUTAR: Obter Coordenadas de Drone
    # =====================================================
    def run_drone_coords(self):
        from .plugins.drone_cordinates import run_drone_cordinates
        self.drone_cordinates_dlg =run_drone_cordinates(self.iface)

    # =====================================================
    # EXECUTAR: Base Tool
    # =====================================================
    def run_base_tool(self):
        from .plugins.base_tool import run_base_tool
        run_base_tool(self.iface)
        