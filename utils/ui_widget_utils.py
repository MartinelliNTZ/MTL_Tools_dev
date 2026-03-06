# utils/ui/ui_widget_utils.py
# -*- coding: utf-8 -*-

"""
Utilitários genéricos de interface gráfica (UI) para widgets Qt
utilizados em plugins QGIS.

Centraliza comportamentos reutilizáveis de:
- seleção de camadas vetoriais (QComboBox)
- drag & drop de camadas
- listas com checkbox (QListWidget)
- sincronização com estado do projeto QGIS

Compatibilidade:
    QGIS 3.16 → 3.40
"""

from qgis.core import QgsVectorLayer, QgsWkbTypes, QgsMapLayerProxyModel, QgsProject
from qgis.PyQt.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QMessageBox, QCheckBox, QTextEdit, QComboBox, QListWidget, QDoubleSpinBox, QGridLayout, QFrame
)
from qgis.PyQt.QtCore import QObject, QEvent, Qt
from qgis.gui import QgsMapLayerComboBox
from ..utils.string_utils import StringUtils


# ==========================================================
# EVENT FILTER (uso interno)
# ==========================================================
class _LayerComboEventFilter(QObject):
    """
    Filtro de eventos para QComboBox que lista camadas vetoriais.

    Uso interno do UiWidgetUtils.
    """

    def __init__(self, combo: QComboBox, iface):
        super().__init__(combo)
        self.combo = combo
        self.iface = iface

    def eventFilter(self, obj, event):

        # Atualiza lista ao clicar no combo
        if event.type() == QEvent.MouseButtonPress:
            OldUiWidgetUtils.populate_vector_layers(self.combo)

        # DRAG ENTER / MOVE → só aceita se for camada vetorial
        if event.type() in (QEvent.DragEnter, QEvent.DragMove):
            layer = self.iface.activeLayer()
            if isinstance(layer, QgsVectorLayer):
                event.acceptProposedAction()
                return True
            else:
                event.ignore()
                return True

        # DROP → só aplica se for vetorial
        if event.type() == QEvent.Drop:
            layer = self.iface.activeLayer()

            if isinstance(layer, QgsVectorLayer):
                idx = self.combo.findData(layer.id())
                if idx != -1:
                    self.combo.setCurrentIndex(idx)
                event.acceptProposedAction()
            else:
                event.ignore()

            return True

        return False



