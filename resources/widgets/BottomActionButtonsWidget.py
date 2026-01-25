# -*- coding: utf-8 -*-

from qgis.PyQt.QtWidgets import QWidget, QHBoxLayout, QPushButton
from ...core.config.LogUtils import LogUtils


class BottomActionButtonsWidget(QWidget):
    """
    Widget padronizado de botões inferiores (Run / Close / Info).
    """

    def __init__(
        self,
        *,
        run_callback,
        close_callback,
        info_callback=None,
        run_text="Executar",
        close_text="Fechar",
        height=24,
        tool_key=None,
        parent=None
    ):
        super().__init__(parent)

        self._tool_key = tool_key
        self._info_callback = info_callback

        LogUtils.log(
            "Inicializando BottomActionButtonsWidget",
            level="DEBUG",
            tool=self._tool_key,
            class_name=self.__class__.__name__,
        )

        self._btn_run = QPushButton(run_text)
        self._btn_close = QPushButton(close_text)
        self._btn_info = QPushButton("ℹ️")

        self._build_ui(height)
        self._bind_callbacks(run_callback, close_callback, info_callback)

    # --------------------------------------------------
    # UI
    # --------------------------------------------------
    def _build_ui(self, height: int):
        layout = QHBoxLayout(self)
        layout.addStretch()

        self._btn_run.setFixedHeight(height)
        self._btn_close.setFixedHeight(height)
        self._btn_info.setFixedWidth(height)
        self._btn_info.setFixedHeight(height)

        layout.addWidget(self._btn_run)
        layout.addWidget(self._btn_close)
        layout.addWidget(self._btn_info)

    # --------------------------------------------------
    # Bindings
    # --------------------------------------------------
    def _bind_callbacks(self, run_cb, close_cb, info_cb):
        self._btn_run.clicked.connect(run_cb)
        self._btn_close.clicked.connect(close_cb)

        if info_cb:
            self._btn_info.clicked.connect(info_cb)
        else:
            self._btn_info.setVisible(False)

    # --------------------------------------------------
    # API pública
    # --------------------------------------------------
    def set_run_enabled(self, enabled: bool):
        LogUtils.log(
            f"set_run_enabled({enabled})",
            level="DEBUG",
            tool=self._tool_key,
            class_name=self.__class__.__name__,
        )
        self._btn_run.setEnabled(enabled)

    def set_info_visible(self, visible: bool):
        LogUtils.log(
            f"set_info_visible({visible})",
            level="DEBUG",
            tool=self._tool_key,
            class_name=self.__class__.__name__,
        )
        self._btn_info.setVisible(visible)
