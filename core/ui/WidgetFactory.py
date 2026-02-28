from qgis.core import QgsVectorLayer, QgsWkbTypes, QgsMapLayerProxyModel, QgsProject
from qgis.PyQt.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QMessageBox, QCheckBox, QTextEdit, QComboBox, QListWidget, QDoubleSpinBox, QGridLayout, QFrame
)
from qgis.PyQt.QtCore import QObject, QEvent, Qt
from qgis.PyQt.QtWidgets import QLayout, QWidget
from qgis.gui import QgsMapLayerComboBox
from ...utils.string_utils import StringUtils
from ...resources.widgets.LayerInputWidget import LayerInputWidget
from ...resources.widgets.FileSelectorWidget import FileSelectorWidget
from ...resources.widgets.BottomActionButtonsWidget import BottomActionButtonsWidget
from ...resources.widgets.MainLayout import MainLayout
from ...resources.styles.Styles import Styles
from ...resources.widgets.AppBarWidget import AppBarWidget
from ...resources.widgets.AttributeSelectorWidget import AttributeSelectorWidget
from ...resources.widgets.RadioButtonGridWidget import RadioButtonGridWidget



class WidgetFactory:
    def __init__(self, combo: QComboBox, iface):
        super().__init__(combo)
        self.combo = combo
        self.iface = iface


class WidgetFactory:
    
    
    @staticmethod
    def create_attribute_selector(
        *,
        parent=None,
        title="Atributos",
        check_all_text="Usar todos os atributos",        
        separator_top=False,
        separator_bottom=True,
    ):
        layout = QVBoxLayout()

        if separator_top:
            layout.addWidget(WidgetFactory.create_separator())

        widget = AttributeSelectorWidget(
            title=title,
            check_all_text=check_all_text,
            parent=parent
        )

        layout.addWidget(widget)

        if separator_bottom:
            layout.addWidget(WidgetFactory.create_separator())

        widget.setStyleSheet(Styles.attribute_selector())
        return layout, widget

    @staticmethod
    def create_app_bar(
        *,
        parent,
        title: str,
        on_run=None,
        on_info=None,
        on_close=None,
        show_run=False,
        show_info=False,
        show_close=True,
    ):
        app_bar = AppBarWidget(
            title=title,
            show_run=show_run,
            show_info=show_info,
            show_close=show_close,
            parent=parent,
        )

        app_bar.setStyleSheet(Styles.app_bar())

        if on_run:
            app_bar.runClicked.connect(on_run)

        if on_info:
            app_bar.infoClicked.connect(on_info)

        if on_close:
            app_bar.closeClicked.connect(on_close)

        return app_bar

    @staticmethod
    def create_bottom_action_buttons(
        *,
        parent,
        run_callback,
        close_callback,
        info_callback=None,
        separator_top=False,
        separator_bottom=False,
        tool_key=None,
        run_text="Executar",
        close_text="Fechar",
    ):
        layout = QVBoxLayout()

        if separator_top:
            layout.addWidget(WidgetFactory.create_separator())

        widget = BottomActionButtonsWidget(
            parent=parent,
            run_callback=run_callback,
            close_callback=close_callback,
            info_callback=info_callback,
            tool_key=tool_key,
            style = Styles.buttons(),
            run_text=run_text,
            close_text=close_text,
        )

        layout.addWidget(widget)
        if separator_bottom:
            layout.addWidget(WidgetFactory.create_separator())


        return layout, widget

    @staticmethod
    def create_qml_selector(
            *,
            parent,
            separator_top=False,
            separator_bottom=True,
            file_filter=StringUtils.FILTER_QGIS_STYLE,
            checkbox_text="Aplicar estilo QML",
            label_text="QML:"
    ):
        layout = QVBoxLayout()

        if separator_top:
            layout.addWidget(WidgetFactory.create_separator())

        widget = FileSelectorWidget(
            parent=parent,
            file_filter=file_filter,
            checkbox_text=checkbox_text,
            label_text=label_text,
            mode=FileSelectorWidget.MODE_OPEN
        )

        widget.setStyleSheet(Styles.file_selector())

        layout.addWidget(widget)

        if separator_bottom:
            layout.addWidget(WidgetFactory.create_separator())

        return layout, widget
    
    def create_main_layout(self, title: str="Title"):
        #ha implementar
        layout = MainLayout(self)      

        app_bar = WidgetFactory.create_app_bar(
            parent=self,
            title=title,
        )
        layout.addWidget(app_bar)

        self.setStyleSheet(Styles.main_application())
        return layout

    @staticmethod
    def create_save_file_selector(
            *,
            parent,
            separator_top=False,
            separator_bottom=True,
            file_filter=StringUtils.FILTER_VECTOR,
            checkbox_text: str = "Salvar em arquivo (caso não marcado: camada temporária)",
            label_text: str = "Salvar em:",
    ):
        layout = QVBoxLayout()

        if separator_top:
            layout.addWidget(WidgetFactory.create_separator())

        widget = FileSelectorWidget(
            parent=parent,
            file_filter=file_filter,
            checkbox_text=checkbox_text,
            label_text=label_text,
            mode=FileSelectorWidget.MODE_SAVE
        )

        widget.setStyleSheet(Styles.file_selector())

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
            keyboard_tracking=False,
            separator_top=False,
            separator_bottom=True
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
        if separator_top:
            layout.addWidget(WidgetFactory.create_separator())

        lbl = QLabel(label_text)
        layout.addWidget(lbl)

        spin = QDoubleSpinBox()
        spin.setKeyboardTracking(keyboard_tracking)
        spin.setDecimals(decimals)
        spin.setSingleStep(step)
        spin.setRange(minimum, maximum)
        spin.setValue(value)

        layout.addWidget(spin)
        if separator_bottom:
            layout.addWidget(WidgetFactory.create_separator())

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

    @staticmethod
    def create_radio_button_grid(
        *,
        items: list,
        columns: int = 3,
        title: str = None,
        checked_index: int = -1,
        tool_key: str = None,
        separator_top: bool = False,
        separator_bottom: bool = True,
        parent=None,
    ):
        """
        Cria um grid de radio buttons exclusivos (apenas um pode estar selecionado).
        
        Parameters
        ----------
        items : list
            Lista de textos para os radio buttons
        
        columns : int
            Número de colunas no grid (padrão: 3)
        
        title : str
            Título do grupo (opcional)
        
        checked_index : int
            Índice do item pré-selecionado (-1 para nenhum)
        
        tool_key : str
            Chave da ferramenta para logging
        
        separator_top : bool
            Adicionar separador no topo
        
        separator_bottom : bool
            Adicionar separador no rodapé
        
        parent : QWidget
            Widget pai
        
        Returns
        -------
        tuple:
            (layout_principal, widget_radios)
        """
        layout = QVBoxLayout()
        
        if separator_top:
            layout.addWidget(WidgetFactory.create_separator())
        
        widget = RadioButtonGridWidget(
            items=items,
            columns=columns,
            title=title,
            checked_index=checked_index,
            tool_key=tool_key,
            parent=parent
        )
        
        layout.addWidget(widget)
        
        if separator_bottom:
            layout.addWidget(WidgetFactory.create_separator())
        
        return layout, widget

    @staticmethod
    def create_separator(shape=QFrame.HLine, shadow=QFrame.Sunken, height=1, color="palette(mid)"):
        qframe = QFrame()
        qframe.setFrameShape(shape)
        qframe.setFrameShadow(shadow)
        qframe.setFixedHeight(height)
        qframe.setStyleSheet(Styles.separator())
        return qframe

