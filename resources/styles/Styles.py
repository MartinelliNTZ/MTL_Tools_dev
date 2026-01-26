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

    COLOR_BORDER = "rgba(166, 120, 79, 180)"


    # ==========================================================
    # FONTES
    # ==========================================================

    FONT_FAMILY_DEFAULT = "'Segoe UI', Arial, sans-serif"
    FONT_SIZE_TITLE = "20pt"
    FONT_SIZE_NORMAL = "9.5pt"
    FONT_SIZE_SMALL = "8.5pt"

    # ==========================================================
    # ESTILOS GERAIS (APLICAÇÃO INTEIRA)
    # ==========================================================

    @staticmethod
    def main_application():
        """
        Estilo base aplicado no dialog/janela principal.
        """
        return f"""
        QDialog {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 {Styles.COLOR_BACKGROUND_MAIN},
                stop:0.5 {Styles.COLOR_BACKGROUND_PANEL},
                stop:1 {Styles.COLOR_BACKGROUND_MAIN});
            border: 2px solid {Styles.COLOR_BORDER};
            border-radius: 8px;
        }}

        QLabel {{
            color: {Styles.COLOR_TEXT_PRIMARY};
            font-family: {Styles.FONT_FAMILY_DEFAULT};
            background: transparent;
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
            min-height: 42px;
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
            border-radius: 5px;            
            
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

    # ==========================================================
    # SEPARADORES
    # ==========================================================

    @staticmethod
    def separator():
        return f"""
        QFrame {{
            background-color: {Styles.COLOR_PRIMARY};
            max-height: 1px;
        }}
        """
