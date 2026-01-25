# -*- coding: utf-8 -*-

from qgis.PyQt.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QCheckBox, QLineEdit, QPushButton
)
from ...utils.string_utils import StringUtils


class QmlSelectorWidget(QWidget):
    """
    Widget exclusivo para seleção opcional de arquivo QML.
    """

    def __init__(
        self,
        *,
        checkbox_text="Aplicar estilo (QML) ao resultado",
        label_text="QML:",
        file_filter=StringUtils.FILTER_QGIS_STYLE,
        file_dialog_callback=None,
        parent=None
    ):
        super().__init__(parent)

        if file_dialog_callback is None:
            raise ValueError("file_dialog_callback é obrigatório")

        self._file_dialog_callback = file_dialog_callback
        self._file_filter = file_filter

        self._chk = QCheckBox(checkbox_text)
        self._txt = QLineEdit()
        self._btn = QPushButton("...")

        self._build_ui(label_text)
        self._bind_events()

    # --------------------------------------------------
    # UI
    # --------------------------------------------------
    def _build_ui(self, label_text):
        layout = QVBoxLayout(self)

        layout.addWidget(self._chk)

        row = QHBoxLayout()
        row.addWidget(QLabel(label_text))
        row.addWidget(self._txt)
        row.addWidget(self._btn)

        layout.addLayout(row)

        self._txt.setEnabled(False)
        self._btn.setEnabled(False)

    # --------------------------------------------------
    # Bindings
    # --------------------------------------------------
    def _bind_events(self):
        self._chk.toggled.connect(self._update_enabled_state)

        self._btn.clicked.connect(
            lambda: self._file_dialog_callback(
                self._txt,
                self._file_filter
            )
        )

        self._update_enabled_state()

    def _update_enabled_state(self):
        enabled = self._chk.isChecked()
        self._txt.setEnabled(enabled)
        self._btn.setEnabled(enabled)

    # --------------------------------------------------
    # API pública
    # --------------------------------------------------
    def is_enabled(self) -> bool:
        return self._chk.isChecked()

    def qml_path(self) -> str:
        return self._txt.text().strip()

    def set_qml_path(self, path: str):
        self._txt.setText(path or "")
