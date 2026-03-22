# -*- coding: utf-8 -*-
from qgis.PyQt.QtWidgets import QMenu
from .ToolRegistry import ToolRegistry
from ..resources.widgets.DropdownToolButton import DropdownToolButton
from ..core.config.LogUtils import LogUtils
from ..utils.ToolKeys import ToolKey


class MenuManager:
    SYSTEM = "SYSTEM"
    VECTOR = "VECTOR"
    AGRICULTURE = "AGRICULTURE"
    LAYOUTS = "LAYOUTS"
    RASTER = "RASTER"

    def __init__(self, iface,tools=None):
        self.iface = iface
        self.menu = None
        self.submenus = {}
        self.toolbar = None
        self.tools = tools if tools is not None else []
        self.logger = LogUtils(tool=ToolKey.SYSTEM, class_name="MenuManager")

    def create_menu(self):
        self.menu = QMenu("Cadmus", self.iface.mainWindow())
        self.menu.setObjectName("Cadmus")
        standard_menu = self.iface.firstRightStandardMenu()
        self.iface.mainWindow().menuBar().insertMenu(standard_menu.menuAction(), self.menu)

        for category in [
            self.SYSTEM,
            self.VECTOR,
            self.AGRICULTURE,
            self.LAYOUTS,
            self.RASTER,
        ]:
            submenu = QMenu(category.title(), self.menu)
            self.submenus[category] = submenu
            self.menu.addMenu(submenu)

        self.logger.debug("Menus principais criados")

    def create_toolbar(self):
        self.toolbar = self.iface.addToolBar("Cadmus")
        self.toolbar.setObjectName("Cadmus_Toolbar")

        # Adicionar toolbars por main_action por categoria
        for category in [
            self.SYSTEM,
            self.LAYOUTS,
            self.VECTOR,
            self.AGRICULTURE,
            self.RASTER,
        ]:
            main_tools = [t for t in self.tools if t.category == category and t.main_action]
            secondary_actions = [t.action for t in self.tools if t.category == category and not t.main_action]

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
        for tool in self.tools:
            category = tool.category
            if category not in self.submenus:
                continue
            self.submenus[category].addAction(tool.action)
        self.logger.debug("Submenus populados com ferramentas")

    def unload(self):
        if self.menu:
            self.iface.mainWindow().menuBar().removeAction(self.menu.menuAction())
            self.menu = None
        if self.toolbar:
            self.iface.mainWindow().removeToolBar(self.toolbar)
            self.toolbar = None
        self.submenus.clear()
        self.logger.debug("MenuManager unloaded")
