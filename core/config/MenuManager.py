# -*- coding: utf-8 -*-
from qgis.PyQt.QtWidgets import QMenu, QAction, QToolBar
from ...resources.IconManager import IconManager as im
from ...resources.widgets.DropdownToolButton import DropdownToolButton
from .LogUtils import LogUtils
from ...utils.ToolKeys import ToolKey
from ...utils.Preferences import Preferences
from ...utils.StringManager import StringManager


class MenuManager:
    def __init__(self, iface, tools=None, logger=None):
        self.iface = iface
        self.menu = None
        self.submenus = {}
        self.toolbar = None
        self.tools = tools if tools is not None else []
        self.TOOLKEY = ToolKey.SYSTEM
        self.logger = LogUtils(tool=self.TOOLKEY, class_name="MenuManager")
        self._create_actions_for_tools()
        self.prefs = Preferences.load_tool_prefs(self.TOOLKEY)
        self.logger.debug(
            f"MenuManager: {self.menu}. Tools: {self.tools}. "
            f"Toolbar: {self.toolbar}."
        )

    def _create_actions_for_tools(self):
        """Cria QActions para todas as ferramentas e conecta executores."""
        for tool in self.tools:
            tool.action = QAction(tool.icon, tool.name, self.iface.mainWindow())
            tool.action.setToolTip(tool.tooltip or tool.name)
            tool.action.setData(tool)
            if tool.executor is not None:
                tool.action.triggered.connect(tool.executor)
        self.logger.debug("Actions criadas para todas as ferramentas")

    def create_menu(self):
        self.logger.debug("Iniciando criação do menu")
        self.menu = QMenu("Cadmus", self.iface.mainWindow())
        self.menu.setObjectName("Cadmus")
        standard_menu = self.iface.firstRightStandardMenu()
        self.iface.mainWindow().menuBar().insertMenu(
            standard_menu.menuAction(), self.menu
        )

        # Mapeamento de categoria para ícone
        category_icons = {
            "SYSTEM": im.icon(im.SYSTEM),
            "LAYOUTS": im.icon(im.LAYOUT),
            "FOLDER": im.icon(im.LAYER),  # Usar ícone de layer para folder
            "VECTOR": im.icon(im.VECTOR),
            "AGRICULTURE": im.icon(im.AGRICULTURE),
            "RASTER": im.icon(im.RASTER),
        }
        self.logger.debug(
            f"Criando submenus para cada categoria: {list(category_icons.keys())}"
        )
        for category, label in StringManager.MENU_CATEGORIES.items():
            submenu = QMenu(label, self.menu)
            if category in category_icons:
                submenu.setIcon(category_icons[category])
            self.submenus[category] = submenu
            self.menu.addMenu(submenu)
            self.logger.debug(
                f"Submenu '{category}' criado com ícone: {category_icons.get(category)}"
            )

        self.logger.debug("Menus principais criados")

    def create_toolbar(self):
        self.logger.debug(f"Iniciando toolbar:Total de ferramentas: {len(self.tools)}")
        self.toolbar = QToolBar("Cadmus", self.iface.mainWindow())
        self.toolbar.setObjectName("Cadmus_Toolbar")
        self.iface.addToolBar(self.toolbar)
        self.logger.debug(
            f"Toolbar criada e adicionada ao QGIS: {self.toolbar.objectName()}"
        )

        self.logger.debug(
            f"Toolbar criada e adicionada ao QGIS: {self.toolbar.objectName()}"
        )

        # Coletar todos os dropdown buttons por categoria
        dropdown_buttons = []

        for category in StringManager.MENU_CATEGORIES:
            self.logger.debug(f"Verificando categoria {category}")
            all_tools_in_category = [t for t in self.tools if t.category == category]
            self.logger.debug(
                f"Total de ferramentas na categoria {category}: {len(all_tools_in_category)}"
            )

            main_tools = [
                t
                for t in self.tools
                if t.category == category and t.main_action and t.show_in_toolbar
            ]
            self.logger.debug(f"Main tools na categoria {category}: {len(main_tools)}")

            secondary_tools = [
                t
                for t in self.tools
                if t.category == category and not t.main_action and t.show_in_toolbar
            ]
            self.logger.debug(
                f"Secondary tools na categoria {category}: {len(secondary_tools)}"
            )

            if not main_tools:
                self.logger.debug(
                    f"Pulando categoria {category} - nenhum main_tool encontrado"
                )
                continue

            main_tool = main_tools[0]
            self.logger.debug(
                f"Criando dropdown para categoria {category} com main_tool: {main_tool.name}"
            )
            secondary_actions = [
                t.action for t in sorted(secondary_tools, key=lambda x: x.order)
            ]
            self.logger.debug(f"Secondary actions: {len(secondary_actions)}")

            dropdown = DropdownToolButton(
                iface=self.iface,
                title=main_tool.name,
                main_action=main_tool.action,
                secondary_actions=secondary_actions,
                icon=main_tool.icon,  # Adicionado ícone
            )
            self.logger.debug(
                f"Dropdown criado com text: {dropdown.text() if hasattr(dropdown, 'text') else 'None'}"
            )
            dropdown_buttons.append(dropdown)

        # TESTE: Adicionar main_actions diretamente sem DropdownToolButton
        if dropdown_buttons:
            self.logger.debug(
                f"Adicionando {len(dropdown_buttons)} botões dropdown à toolbar"
            )
            for button in dropdown_buttons:
                self.logger.debug(f"Adicionando botão: {button.text()}")
                self.toolbar.addWidget(button)
                self.logger.debug(f"Botão '{button.text()}' adicionado à toolbar")
                # Adicionar separador após cada botão, exceto o último
                if button != dropdown_buttons[-1]:
                    self.toolbar.addSeparator()
        else:
            # Fallback: adicionar main_actions diretamente
            self.logger.warning(
                "Nenhum botão dropdown criado, tentando adicionar main_actions diretamente"
            )
            for category in (
                "SYSTEM",
                "LAYOUTS",
                "VECTOR",
                "AGRICULTURE",
            ):
                main_tools = [
                    t
                    for t in self.tools
                    if t.category == category and t.main_action and t.show_in_toolbar
                ]
                if main_tools:
                    main_tool = main_tools[0]
                    self.logger.debug(
                        f"Adicionando main_action diretamente: {main_tool.name}"
                    )
                    self.toolbar.addAction(main_tool.action)
                    self.toolbar.addSeparator()

    def populate_menus(self):
        # Ordenar ferramentas por order dentro de cada categoria
        for category in StringManager.MENU_CATEGORIES:
            if category not in self.submenus:
                continue
            sorted_tools = sorted(
                [t for t in self.tools if t.category == category], key=lambda x: x.order
            )
            for tool in sorted_tools:
                self.submenus[category].addAction(tool.action)
        self.logger.debug("Submenus populados com ferramentas (ordenadas)")

    def unload(self):
        # Remover ações do menu
        for tool in self.tools:
            if tool.action:
                self.iface.removePluginMenu("Cadmus", tool.action)

        # Remover menu principal
        if self.menu:
            self.iface.mainWindow().menuBar().removeAction(self.menu.menuAction())
            # Importante: deletar o menu após remover
            self.menu.deleteLater()
            self.menu = None

        # Remover toolbar - MÉTODO CORRETO
        if self.toolbar:
            # Remove da interface
            self.iface.mainWindow().removeToolBar(self.toolbar)
            # Força a destruição do objeto
            self.toolbar.deleteLater()
            # self.toolbar = None

        self.submenus.clear()
        self.logger.debug("MenuManager unloaded")
