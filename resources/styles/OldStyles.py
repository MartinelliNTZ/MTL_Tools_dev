
# -*- coding: utf-8 -*-
"""
Centraliza todos os estilos QSS da aplicação About Dialog.
"""


class OldStyles:
    """Centraliza todos os estilos QSS da aplicação."""
    
    @staticmethod
    def get_main_stylesheet():
        """Retorna o stylesheet principal do dialog."""
        return """
        QDialog {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 rgba(15, 15, 15, 250), 
                stop:0.5 rgba(42, 42, 53, 250),
                stop:1 rgba(15, 15, 15, 250));
            border: 2px solid rgba(42, 90, 160, 200);
            border-radius: 8px;
        }
        
        #main_frame {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 rgba(15, 15, 15, 250), 
                stop:0.3 rgba(42, 42, 53, 250),
                stop:0.7 rgba(35, 35, 50, 250),
                stop:1 rgba(15, 15, 15, 250));
            border: 1px solid rgba(74, 127, 184, 200);
            border-radius: 0px 0px 8px 8px;
            padding: 5px;
            margin: 0px 2px 2px 2px;
        }
        
        #title_label {
            color: #e0e0e0;
            font-weight: bold;
            font-size: 20pt;
            font-family: 'Segoe UI', Arial, sans-serif;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.8);
            margin: 8px 0px;
        }
        
        #subtitle_label {
            color: #9ac4ff;
            font-size: 10pt;
            font-style: italic;
            font-family: 'Segoe UI', Arial, sans-serif;
            margin: 3px 0px;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.6);
        }
        
        #info_label {
            color: #d5e0ff;
            font-size: 8.5pt;
            font-family: 'Segoe UI', Arial, sans-serif;
            line-height: 1.6;
            background: rgba(30, 30, 50, 200);
            border-radius: 5px;
            padding: 12px;
            border-left: 4px solid #4a9eff;
        }
        
        #info_label a {
            color: #4a9eff;
            text-decoration: none;
            font-weight: bold;
        }
        
        #info_label a:hover {
            color: #6bb3ff;
            text-decoration: underline;
        }
        
        #separator_line {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 rgba(74, 158, 255, 0), 
                stop:0.5 rgba(74, 158, 255, 220),
                stop:1 rgba(74, 158, 255, 0));
            height: 2px;
            border: none;
            margin: 2px 0px;
        }
        
        QPushButton {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #4a8fff, 
                stop:1 #2d5fb0);
            color: #ffffff;
            font-weight: bold;
            font-size: 9.5pt;
            font-family: 'Segoe UI', Arial, sans-serif;
            border: 1px solid #1e4080;
            border-radius: 4px;
            padding: 7px 18px;
            min-height: 30px;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.6);
        }
        
        QPushButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #5a9fff, 
                stop:1 #3d6bc8);
            border: 1px solid #3d5fa8;
        }
        
        QPushButton:pressed {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #2d5fb0, 
                stop:1 #1e4080);
            border: 1px solid #1e4080;
        }
        
        QPushButton#btn_close {
            min-width: 110px;
        }
        
        QLabel {
            background: transparent;
        }
        """
    
    @staticmethod
    def get_title_bar_stylesheet():
        """Retorna o stylesheet da barra de título."""
        return """
            #title_bar {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(15, 15, 15, 250), 
                    stop:0.5 rgba(42, 42, 53, 250),
                    stop:1 rgba(15, 15, 15, 250));
                border: 1px solid rgba(74, 127, 184, 200);
                border-bottom: none;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                border-bottom-left-radius: 0px;
                border-bottom-right-radius: 0px;
                margin: 2px 2px 0px 2px;
            }
        """
    
    @staticmethod
    def get_title_label_stylesheet():
        """Retorna o stylesheet do label da barra de título."""
        return """
            QLabel {
                color: #4a9eff;
                font-weight: bold;
                font-size: 11pt;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        """
    
    @staticmethod
    def get_close_button_stylesheet():
        """Retorna o stylesheet do botão fechar."""
        return """
            QPushButton {
                background: transparent;
                color: #9ac4ff;
                font-weight: bold;
                font-size: 14pt;
                border: none;
                padding: 0px 8px;
                min-width: 30px;
                min-height: 30px;
            }
            QPushButton:hover {
                background: rgba(74, 158, 255, 100);
                color: #4a9eff;
                border-radius: 3px;
            }
            QPushButton:pressed {
                background: rgba(74, 158, 255, 180);
            }
        """
    
    @staticmethod
    def get_scroll_area_stylesheet():
        """Retorna o stylesheet da scroll area."""
        return """
            QScrollArea {
                background: transparent;
                border: none;
                margin: 0px;
                padding: 0px;
            }
            QScrollBar:vertical {
                background: rgba(45, 45, 45, 180);
                width: 10px;
                border-radius: 5px;
                margin: 0px 2px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: #4a9eff;
                border-radius: 5px;
                min-height: 20px;
                margin: 2px 0px;
            }
            QScrollBar::handle:vertical:hover {
                background: #6bb3ff;
            }
        """
    
    @staticmethod
    def get_logo_container_stylesheet():
        """Retorna o stylesheet do container da logo."""
        return """
            #logo_container {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(50, 80, 130, 140),
                    stop:1 rgba(30, 50, 90, 140));
                border-radius: 8px;
                padding: 10px;
                border: 2px solid #4a9eff;
            }
        """
# -*- coding: utf-8 -*-
"""
Centraliza todos os estilos QSS da aplicação About Dialog.
"""

