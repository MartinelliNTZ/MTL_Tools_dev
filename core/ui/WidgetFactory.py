from qgis.PyQt.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QTextBrowser,
    QComboBox,
    QDoubleSpinBox,
    QFrame,
)
from ...resources.widgets.ImageWidget import ImageWidget
from ...utils.StringUtils import StringUtils
from ...resources.widgets.LayerInputWidget import LayerInputWidget
from ...resources.widgets.BottomActionButtonsWidget import BottomActionButtonsWidget
from ...resources.widgets.MainLayout import MainLayout
from ...resources.styles.Styles import Styles
from ...resources.widgets.AppBarWidget import AppBarWidget
from ...resources.widgets.AttributeSelectorWidget import AttributeSelectorWidget
from ...resources.widgets.RadioButtonGridWidget import RadioButtonGridWidget
from ...resources.widgets.CollapsibleParametersWidget import CollapsibleParametersWidget
from ...resources.widgets.SelectorWidget import SelectorWidget
from ...resources.widgets.InputFieldsWidget import InputFieldsWidget
from ...resources.widgets.SimpleButtonWidget import SimpleButtonWidget
from ...resources.widgets.CheckboxGridWidget import CheckboxGridWidget
from ...resources.widgets.ReadOnlyFieldWidget import ReadOnlyFieldWidget
from ...resources.widgets.DropdownSelectorWidget import DropdownSelectorWidget
from ...i18n.TranslationManager import STR


