from qgis.PyQt.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QCheckBox, QLabel
from ...resources.styles.Styles import Styles

class CheckboxGridWidget(QWidget):
    """
    Widget exclusivo para grid de checkboxes com suporte a dicionário chave→label.
    """
    def __init__(self, options_dict, *, items_per_row=3, checked_by_default=False, title=None, parent=None):
        super().__init__(parent)
        self.options_dict = options_dict
        self.items_per_row = items_per_row
        self.checked_by_default = checked_by_default
        self.title = title
        self.checkbox_map = {}
        self._build()

    def _build(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(0)

        if self.title:
            lbl = QLabel(self.title)
            lbl.setStyleSheet("font-weight: bold;")
            layout.addWidget(lbl)
            layout.addSpacing(6)

        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(Styles.LAYOUT_H_SPACING)
        grid.setVerticalSpacing(Styles.LAYOUT_V_SPACING)

        for idx, (key, label) in enumerate(self.options_dict.items()):
            row = idx // self.items_per_row
            col = idx % self.items_per_row
            chk = QCheckBox(label)
            chk.setChecked(self.checked_by_default)
            chk.setFixedHeight(14)
            grid.addWidget(chk, row, col)
            self.checkbox_map[key] = chk

        for col in range(self.items_per_row):
            grid.setColumnStretch(col, 1)
        layout.addLayout(grid)
        self.setLayout(layout)

    def get_checkbox(self, key):
        return self.checkbox_map.get(key)

    def get_checkbox_map(self):
        return self.checkbox_map