# ==========================================================
# UI WIDGET UTILS
# ==========================================================
class OldUiWidgetUtils:
    """
DECREPATED: Esta classe contém métodos utilitários para criação de widgets UI em plugins QGIS.
NAO USAR MAIS
USE WIDGETFACTORY
    """
    @staticmethod
    def create_attribute_selector(
        *,
        title="Atributos",
        check_all_text="Usar todos os atributos",
        select_text="✔ Selecionar Todos",
        unselect_text="✖ Remover Seleção",
        invert_text="⇄ Inverter Seleção",
        separator_top=True,
        separator_bottom=True
    ):
        """
        Cria um bloco UI padronizado para seleção de atributos.

        Componentes:
        - Checkbox "Usar todos os atributos"
        - QListWidget com checkboxes
        - Botões Selecionar / Desselecionar / Inverter

        Returns
        -------
        tuple:
            (layout, chk_all, list_widget, btn_select, btn_unselect, btn_invert)
        """

        main_layout = QVBoxLayout()

        if separator_top:
            main_layout.addWidget(OldUiWidgetUtils.create_separator())

        if title:
            main_layout.addWidget(QLabel(title))

        chk_all = QCheckBox(check_all_text)
        main_layout.addWidget(chk_all)

        list_widget = QListWidget()
        list_widget.setSelectionMode(QListWidget.ExtendedSelection)
        main_layout.addWidget(list_widget)

        btn_layout = QHBoxLayout()

        btn_select = QPushButton(select_text)
        btn_unselect = QPushButton(unselect_text)
        btn_invert = QPushButton(invert_text)

        btn_layout.addWidget(btn_select)
        btn_layout.addWidget(btn_unselect)
        btn_layout.addWidget(btn_invert)
        btn_layout.addStretch()

        main_layout.addLayout(btn_layout)

        if separator_bottom:
            main_layout.addWidget(OldUiWidgetUtils.create_separator())

        # =========================
        # BINDINGS
        # =========================
        chk_all.toggled.connect(list_widget.setDisabled)

        btn_select.clicked.connect(
            lambda: OldUiWidgetUtils.set_checked_state(
                list_widget, Qt.Checked
            )
        )

        btn_unselect.clicked.connect(
            lambda: OldUiWidgetUtils.set_checked_state(
                list_widget, Qt.Unchecked
            )
        )

        def invert_selection():
            for i in range(list_widget.count()):
                item = list_widget.item(i)
                item.setCheckState(
                    Qt.Unchecked
                    if item.checkState() == Qt.Checked
                    else Qt.Checked
                )

        btn_invert.clicked.connect(invert_selection)

        return (
            main_layout,
            chk_all,
            list_widget,
            btn_select,
            btn_unselect,
            btn_invert
        )

    @staticmethod
    def enable_layer_drag_drop(combo: QComboBox, iface):
        """
        Habilita drag & drop de camadas vetoriais do painel de camadas
        para o QComboBox.
        """
        combo.setAcceptDrops(True)

        filter_obj = _LayerComboEventFilter(combo, iface)
        combo.installEventFilter(filter_obj)

        # Mantém referência para evitar GC (crash clássico)
        combo._layer_event_filter = filter_obj
        # ------------------------------------------------------------------------------------------------------------
    
    @staticmethod
    def populate_vector_layers(combo: QComboBox, keep_current=True):
        """
        Preenche um QComboBox com todas as camadas vetoriais do projeto.

        Parameters
        ----------
        combo : QComboBox
            ComboBox a ser preenchido.
        keep_current : bool
            Mantém a seleção atual, se possível.
        """
        current = combo.currentData() if keep_current else None

        combo.blockSignals(True)
        combo.clear()

        for lyr in QgsProject.instance().mapLayers().values():
            if isinstance(lyr, QgsVectorLayer):
                combo.addItem(lyr.name(), lyr.id())

        if current:
            idx = combo.findData(current)
            if idx != -1:
                combo.setCurrentIndex(idx)

        combo.blockSignals(False)

    @staticmethod
    def set_active_layer(combo: QComboBox, iface):
        """
        Define a camada ativa do QGIS como selecionada no combo.
        """
        layer = iface.activeLayer()
        if isinstance(layer, QgsVectorLayer):
            idx = combo.findData(layer.id())
            if idx != -1:
                combo.setCurrentIndex(idx)
    
    @staticmethod
    def create_layer_input(
        label_text,
        filters,
        *,
        allow_empty=True,
        enable_selected_checkbox=True, separtator_top=False, separtator_bottom=True
    ):
        """
        Cria um bloco UI contendo:
        - QLabel
        - QgsMapLayerProxyModel.AllLayers        # Todas as camadas (vetor + raster + mesh + plugin)
        - QgsMapLayerProxyModel.VectorLayer     # Todas as camadas vetoriais (ponto, linha, polígono)
        - QgsMapLayerProxyModel.RasterLayer     # Apenas camadas raster
        - QgsMapLayerProxyModel.PointLayer      # Apenas camadas vetoriais de ponto
        - QgsMapLayerProxyModel.LineLayer       # Apenas camadas vetoriais de linha
        - QgsMapLayerProxyModel.PolygonLayer    # Apenas camadas vetoriais de polígono
        - QgsMapLayerProxyModel.MeshLayer       # Camadas mesh (ex: modelos hidrodinâmicos)
        - QgsMapLayerProxyModel.PluginLayer     # Camadas fornecidas por plugins
        - QgsMapLayerProxyModel.AnnotationLayer # Camadas de anotação

        - Checkbox 'Somente feições selecionadas' (opcional)

        enable_selected_checkbox : bool
            Cria checkbox de feições selecionadas (somente vetores)

        Returns
        -------
        tuple:
            (layout, combo, checkbox | None)
        """

        layout = QVBoxLayout()
        if separtator_top:          
            layout.addWidget(OldUiWidgetUtils.create_separator())

        # Label
        lbl = QLabel(label_text)
        layout.addWidget(lbl)

        # Combo de camadas
        combo = QgsMapLayerComboBox()
        combo.setAllowEmptyLayer(allow_empty)

        # Normaliza filtros
        if isinstance(filters, (list, tuple, set)):
            final_filter = 0
            for f in filters:
                final_filter |= f
        else:
            final_filter = filters

        combo.setFilters(final_filter)
        layout.addWidget(combo)

        chk = None

        if enable_selected_checkbox:
            chk = QCheckBox("Somente feições selecionadas")
            chk.setEnabled(False)
            layout.addWidget(chk)

            state = {"layer": None}

            def get_current_layer():
                return combo.currentLayer()

            def disconnect_old():
                old = state["layer"]
                if isinstance(old, QgsVectorLayer):
                    try:
                        old.selectionChanged.disconnect(update_state)
                    except Exception:
                        pass

            def connect_new(layer):
                if isinstance(layer, QgsVectorLayer):
                    layer.selectionChanged.connect(update_state)

            def update_state():
                layer = get_current_layer()

                if not isinstance(layer, QgsVectorLayer):
                    chk.setChecked(False)
                    chk.setEnabled(False)
                    return

                selected = layer.selectedFeatureCount()
                chk.setEnabled(selected > 0)
                if selected == 0:
                    chk.setChecked(False)

            def on_layer_changed(*args):
                disconnect_old()
                layer = get_current_layer()
                state["layer"] = layer
                connect_new(layer)
                update_state()

            combo.layerChanged.connect(on_layer_changed)
            on_layer_changed()
        if separtator_bottom:          
            layout.addWidget(OldUiWidgetUtils.create_separator())
        return layout, combo, chk
    
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
        separator_top=False,
        separator_bottom=True,
        separator=None,
    ):
        """
        Cria um grid de checkboxes com colunas fixas e alinhamento consistente.
        Opcionalmente exibe um título e separadores visuais (topo/rodapé).

        Returns
        -------
        tuple:
            (main_layout, checkbox_map)
        """

        # compatibilidade: separator (bool) controla topo+rodapé quando fornecido
        if separator is not None:
            separator_top = separator
            separator_bottom = separator

        if not names:
            raise ValueError("A lista de nomes de checkbox não pode estar vazia")

        main_layout = QVBoxLayout()
        if separator_top:
            main_layout.addWidget(OldUiWidgetUtils.create_separator())
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

        if separator_bottom:
            main_layout.addWidget(OldUiWidgetUtils.create_separator())

        return main_layout, checkbox_map
    
    def create_separator(shape=QFrame.HLine, shadow=QFrame.Sunken, height=1, color="palette(mid)"):
            qframe = QFrame()
            qframe.setFrameShape(shape)
            qframe.setFrameShadow(shadow)
            qframe.setFixedHeight(height)
            qframe.setStyleSheet(f"background-color: {color};")
            return qframe
        
    @staticmethod
    def create_info_button(callback):
        info_layout = QHBoxLayout()
        info_layout.addStretch()

        btn = QPushButton("ℹ️")
        btn.setFixedWidth(30)
        btn.setFixedHeight(30)
        btn.clicked.connect(callback)
        info_layout.addWidget(btn) 
        
        return info_layout, btn  
   
    @staticmethod
    def create_run_close_buttons(run_callback, close_callback, info_callback=None,
                                 run_text="Executar", close_text="Fechar", height=22
                                 ):
        layout = QHBoxLayout()
        layout.addStretch()

        btn_run = QPushButton(run_text)
        btn_run.setFixedHeight(height)
        btn_run.clicked.connect(run_callback)

        btn_close = QPushButton(close_text)
        btn_close.setFixedHeight(height)
        btn_close.clicked.connect(close_callback)

        layout.addWidget(btn_run)
        layout.addWidget(btn_close)
        
        if info_callback:
            btn_info = QPushButton("ℹ️")
            btn_info.setFixedWidth(height)
            btn_info.setFixedHeight(height)
            btn_info.clicked.connect(info_callback)
            layout.addWidget(btn_info)
        return layout

    @staticmethod
    def create_qml_selector(
        parent,
        checkbox_text: str = "Aplicar estilo (QML) ao resultado",
        label_text: str = "QML:",
        filters: str = StringUtils.FILTER_QGIS_STYLE, separtator_top=False, separtator_bottom=True
    ):
        """
        Cria layout completo com:
        - Linha 1: QCheckBox (aplicar estilo)
        - Linha 2: Label + QLineEdit + Botão '...'
        - Binding automático checkbox → enable/disable lineedit e botão

        Returns
        -------
        tuple(QVBoxLayout, QCheckBox, QLineEdit)
        """

        main_layout = QVBoxLayout()
        if separtator_top:          
            main_layout.addWidget(OldUiWidgetUtils.create_separator())

        # Linha 1 — Checkbox
        chk_apply = QCheckBox(checkbox_text)
        main_layout.addWidget(chk_apply)

        # Linha 2 — Seletor de QML
        file_layout = QHBoxLayout()

        file_layout.addWidget(QLabel(label_text))

        txt_qml = QLineEdit()
        txt_qml.setEnabled(False)
        file_layout.addWidget(txt_qml)

        btn_qml = QPushButton("...")
        btn_qml.setEnabled(False)
        btn_qml.clicked.connect(
            lambda: parent.select_file(txt_qml, filters)
        )
        file_layout.addWidget(btn_qml)

        main_layout.addLayout(file_layout)

        # Bind checkbox → widgets
        OldUiWidgetUtils._bind_checkbox_enable_widget(chk_apply, txt_qml)
        OldUiWidgetUtils._bind_checkbox_enable_widget(chk_apply, btn_qml)
        if separtator_bottom:          
            main_layout.addWidget(OldUiWidgetUtils.create_separator())

        return main_layout, chk_apply, txt_qml
    
    @staticmethod
    def create_save_file_selector(
        parent,
        checkbox_text: str = "Salvar em arquivo (caso não marcado: camada temporária)",
        label_text: str = "Salvar em (arquivo):",
        filters: str = StringUtils.FILTER_VECTOR , separtator_top=True, separtator_bottom=True
    ):
        """
        Cria layout completo com:
        - Linha 1: QCheckBox (salvar em arquivo)
        - Linha 2: Label + QLineEdit + Botão '...'
        - Binding automático checkbox → enable/disable lineedit e botão

        Returns
        -------
        tuple(QVBoxLayout, QCheckBox, QLineEdit)
        """

        main_layout = QVBoxLayout()
        if separtator_top:          
            main_layout.addWidget(OldUiWidgetUtils.create_separator())

        # Linha 1 — Checkbox
        chk_save = QCheckBox(checkbox_text)
        main_layout.addWidget(chk_save)

        # Linha 2 — Seletor de arquivo
        file_layout = QHBoxLayout()

        file_layout.addWidget(QLabel(label_text))

        txt_output = QLineEdit()
        txt_output.setEnabled(False)
        file_layout.addWidget(txt_output)

        btn_file = QPushButton("...")
        btn_file.setEnabled(False)
        btn_file.clicked.connect(
            lambda: parent.select_file_to_save(txt_output, filters)
        )
        file_layout.addWidget(btn_file)

        main_layout.addLayout(file_layout)

        # Bind checkbox → widgets
        OldUiWidgetUtils._bind_checkbox_enable_widget(chk_save, txt_output)
        OldUiWidgetUtils._bind_checkbox_enable_widget(chk_save, btn_file)
        if separtator_bottom:          
            main_layout.addWidget(OldUiWidgetUtils.create_separator())

        return main_layout, chk_save, txt_output

    @staticmethod
    def _escape_html( text: str) -> str:
        return (
            text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
        )

    @staticmethod
    def set_checked_state(
        list_widget: QListWidget,
        state: Qt.CheckState
    ):
        """
        Define o estado de checkbox dos itens de um QListWidget.

        Comportamento:
        - Se houver itens selecionados → aplica apenas neles
        - Caso contrário → aplica a todos os itens

        Parameters
        ----------
        list_widget : QListWidget
            Lista com itens checkáveis.
        state : Qt.CheckState
            Qt.Checked ou Qt.Unchecked
        """
        selected = list_widget.selectedItems()

        items = selected if selected else [
            list_widget.item(i)
            for i in range(list_widget.count())
        ]

        for item in items:
            item.setCheckState(state)
    
    @staticmethod
    def _bind_checkbox_enable_widget(chk: QCheckBox, widget):
        """
        Habilita/desabilita um widgets com base no estado do checkbox.
        """
        def _update_state():
            widget.setEnabled(chk.isChecked())

        chk.stateChanged.connect(_update_state)
        _update_state()  # estado inicial


