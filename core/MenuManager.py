# -*- coding: utf-8 -*-
from qgis.PyQt.QtWidgets import QMenu, QAction
from .ToolRegistry import ToolRegistry
from ..resources.widgets.DropdownToolButton import DropdownToolButton
from ..core.config.LogUtils import LogUtils
from ..utils.ToolKeys import ToolKey


class MenuManager:
    SYSTEM = "SYSTEM"#1
    LAYOUTS = "LAYOUTS"#2
    FOLDER = "FOLDER"#3
    VECTOR = "VECTOR"#4
    AGRICULTURE = "AGRICULTURE"#5
    RASTER = "RASTER"#6

    def __init__(self, iface,tools=None):
        self.iface = iface
        self.menu = None
        self.submenus = {}
        self.toolbar = None
        self.tools = tools if tools is not None else []
        self.logger = LogUtils(tool=ToolKey.SYSTEM, class_name="MenuManager")
        self._create_actions_for_tools()

    def _create_actions_for_tools(self):
        """Cria QActions para todas as ferramentas e conecta executores."""
        for tool in self.tools:
            tool.action = QAction(tool.icon, tool.name)
            tool.action.setToolTip(tool.tooltip or tool.name)
            tool.action.setData(tool)
            if tool.executor is not None:
                tool.action.triggered.connect(tool.executor)
        self.logger.debug("Actions criadas para todas as ferramentas")

    def create_menu(self):
        self.menu = QMenu("Cadmus", self.iface.mainWindow())
        self.menu.setObjectName("Cadmus")
        standard_menu = self.iface.firstRightStandardMenu()
        self.iface.mainWindow().menuBar().insertMenu(standard_menu.menuAction(), self.menu)

        for category in [
            self.SYSTEM,
            self.LAYOUTS,
            self.FOLDER,
            self.VECTOR,
            self.AGRICULTURE,
            self.RASTER,
        ]:
            submenu = QMenu(category.title(), self.menu)
            self.submenus[category] = submenu
            self.menu.addMenu(submenu)

        self.logger.debug("Menus principais criados")

    def create_toolbar(self):
        self.toolbar = self.iface.addToolBar("Cadmus")
        self.toolbar.setObjectName("Cadmus_Toolbar")

        # Adicionar toolbars por main_action por categoria, respeitando show_in_toolbar e order
        for category in [
            self.SYSTEM,
            self.LAYOUTS,
            self.FOLDER,
            self.VECTOR,
            self.AGRICULTURE,
            self.RASTER,
        ]:
            main_tools = [t for t in self.tools if t.category == category and t.main_action and t.show_in_toolbar]
            secondary_actions = [t.action for t in sorted([t for t in self.tools if t.category == category and not t.main_action and t.show_in_toolbar], key=lambda x: x.order)]

            if not main_tools:
                continue

            main_tool = main_tools[0]
            dropdown = DropdownToolButton(
                iface=self.iface,
                title=main_tool.name,
                main_action=main_tool.action,
                secondary_actions=secondary_actions,
                icon=main_tool.icon,
            )
            self.toolbar.addAction(dropdown.action)
            self.toolbar.addSeparator()

        self.logger.debug("Toolbar preenchida a partir do ToolRegistry")

    def populate_menus(self):
        # Ordenar ferramentas por order dentro de cada categoria
        for category in [self.SYSTEM, self.LAYOUTS, self.FOLDER, self.VECTOR, self.AGRICULTURE, self.RASTER]:
            if category not in self.submenus:
                continue
            sorted_tools = sorted([t for t in self.tools if t.category == category], key=lambda x: x.order)
            for tool in sorted_tools:
                self.submenus[category].addAction(tool.action)
        self.logger.debug("Submenus populados com ferramentas (ordenadas)")

    def unload(self):
        if self.menu:
            self.iface.mainWindow().menuBar().removeAction(self.menu.menuAction())
            self.menu = None
        if self.toolbar:
            self.iface.mainWindow().removeToolBar(self.toolbar)
            self.toolbar = None
        self.submenus.clear()
        self.logger.debug("MenuManager unloaded")
