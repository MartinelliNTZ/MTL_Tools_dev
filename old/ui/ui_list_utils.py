# -*- coding: utf-8 -*-

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QListWidget


class UiListUtils:
    """
    Utilitários de UI para listas com checkboxes
    Comportamento padrão QGIS
    """

    @staticmethod
    def set_checked_state(
        list_widget: QListWidget,
        state: Qt.CheckState
    ):
        """
        Se houver itens selecionados → aplica só neles
        Caso contrário → aplica a todos
        """

        selected = list_widget.selectedItems()

        items = selected if selected else [
            list_widget.item(i)
            for i in range(list_widget.count())
        ]

        for item in items:
            item.setCheckState(state)
