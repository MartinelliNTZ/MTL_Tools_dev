from qgis.core import QgsVectorLayer, QgsWkbTypes, QgsMapLayerProxyModel, QgsProject
from qgis.PyQt.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QMessageBox, QCheckBox, QTextEdit, QComboBox, QListWidget, QDoubleSpinBox, QGridLayout, QFrame
)
from qgis.PyQt.QtCore import QObject, QEvent, Qt
from qgis.gui import QgsMapLayerComboBox
from ...utils.string_utils import StringUtils
from ...resources.widgets.LayerInputWidget import LayerInputWidget
from ...resources.widgets.qml_selector_widget import QmlSelectorWidget


class WidgetFactory:
    def __init__(self, combo: QComboBox, iface):
        super().__init__(combo)
        self.combo = combo
        self.iface = iface

    @staticmethod
    def create_qml_selector(
            *,
            parent,
            separator_top=False,
            separator_bottom=True
    ):
        layout = QVBoxLayout()

        if separator_top:
            layout.addWidget(WidgetFactory.create_separator())

        widget = QmlSelectorWidget(
            parent=parent,
            file_dialog_callback=parent.select_file
        )

        layout.addWidget(widget)

        if separator_bottom:
            layout.addWidget(WidgetFactory.create_separator())

        return layout, widget

    @staticmethod
    def create_layer_input(
            label_text,
            filters,
            *,
            allow_empty=True,
            enable_selected_checkbox=True,
            parent=None,
            separator_top=False,
            separator_bottom=True,
    ) -> LayerInputWidget:
        """current_layer() -> QgsMapLayer | None
            only_selected_enabled() -> bool
            set_layer(layer)
            """
        layout = QVBoxLayout()
        if separator_top:
            layout.addWidget(WidgetFactory.create_separator())

        widget = LayerInputWidget(
            label_text=label_text,
            filters=filters,
            allow_empty=allow_empty,
            enable_selected_checkbox=enable_selected_checkbox,
            parent=parent
        )
        layout.addWidget(widget)
        if separator_bottom:
            layout.addWidget(WidgetFactory.create_separator())

        # estilo centralizado (opcional)
        # LayerInputStyles.apply(widgets)

        return layout, widget

    @staticmethod
    def create_double_spin_input(
            label_text,
            *,
            decimals=4,
            step=0.5,
            minimum=0.0,
            maximum=99999999.0,
            value=0.0,
            keyboard_tracking=False
    ):
        """
        Cria um input numérico com label (QDoubleSpinBox)

        Parameters
        ----------
        label_text : str
            Texto do label (posicional)

        decimals : int
            Casas decimais

        step : float
            Incremento do spin

        minimum : float
            Valor mínimo

        maximum : float
            Valor máximo

        value : float
            Valor inicial

        keyboard_tracking : bool
            Atualiza valor enquanto digita
        """

        layout = QHBoxLayout()

        lbl = QLabel(label_text)
        layout.addWidget(lbl)

        spin = QDoubleSpinBox()
        spin.setKeyboardTracking(keyboard_tracking)
        spin.setDecimals(decimals)
        spin.setSingleStep(step)
        spin.setRange(minimum, maximum)
        spin.setValue(value)

        layout.addWidget(spin)

        return layout, spin

    @staticmethod
    def create_checkbox_grid(
            names,
            *,
            items_per_row=3,
            checked_by_default=False,
            h_spacing=10,
            v_spacing=5,
            title=None,
            separator=True
    ):
        """
        Cria um grid de checkboxes com colunas fixas e alinhamento consistente.
        Opcionalmente exibe um título e um separador visual.

        Returns
        -------
        tuple:
            (main_layout, checkbox_map)
        """

        if not names:
            raise ValueError("A lista de nomes de checkbox não pode estar vazia")

        main_layout = QVBoxLayout()
        if separator:
            main_layout.addWidget(WidgetFactory.create_separator())
        # 🔹 Título opcional
        if title:
            lbl = QLabel(title)
            lbl.setStyleSheet("font-weight: bold;")
            main_layout.addWidget(lbl)

        grid = QGridLayout()
        grid.setHorizontalSpacing(h_spacing)
        grid.setVerticalSpacing(v_spacing)

        checkbox_map = {}

        for index, name in enumerate(names):
            row = index // items_per_row
            col = index % items_per_row

            chk = QCheckBox(name)
            chk.setChecked(checked_by_default)

            grid.addWidget(chk, row, col)
            checkbox_map[name] = chk

        # 🔑 força todas as colunas a terem o mesmo peso
        for col in range(items_per_row):
            grid.setColumnStretch(col, 1)
        main_layout.addLayout(grid)

        if separator:
            main_layout.addWidget(WidgetFactory.create_separator())

        return main_layout, checkbox_map

    def create_separator(shape=QFrame.HLine, shadow=QFrame.Sunken, height=1, color="palette(mid)"):
        qframe = QFrame()
        qframe.setFrameShape(shape)
        qframe.setFrameShadow(shadow)
        qframe.setFixedHeight(height)
        qframe.setStyleSheet(f"background-color: {color};")
        return qframe
