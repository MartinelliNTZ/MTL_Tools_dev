# -*- coding: utf-8 -*-
from qgis.PyQt.QtWidgets import QAction
from ..config.LogUtils import LogUtils
from ...utils.ToolKeys import ToolKey


class Tool:
    """Abstração de ferramenta para menu/toolbar do plugin."""

    def __init__(
        self,
        name,
        icon,
        category,
        tool_type,
        main_action=False,
        executor=None,
        executor_name=None,
        tooltip=None,
    ):
        self.logger = LogUtils(tool=ToolKey.SYSTEM, class_name="Tool")

        self.name = name
        self.icon = icon
        self.category = category
        self.tool_type = tool_type
        self.main_action = main_action
        self.executor = executor
        self.executor_name = executor_name

        self.action = QAction(icon, name)
        self.action.setToolTip(tooltip or name)
        self.action.setData(self)

        if executor is not None:
            self.action.triggered.connect(executor)

    def set_executor(self, executor):
        self.executor = executor
        try:
            self.action.triggered.disconnect()
        except Exception as e:
            self.logger.error(f"Falha ao desconectar executor anterior: {e}")
        self.action.triggered.connect(executor)