class WidgetFactory:
    def __init__(self, combo: QComboBox, iface):
        super().__init__(combo)
        self.combo = combo
        self.iface = iface

    @staticmethod
    def create_attribute_selector(
        *,
        parent=None,
        title=STR.ATTRIBUTES,
        check_all_text=STR.USE_ALL_ATTRIBUTES,
        separator_top=False,
        separator_bottom=True,
    ):
        layout = QVBoxLayout()

        if separator_top:
            layout.addWidget(WidgetFactory.create_separator())

        widget = AttributeSelectorWidget(
            title=title, check_all_text=check_all_text, parent=parent
        )

        layout.addWidget(widget)

        if separator_bottom:
            layout.addWidget(WidgetFactory.create_separator())

        widget.setStyleSheet(Styles.attribute_selector())
        return layout, widget

    @staticmethod
    def create_image_widget(
        *,
        image_path: str,
        fixed_height: int = 60,
        clickable: bool = False,
        clicked_callback=None,
        separator_top: bool = False,
        separator_bottom: bool = False,
        parent=None,
    ):
        """
        Cria um widget de logo padronizado.

        :param image_path: Caminho absoluto para a imagem.
        :param fixed_height: Altura fixa do widget (padrão 60px).
        :param clickable: Se True, o widget emite um sinal ao ser clicado.
        :param clicked_callback: Função a ser chamada quando clicado (se clickable=True).
        :param separator_top: Adiciona separador acima do widget.
        :param separator_bottom: Adiciona separador abaixo do widget.
        :param parent: Widget pai.
        :return: tuple (layout contendo o widget, instância do widget)
        """
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)  # ou use Styles.LAYOUT_V_SPACING

        if separator_top:
            layout.addWidget(WidgetFactory.create_separator())

        widget = ImageWidget(
            image_path=image_path, fixed_height=fixed_height, parent=parent
        )

        if clickable and clicked_callback:
            widget.clicked.connect(clicked_callback)

        # Opcional: aplicar estilo específico se definido em Styles
        # widget.setStyleSheet(Styles.logo_widget())

        layout.addWidget(widget)

        if separator_bottom:
            layout.addWidget(WidgetFactory.create_separator())

        return layout, widget

    @staticmethod
    def create_app_bar(
        *,
        parent,
        title: str,
        icon_path: str = None,
        on_run=None,
        on_info=None,
        on_close=None,
        show_run=False,
        show_info=False,
        show_close=True,
    ):
        app_bar = AppBarWidget(
            title=title,
            icon_path=icon_path,
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
        run_text=STR.EXECUTE,
        close_text=STR.CLOSE,
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
            style=Styles.bottom_action_buttons_widget(),
            run_text=run_text,
            close_text=close_text,
        )

        layout.addWidget(widget)
        if separator_bottom:
            layout.addWidget(WidgetFactory.create_separator())

        return layout, widget

    @staticmethod
    def create_checkbox_grid(
        options_dict,
        *,
        items_per_row=3,
        checked_by_default=False,
        title=None,
        separator_top=False,
        separator_bottom=True,
    ):
        """
        Cria um grid de checkboxes a partir de um dicionário chave→label.
        Retorna (layout, checkbox_map) para integração fácil.
        """
        layout = QVBoxLayout()
        if separator_top:
            layout.addWidget(WidgetFactory.create_separator())

        widget = CheckboxGridWidget(
            options_dict,
            items_per_row=items_per_row,
            checked_by_default=checked_by_default,
            title=title,
        )
        layout.addWidget(widget)
        widget.setStyleSheet(Styles.grid_checkboxes())

        if separator_bottom:
            layout.addWidget(WidgetFactory.create_separator())

        return layout, widget.get_checkbox_map()

    @staticmethod
    def create_qml_selector(
        *,
        parent,
        separator_top=False,
        separator_bottom=True,
        file_filter=StringUtils.FILTER_QGIS_STYLE,
        checkbox_text=STR.APPLY_QML_STYLE,
        label_text=STR.QML_LABEL,
    ):
        """Criar seletor de arquivo QML com checkbox."""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(Styles.LAYOUT_V_SPACING)

        if separator_top:
            layout.addWidget(WidgetFactory.create_separator())

        widget = SelectorWidget(
            parent=parent,
            file_filter=file_filter,
            checkbox_text=checkbox_text,
            title=label_text,
            mode=SelectorWidget.MODE_FILE,
            checkbox=True,
        )

        widget.setStyleSheet(Styles.path_selector_widget())

        layout.addWidget(widget)

        if separator_bottom:
            layout.addWidget(WidgetFactory.create_separator())

        return layout, widget

    @staticmethod
    def create_text_browser(
        *, parent=None, open_external_links: bool = True, read_only: bool = True
    ):
        """Create and configure a QTextBrowser with project defaults.

        Returns a configured QTextBrowser instance.
        """
        browser = QTextBrowser(parent)
        browser.setOpenExternalLinks(open_external_links)
        browser.setReadOnly(read_only)
        return browser

    @staticmethod
    def create_main_layout(
        self, title: str = STR.APP_NAME, enable_scroll: bool = False, icon_path: str = None
    ):
        """
        Criar layout principal com AppBar.

        O MainLayout agora encapsula o scroll internamente.

        Args:
            title: Texto do AppBar
            enable_scroll: Se True, MainLayout cria ScrollWidget internamente

        Returns:
            MainLayout (que gerencia scroll automaticamente)
        """
        layout = MainLayout(self, enable_scroll=enable_scroll)

        app_bar = WidgetFactory.create_app_bar(
            parent=self,
            title=title,
            icon_path=icon_path,
        )

        # Adicionar app_bar ao INÍCIO do _inner_layout (fora do scroll)
        layout._inner_layout.insertWidget(0, app_bar)

        self.setStyleSheet(Styles.main_application())

        return layout

    @staticmethod
    def create_save_file_selector(
        *,
        parent,
        separator_top=False,
        separator_bottom=True,
        file_filter=StringUtils.FILTER_VECTOR,
        checkbox_text: str = STR.SAVE_TO_FILE,
        label_text: str = STR.SAVE_IN,
    ):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(Styles.LAYOUT_V_SPACING)

        if separator_top:
            layout.addWidget(WidgetFactory.create_separator())

        widget = SelectorWidget(
            parent=parent,
            file_filter=file_filter,
            checkbox_text=checkbox_text,
            title=label_text,
            mode=SelectorWidget.MODE_SAVE,
            checkbox=True,
        )

        widget.setStyleSheet(Styles.path_selector_widget())

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
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)
        if separator_top:
            layout.addWidget(WidgetFactory.create_separator())

        widget = LayerInputWidget(
            label_text=label_text,
            filters=filters,
            allow_empty=allow_empty,
            enable_selected_checkbox=enable_selected_checkbox,
            parent=parent,
        )

        widget.setStyleSheet(Styles.layer_input_widget())

        layout.addWidget(widget)
        if separator_bottom:
            layout.addWidget(WidgetFactory.create_separator())

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
        separator_bottom=True,
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

        # Layout externo (vertical) para separadores em linhas diferentes
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(2)

        if separator_top:
            main_layout.addWidget(WidgetFactory.create_separator())

        # Layout interno (horizontal) para label + spin na mesma linha
        h_layout = QHBoxLayout()
        h_layout.setContentsMargins(0, 0, 0, 0)
        h_layout.setSpacing(4)

        lbl = QLabel(label_text)
        h_layout.addWidget(lbl)

        spin = QDoubleSpinBox()
        spin.setKeyboardTracking(keyboard_tracking)
        spin.setDecimals(decimals)
        spin.setSingleStep(step)
        spin.setRange(minimum, maximum)
        spin.setValue(value)
        spin.setStyleSheet(Styles.input_fields_widget())

        h_layout.addWidget(spin)

        # Adicionar h_layout ao main_layout
        main_layout.addLayout(h_layout)

        if separator_bottom:
            main_layout.addWidget(WidgetFactory.create_separator())

        return main_layout, spin

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
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)

        if separator_top:
            layout.addWidget(WidgetFactory.create_separator())

        widget = RadioButtonGridWidget(
            items=items,
            columns=columns,
            title=title,
            checked_index=checked_index,
            tool_key=tool_key,
            parent=parent,
        )

        widget.setStyleSheet(Styles.radio_button_grid_widget())

        layout.addWidget(widget)

        if separator_bottom:
            layout.addWidget(WidgetFactory.create_separator())

        return layout, widget

    @staticmethod
    def create_readonly_field(
        *,
        parent=None,
        title: str = None,
        fields: dict = None,
        num_columns: int = 1,
        copy_all_button_title: str = None,
        default_button_title: str = STR.COPY,
        tool_key: str = None,
        separator_top: bool = False,
        separator_bottom: bool = True,
    ):
        """
        Cria um bloco ReadOnlyFieldWidget.

        Parameters
        ----------
        fields : dict
            Dicionário com chaves identificadoras e valores
              { 'title': str, 'value': Any, 'value_type': str, 'titlebutton': str }
        num_columns : int
            Número de colunas para layout
        copy_all_button_title : str|None
            Texto do botão "Copiar tudo". Se None, não cria o botão.
        default_button_title : str
            Texto padrão para botões individuais
        """
        layout = QVBoxLayout()
        if separator_top:
            layout.addWidget(WidgetFactory.create_separator())
        widget = ReadOnlyFieldWidget(
            fields=fields or {},
            title=title,
            title_button_copy_all=copy_all_button_title,
            default_button_title=default_button_title,
            num_columns=num_columns,
            parent=parent,
        )
        layout.addWidget(widget)
        if separator_bottom:
            layout.addWidget(WidgetFactory.create_separator())
        return layout, widget

    @staticmethod
    def create_separator(shape=None, shadow=None, height=1, color="palette(mid)"):
        if shape is None:
            if hasattr(QFrame, "HLine"):
                shape = QFrame.HLine
            elif hasattr(QFrame, "Shape") and hasattr(QFrame.Shape, "HLine"):
                shape = QFrame.Shape.HLine
            else:
                shape = QFrame.NoFrame

        if shadow is None:
            if hasattr(QFrame, "Sunken"):
                shadow = QFrame.Sunken
            elif hasattr(QFrame, "Shadow") and hasattr(QFrame.Shadow, "Sunken"):
                shadow = QFrame.Shadow.Sunken
            else:
                shadow = QFrame.Plain

        qframe = QFrame()
        qframe.setFrameShape(shape)
        qframe.setFrameShadow(shadow)
        qframe.setFixedHeight(height)
        qframe.setStyleSheet(Styles.separator())
        return qframe

    @staticmethod
    def create_collapsible_parameters(
        *,
        parent=None,
        title: str = STR.ADVANCED_PARAMETERS,
        expanded_by_default: bool = False,
        separator_top: bool = False,
        separator_bottom: bool = True,
    ) -> tuple:
        """
        Cria um widget para parâmetros avançados com suporte a expansão/recolhimento.

        Arquitetura:
        - Widget genérico e reutilizável (pode ser usado em múltiplos plugins)
        - Suporta adicionar widgets e layouts dinamicamente
        - Animação suave na expansão/recolhimento
        - Ícone dinâmico (→ recolhido | ↓ expandido)

        Parameters
        ----------
        parent : QWidget, optional
            Widget pai

        title : str
            Texto do título exibido no header

        expanded_by_default : bool
            Se True, inicia expandido; caso contrário, recolhido

        separator_top : bool
            Adicionar separador no topo

        separator_bottom : bool
            Adicionar separador no rodapé

        Returns
        -------
        tuple:
            (layout_principal, widget_collapsible)

        Exemplo de uso:
        --------
        # Criar o widget
        adv_layout, adv_widget = WidgetFactory.create_collapsible_parameters(
            parent=self,
            title="Configurações Avançadas",
            expanded_by_default=False
        )

        # Adicionar conteúdo
        qml_layout, qml_widget = WidgetFactory.create_qml_selector(parent=self)
        adv_widget.add_content_layout(qml_layout)

        # Adicionar ao layout da janela
        main_layout.addLayout(adv_layout)
        """
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)

        if separator_top:
            layout.addWidget(WidgetFactory.create_separator())

        # Criar widget colapsável
        widget = CollapsibleParametersWidget(title=title, parent=parent)

        # Aplicar estilos
        widget.setStyleSheet(Styles.collapsible_parameters())

        # Definir estado inicial
        if expanded_by_default:
            widget.set_expanded(True)

        layout.addWidget(widget)

        if separator_bottom:
            layout.addWidget(WidgetFactory.create_separator())

        return layout, widget

    @staticmethod
    def create_path_selector(
        *,
        parent=None,
        title: str = STR.SELECT_PATH,
        file_filter: str = StringUtils.FILTER_ALL,
        mode: str = "radio",
        separator_top: bool = False,
        separator_bottom: bool = True,
    ) -> tuple:
        """Cria um widget de seleção de caminho.

        O widget pode operar nos seguintes modos:
        - "radio" (padrão): exibe rádios Pasta / Arquivos
        - "folder": somente pasta (sem rádios)
        - "files": somente arquivos (sem rádios)
        """
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)

        if separator_top:
            layout.addWidget(WidgetFactory.create_separator())

        widget = SelectorWidget(
            title=title,
            file_filter=file_filter,
            mode=mode,
            parent=parent,
        )

        widget.setStyleSheet(Styles.path_selector_widget())

        layout.addWidget(widget)

        if separator_bottom:
            layout.addWidget(WidgetFactory.create_separator())

        return layout, widget

    @staticmethod
    def create_input_fields_widget(
        *,
        fields_dict: dict,
        parent=None,
        separator_top=False,
        separator_bottom=True,
    ):
        """
        Cria widget com múltiplos campos de input baseados em dicionário.

        Parameters
        ----------
        fields_dict : dict
            Dicionário com configuração dos campos
            {
                'chave': {
                    'title': 'Rótulo',
                    'type': 'text' | 'int' | 'float',
                    'default': valor_padrão
                },
                ...
            }

        separator_top : bool
            Adicionar separador no topo

        separator_bottom : bool
            Adicionar separador no rodapé

        Returns
        -------
        tuple:
            (layout_principal, widget_input_fields)
        """
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(Styles.LAYOUT_V_SPACING)

        if separator_top:
            layout.addWidget(WidgetFactory.create_separator())

        widget = InputFieldsWidget(fields_dict, parent=parent)
        widget.setStyleSheet(Styles.input_fields_widget())
        layout.addWidget(widget)

        if separator_bottom:
            layout.addWidget(WidgetFactory.create_separator())

        return layout, widget

    @staticmethod
    def create_dropdown_selector(
        *,
        title: str,
        options_dict: dict,
        selected_key=None,
        allow_empty: bool = False,
        empty_text: str = f"{STR.SELECT}...",
        parent=None,
        separator_top: bool = False,
        separator_bottom: bool = True,
    ):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(Styles.LAYOUT_V_SPACING)

        if separator_top:
            layout.addWidget(WidgetFactory.create_separator())

        widget = DropdownSelectorWidget(
            title=title,
            options_dict=options_dict,
            selected_key=selected_key,
            allow_empty=allow_empty,
            empty_text=empty_text,
            parent=parent,
        )
        widget.setStyleSheet(Styles.dropdown_selector_widget())
        layout.addWidget(widget)

        if separator_bottom:
            layout.addWidget(WidgetFactory.create_separator())

        return layout, widget

    @staticmethod
    def create_simple_button(
        *,
        text: str = STR.BUTTON,
        parent=None,
        separator_top=False,
        separator_bottom=False,
        spacing: int = Styles.LAYOUT_V_SPACING * 10,
    ):
        """
        Cria botão simples que ocupa espaço disponível.

        Parameters
        ----------
        text : str
            Texto exibido no botão

        separator_top : bool
            Adicionar separador no topo

        separator_bottom : bool
            Adicionar separador no rodapé

        Returns
        -------
        tuple:
            (layout_principal, botao)
        """
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(Styles.LAYOUT_V_SPACING)

        if separator_top:
            layout.addWidget(WidgetFactory.create_separator())

        widget = SimpleButtonWidget(text, parent=parent)
        widget.setStyleSheet(Styles.simple_button_widget())
        layout.addWidget(widget)
        layout.addSpacing(spacing)
        if separator_bottom:
            layout.addWidget(WidgetFactory.create_separator())

        return layout, widget

    @staticmethod
    def create_label(
        *,
        text: str = "",
        bold: bool = False,
        word_wrap: bool = False,
        parent=None,
        text_format=None,
        text_interaction_flags=None,
        open_external_links=None,
        alignment=None,
    ) -> QLabel:
        """
        Cria um QLabel configurado e estilizado.

        Parameters
        ----------
        text : str
            Texto do label

        bold : bool
            Se True, aplica negrito

        word_wrap : bool
            Se True, ativa quebra de linha

        parent : QWidget
            Widget pai

        text_format : Qt.TextFormat | None
            Define o formato do texto (p.ex., Qt.RichText)

        text_interaction_flags : Qt.TextInteractionFlags | None
            Flags de interação de texto para links

        open_external_links : bool | None
            Se True, permite links externos

        alignment : Qt.Alignment | None
            Alinhamento do label

        Returns
        -------
        QLabel
            Label configurado e estilizado
        """
        label = QLabel(text, parent)
        label.setStyleSheet(Styles.label())
        label.setWordWrap(word_wrap)

        if bold:
            font = label.font()
            font.setBold(True)
            label.setFont(font)

        if text_format is not None:
            label.setTextFormat(text_format)

        if text_interaction_flags is not None:
            label.setTextInteractionFlags(text_interaction_flags)

        if open_external_links is not None:
            label.setOpenExternalLinks(open_external_links)

        if alignment is not None:
            label.setAlignment(alignment)

        return label
