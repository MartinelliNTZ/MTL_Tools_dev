# -*- coding: utf-8 -*-
from qgis.PyQt.QtWidgets import QAction, QMenu


class DropdownToolButton:
    """
    Widget para botão dropdown na toolbar do QGIS.

    Encapsula um QAction com menu dropdown para múltiplas ações,
    compatível com diferentes versões do Qt/PyQt.
    """

    def __init__(self, iface=None, title=None, main_action=None, secondary_actions=None, icon=None):
        """
        Inicializa o botão dropdown.

        :param iface: Interface do QGIS (usado para mainWindow() do menu)
        :param title: Texto do botão
        :param main_action: QAction principal (ação padrão ao clicar)
        :param secondary_actions: Lista de QActions adicionais no menu
        :param icon: QIcon opcional (usa ícone da main_action se None)
        """
        self.action = QAction()
        self.menu = QMenu(iface.mainWindow() if iface else None)
        self.action.setMenu(self.menu)

        if main_action is not None:
            self.setup(title, main_action, secondary_actions, icon)

    def setup(self, title, main_action, secondary_actions=None, icon=None):
        """
        Configura o botão dropdown com ações.

        :param title: Texto do botão
        :param main_action: QAction principal (ação padrão ao clicar)
        :param secondary_actions: Lista de QActions adicionais no menu
        :param icon: QIcon opcional (usa ícone da main_action se None)
        """
        if secondary_actions is None:
            secondary_actions = []

        self.action.setText(title)
        self.action.setIcon(icon or main_action.icon())
        self.action.setToolTip(main_action.toolTip())

        self.menu.clear()
        self.menu.setToolTipsVisible(True)
        self.menu.addAction(main_action)  # Ação principal no topo

        for act in secondary_actions:
            self.menu.addAction(act)

        # Conectar triggered da action à execução da main_action
        self.action.triggered.connect(lambda: main_action.trigger())