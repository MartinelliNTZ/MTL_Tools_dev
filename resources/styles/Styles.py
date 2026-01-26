# -*- coding: utf-8 -*-
"""
Centraliza o tema visual do plugin.
Responsável apenas por DEFINIR estilos, não por aplicar lógica.
"""


class Styles:
    # ==========================================================
    # CORES BASE (TEMA)
    # ==========================================================

    COLOR_PRIMARY = "#a6784f"
    COLOR_PRIMARY_LIGHT = "#c1936b"
    COLOR_PRIMARY_DARK = "#6b4a2f"

    COLOR_BACKGROUND_MAIN = "rgba(16, 14, 12, 255)"
    COLOR_BACKGROUND_PANEL = "rgba(34, 30, 26, 255)"
    COLOR_BACKGROUND_SOFT = "rgba(26, 22, 20, 220)"

    COLOR_TEXT_PRIMARY = "#ece6df"
    COLOR_TEXT_SECONDARY = "#d2bca6"

    COLOR_BORDER = "#a6784f"


    # ==========================================================
    # FONTES
    # ==========================================================

    FONT_FAMILY_DEFAULT = "'Segoe UI', Arial, sans-serif"
    FONT_SIZE_TITLE = "20pt"
    FONT_SIZE_NORMAL = "9.0pt"
    FONT_SIZE_SMALL = "8.0pt"

    # ==========================================================
    # ESTILOS GERAIS (APLICAÇÃO INTEIRA)
    # ==========================================================

    @staticmethod
    def main_application():
        """
        Estilo base aplicado no dialog/janela principal.
        """
        return f"""
        #main_container {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 {Styles.COLOR_BACKGROUND_MAIN},
                stop:0.5 {Styles.COLOR_BACKGROUND_PANEL},
                stop:1 {Styles.COLOR_BACKGROUND_MAIN});
            border: 3px solid {Styles.COLOR_BORDER};
            border-radius: 8px;
        }}

        QLabel {{
            color: {Styles.COLOR_TEXT_PRIMARY};
            font-family: {Styles.FONT_FAMILY_DEFAULT};
            background: transparent;
        }}
        QCheckBox {{
            color: {Styles.COLOR_TEXT_PRIMARY};
            font-family: {Styles.FONT_FAMILY_DEFAULT};
            font-size: {Styles.FONT_SIZE_NORMAL};
            spacing: 6px;
            background: transparent;
        }}

        QCheckBox::indicator {{
            width: 16px;
            height: 16px;
            border-radius: 3px;
            border: 1px solid {Styles.COLOR_BORDER};
            background: transparent;
        }}

        QCheckBox::indicator:unchecked {{
            background: {Styles.COLOR_BACKGROUND_PANEL};
        }}

        QCheckBox::indicator:unchecked:hover {{
            border: 1px solid {Styles.COLOR_PRIMARY_LIGHT};
        }}

        QCheckBox::indicator:checked {{
            background: {Styles.COLOR_PRIMARY};
            border: 1px solid {Styles.COLOR_PRIMARY_DARK};
        }}

        QCheckBox::indicator:checked:hover {{
            background: {Styles.COLOR_PRIMARY_LIGHT};
        }}

        QCheckBox::indicator:disabled {{
            background: {Styles.COLOR_BACKGROUND_SOFT};
            border: 1px solid {Styles.COLOR_BORDER};
        }}

        QCheckBox:disabled {{
            color: {Styles.COLOR_TEXT_SECONDARY};
        }}

        QCheckBox::indicator:checked:disabled {{
            background: {Styles.COLOR_PRIMARY_DARK};
        }}
        
        QgsMapLayerComboBox {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {Styles.COLOR_PRIMARY_LIGHT},
                stop:1 {Styles.COLOR_PRIMARY_DARK});
            color: {Styles.COLOR_TEXT_PRIMARY};
            font-family: {Styles.FONT_FAMILY_DEFAULT};
            font-size: {Styles.FONT_SIZE_NORMAL};
            border: 1px solid {Styles.COLOR_BORDER};
            border-radius: 6px;
            padding: 4px 8px;
        }}

        QgsMapLayerComboBox:hover {{
            border: 1px solid {Styles.COLOR_PRIMARY_LIGHT};
        }}

        QgsMapLayerComboBox:focus {{
            border: 1px solid {Styles.COLOR_PRIMARY};
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {Styles.COLOR_PRIMARY},
                stop:1 {Styles.COLOR_PRIMARY_DARK});
        }}

        QgsMapLayerComboBox:disabled {{
            background: {Styles.COLOR_BACKGROUND_SOFT};
            color: {Styles.COLOR_TEXT_SECONDARY};
            border: 1px solid {Styles.COLOR_BORDER};
        }}

        
        QDoubleSpinBox {{
            background: {Styles.COLOR_BACKGROUND_PANEL};
            color: {Styles.COLOR_TEXT_PRIMARY};
            font-family: {Styles.FONT_FAMILY_DEFAULT};
            font-size: {Styles.FONT_SIZE_NORMAL};
            border: 1px solid {Styles.COLOR_BORDER};
            border-radius: 6px;
            padding-right: 22px; /* espaço para os botões */
        }}

        QDoubleSpinBox:hover {{
            border: 1px solid {Styles.COLOR_PRIMARY_LIGHT};
        }}

        QDoubleSpinBox:focus {{
            border: 1px solid {Styles.COLOR_PRIMARY};
        }}

        QDoubleSpinBox:disabled {{
            background: {Styles.COLOR_BACKGROUND_SOFT};
            color: {Styles.COLOR_TEXT_SECONDARY};
        }}

        /* ---------- Botões up / down ---------- */


        QDoubleSpinBox::up-button,
        QDoubleSpinBox::down-button {{
            width: 16px;
            border-left: 1px solid {Styles.COLOR_BORDER};
            background: {Styles.COLOR_PRIMARY};
        }}

        QDoubleSpinBox::up-button:hover,
        QDoubleSpinBox::down-button:hover {{
            background: {Styles.COLOR_PRIMARY_LIGHT};
        }}

        QDoubleSpinBox::up-button:pressed,
        QDoubleSpinBox::down-button:pressed {{
            background: {Styles.COLOR_PRIMARY_DARK};
        }}
        
        """
    @staticmethod
    def app_bar():
        return f"""
        #app_bar {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {Styles.COLOR_PRIMARY_DARK},
                stop:1 {Styles.COLOR_PRIMARY});
            border-bottom: 1px solid {Styles.COLOR_BORDER};
            border-radius: 8px;
            min-height: 35px;
        }}

        #app_bar_title {{
            color: {Styles.COLOR_TEXT_PRIMARY};
            font-size: 10.5pt;
            font-weight: bold;
            font-family: {Styles.FONT_FAMILY_DEFAULT};
        }}

        QPushButton#app_bar_btn_run {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {Styles.COLOR_PRIMARY},
                stop:1 {Styles.COLOR_PRIMARY_LIGHT});
            color: #ffffff;
            border: 1px solid {Styles.COLOR_PRIMARY_DARK};
            border-radius: 4px;
            padding: 4px 14px;
            font-weight: bold;
            font-size: {Styles.FONT_SIZE_SMALL};
        }}

        QPushButton#app_bar_btn_run:hover {{
            background: {Styles.COLOR_PRIMARY_LIGHT};
        }}

        QPushButton#app_bar_btn_info {{
            background: rgba(255, 255, 255, 20);
            color: {Styles.COLOR_TEXT_SECONDARY};
            border: 1px solid {Styles.COLOR_BORDER};
            border-radius: 4px;
            padding: 4px 12px;
            font-size: {Styles.FONT_SIZE_SMALL};
        }}

        QPushButton#app_bar_btn_info:hover {{
            background: rgba(255, 255, 255, 40);
        }}

        QPushButton#app_bar_btn_close {{
            background: transparent;
            color: {Styles.COLOR_TEXT_SECONDARY};
            font-size: 14pt;
            border: none;
            padding: 0px 8px;
        }}

        QPushButton#app_bar_btn_close:hover {{
            background: rgba(166, 120, 79, 120);
            color: #ffffff;
            border-radius: 3px;
        }}
        """

    # ==========================================================
    # BOTÕES
    # ==========================================================

    @staticmethod
    def buttons():
        return f"""
        QPushButton {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {Styles.COLOR_PRIMARY},
                stop:1 {Styles.COLOR_PRIMARY_DARK});
            color: #ffffff;
            font-weight: bold;
            font-size: {Styles.FONT_SIZE_NORMAL};
            font-family: {Styles.FONT_FAMILY_DEFAULT};
            border: 1px solid {Styles.COLOR_PRIMARY_DARK};
            border-radius: 9px;            
            
        }}

        QPushButton:hover {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {Styles.COLOR_PRIMARY_LIGHT},
                stop:1 {Styles.COLOR_PRIMARY});
        }}

        QPushButton:pressed {{
            background: {Styles.COLOR_PRIMARY_DARK};
        }}
        """

    # ==========================================================
    # CONTAINERS / PAINÉIS
    # ==========================================================

    @staticmethod
    def panel():
        """
        Para widgets container (MainLayout, frames, cards, etc.)
        """
        return f"""
        QFrame {{
            background: {Styles.COLOR_BACKGROUND_SOFT};
            border-radius: 6px;
            padding: 8px;
        }}
        """
    
    @staticmethod
    def file_selector():
        return f"""
        QLineEdit {{
            background: {Styles.COLOR_BACKGROUND_PANEL};
            color: {Styles.COLOR_TEXT_PRIMARY};
            font-family: {Styles.FONT_FAMILY_DEFAULT};
            font-size: {Styles.FONT_SIZE_NORMAL};
            border: 1px solid {Styles.COLOR_BORDER};
            border-radius: 4px;
            padding: 4px 8px;
        }}

        QLineEdit:disabled {{
            background: {Styles.COLOR_BACKGROUND_SOFT};
            color: {Styles.COLOR_TEXT_SECONDARY};
        }}

        QPushButton {{
            background: {Styles.COLOR_PRIMARY};
            color: #ffffff;
            font-weight: bold;
            font-size: {Styles.FONT_SIZE_NORMAL};
            font-family: {Styles.FONT_FAMILY_DEFAULT};           
            border-radius: 4px;
            min-width: 20px;
            min-height: 20px;
        }}

        QPushButton:hover {{
            background: {Styles.COLOR_PRIMARY_LIGHT};
        }}

        QPushButton:pressed {{
            background: {Styles.COLOR_PRIMARY_DARK};
        }}
        
        QPushButton:disabled {{
            background: {Styles.COLOR_BACKGROUND_SOFT};
            color: {Styles.COLOR_TEXT_SECONDARY};
        }}
        """
    # ==========================================================
    # SEPARADORES
    # ==========================================================

    @staticmethod
    def separator():
        return f"""
        QFrame {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {Styles.COLOR_BACKGROUND_PANEL}, 
                stop:0.5 {Styles.COLOR_PRIMARY},
                stop:1 {Styles.COLOR_BACKGROUND_PANEL});
            height: 3px;
            border: none;
            margin: 4px 0px;
        }}
        """


    @staticmethod
    def attribute_selector():
        """
        Estilo exclusivo para AttributeSelectorWidget
        """
        return f"""
        /* =========================
        TÍTULO
        ========================= */
        QLabel {{
            color: {Styles.COLOR_TEXT_PRIMARY};
            font-family: {Styles.FONT_FAMILY_DEFAULT};
            font-size: {Styles.FONT_SIZE_NORMAL};
            font-weight: bold;
            background: transparent;
        }}

        /* =========================
        CHECKBOX "USAR TODOS"
        ========================= */
        QCheckBox {{
            color: {Styles.COLOR_TEXT_PRIMARY};
            font-family: {Styles.FONT_FAMILY_DEFAULT};
            font-size: {Styles.FONT_SIZE_NORMAL};
            spacing: 6px;
            background: transparent;
        }}

        QCheckBox::indicator {{
            width: 16px;
            height: 16px;
            border-radius: 3px;
            border: 1px solid {Styles.COLOR_BORDER};
            background: {Styles.COLOR_BACKGROUND_PANEL};
        }}

        QCheckBox::indicator:checked {{
            background: {Styles.COLOR_PRIMARY};
            border: 1px solid {Styles.COLOR_PRIMARY_DARK};
        }}

        QCheckBox::indicator:checked:hover {{
            background: {Styles.COLOR_PRIMARY_LIGHT};
        }}

        QCheckBox:disabled {{
            color: {Styles.COLOR_TEXT_SECONDARY};
        }}

        /* =========================
        LISTA DE ATRIBUTOS
        ========================= */
        QListWidget {{
            background: {Styles.COLOR_BACKGROUND_PANEL};
            color: {Styles.COLOR_TEXT_PRIMARY};
            font-family: {Styles.FONT_FAMILY_DEFAULT};
            font-size: {Styles.FONT_SIZE_NORMAL};
            border: 1px solid {Styles.COLOR_BORDER};
            border-radius: 6px;
            padding: 4px;
            outline: none;
        }}

        QListWidget:disabled {{
            background: {Styles.COLOR_BACKGROUND_SOFT};
            color: {Styles.COLOR_TEXT_SECONDARY};
        }}

        QListWidget::item {{
            padding: 4px 6px;
            border-radius: 3px;
        }}

        QListWidget::item:selected {{
            background: rgba(166, 120, 79, 120);
            color: {Styles.COLOR_TEXT_PRIMARY};
        }}

        QListWidget::item:hover {{
            background: rgba(166, 120, 79, 60);
        }}

        /* =========================
        CHECKBOX DOS ITENS
        ========================= */
        QListWidget::indicator {{
            width: 14px;
            height: 14px;
        }}

        QListWidget::indicator:unchecked {{
            border: 1px solid {Styles.COLOR_BORDER};
            background: transparent;
        }}

        QListWidget::indicator:checked {{
            background: {Styles.COLOR_PRIMARY};
            border: 1px solid {Styles.COLOR_PRIMARY_DARK};
        }}

        /* =========================
        BOTÕES (Selecionar / Remover / Inverter)
        ========================= */
        QPushButton {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {Styles.COLOR_PRIMARY},
                stop:1 {Styles.COLOR_PRIMARY_DARK});
            color: #ffffff;
            font-family: {Styles.FONT_FAMILY_DEFAULT};
            font-size: {Styles.FONT_SIZE_SMALL};
            font-weight: bold;
            border: 1px solid {Styles.COLOR_PRIMARY_DARK};
            border-radius: 6px;
            padding: 4px 10px;
            min-height: 26px;
        }}

        QPushButton:hover {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {Styles.COLOR_PRIMARY_LIGHT},
                stop:1 {Styles.COLOR_PRIMARY});
        }}

        QPushButton:pressed {{
            background: {Styles.COLOR_PRIMARY_DARK};
        }}

        QPushButton:disabled {{
            background: {Styles.COLOR_BACKGROUND_SOFT};
            color: {Styles.COLOR_TEXT_SECONDARY};
            border: 1px solid {Styles.COLOR_BORDER};
        }}
        """
