# -*- coding: utf-8 -*-
"""
Factory para criar widgets estilizados do About Dialog.
"""
import os
from qgis.PyQt.QtWidgets import (
    QLabel, QPushButton, QFrame, QHBoxLayout, QVBoxLayout, 
    QSpacerItem, QSizePolicy, QScrollArea
)
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QPixmap

from .styles import Styles


class WidgetFactory:
    """Factory para criar widgets estilizados."""
    
    @staticmethod
    def create_title_bar(close_callback):
        """Cria a barra de título customizada."""
        title_bar = QFrame()
        title_bar.setObjectName("title_bar")
        title_bar.setFixedHeight(40)
        title_bar.setStyleSheet(Styles.get_title_bar_stylesheet())
        
        layout = QHBoxLayout(title_bar)
        layout.setContentsMargins(15, 0, 15, 0)
        layout.setSpacing(0)
        
        # Título
        lbl = QLabel("Sobre o MTL Tools")
        lbl.setStyleSheet(Styles.get_title_label_stylesheet())
        layout.addWidget(lbl)
        layout.addStretch()
        
        # Botão fechar
        btn_close = QPushButton("✕")
        btn_close.setStyleSheet(Styles.get_close_button_stylesheet())
        btn_close.clicked.connect(close_callback)
        layout.addWidget(btn_close)
        
        return title_bar
    
    @staticmethod
    def create_scroll_area():
        """Cria a scroll area."""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setContentsMargins(0, 0, 0, 0)
        scroll.setMaximumHeight(515)
        scroll.setStyleSheet(Styles.get_scroll_area_stylesheet())
        return scroll
    
    @staticmethod
    def create_main_frame():
        """Cria o frame principal."""
        main_frame = QFrame()
        main_frame.setObjectName("main_frame")
        frame_layout = QVBoxLayout(main_frame)
        frame_layout.setContentsMargins(25, 25, 25, 25)
        frame_layout.setSpacing(10)
        return main_frame, frame_layout
    
    @staticmethod
    def create_logo_container():
        """Cria o container da logo."""
        container = QFrame()
        container.setObjectName("logo_container")
        container.setStyleSheet(Styles.get_logo_container_stylesheet())
        container.setMaximumHeight(170)
        
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)

        logo_path = os.path.join(
            os.path.dirname(__file__),
            "..", "resources", "icons", "mtl_agro.png"
        )

        if os.path.exists(logo_path):
            lbl_logo = QLabel()
            pixmap = QPixmap(logo_path)
            lbl_logo.setPixmap(pixmap.scaledToWidth(160, Qt.SmoothTransformation))
            lbl_logo.setAlignment(Qt.AlignCenter)
            layout.addWidget(lbl_logo)
        
        return container
    
    @staticmethod
    def create_separator():
        """Cria uma linha separadora."""
        separator = QFrame()
        separator.setObjectName("separator_line")
        separator.setFixedHeight(2)
        return separator
    
    @staticmethod
    def create_title_label(text):
        """Cria um label de título."""
        lbl = QLabel(text)
        lbl.setObjectName("title_label")
        lbl.setAlignment(Qt.AlignCenter)
        return lbl
    
    @staticmethod
    def create_subtitle_label(text):
        """Cria um label de subtítulo."""
        lbl = QLabel(text)
        lbl.setObjectName("subtitle_label")
        lbl.setAlignment(Qt.AlignCenter)
        return lbl
    
    @staticmethod
    def create_info_label(html_content):
        """Cria um label de informações."""
        lbl = QLabel(html_content)
        lbl.setObjectName("info_label")
        lbl.setTextFormat(Qt.RichText)
        lbl.setTextInteractionFlags(Qt.TextBrowserInteraction)
        lbl.setOpenExternalLinks(True)
        lbl.setAlignment(Qt.AlignCenter)
        lbl.setWordWrap(True)
        return lbl
    
    @staticmethod
    def create_button_layout():
        """Cria o layout dos botões."""
        h_btn = QHBoxLayout()
        h_btn.setSpacing(10)
        h_btn.addStretch()

        btn_close = QPushButton("Fechar")
        btn_close.setObjectName("btn_close")
        h_btn.addWidget(btn_close)
        h_btn.addStretch()
        
        return h_btn, btn_close
    
    @staticmethod
    def create_spacer():
        """Cria um spacer flexível."""
        return QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
# -*- coding: utf-8 -*-
"""
Helper para ações e eventos de widgets do About Dialog.
"""


class WidgetHelper:
    """Helper para ações e eventos de widgets."""
    
    @staticmethod
    def connect_button_close(button, callback):
        """Conecta o botão fechar a um callback."""
        button.clicked.connect(callback)
    
    @staticmethod
    def get_info_html():
        """Retorna o HTML formatado com as informações do plugin."""
        return """
            <div style="text-align: center; line-height: 1.6;">
                <p style="margin: 4px 0;">
                    <span style="color: #4a9eff; font-weight: bold;">v1.3.0</span> | 
                    <span style="color: #9ac4ff;">16/01/2026</span>
                </p>
                <hr style="border: 1px solid rgba(74, 158, 255, 120); margin: 6px 0; border-radius: 1px;">
                <p style="margin: 4px 0; font-size: 8pt;">
                    <span style="color: #c4d9ff;">MTL Agricultura e Tecnologia</span><br>
                    <span style="color: #9ac4ff;">📍 Palmas - TO - Brasil</span>
                </p>
                <hr style="border: 1px solid rgba(74, 158, 255, 120); margin: 6px 0; border-radius: 1px;">
                <p style="margin: 4px 0; font-size: 7.5pt;">
                    <a href="mailto:martinelli.matheus11@gmail.com" style="color: #4a9eff; text-decoration: none; font-weight: bold;">📧 Email</a> | 
                    <a href="https://github.com/MartinelliNTZ/mtl-tools-repo" style="color: #4a9eff; text-decoration: none; font-weight: bold;">🔗 GitHub</a>
                </p>
            </div>
        """
# -*- coding: utf-8 -*-
import os
from qgis.PyQt.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QSpacerItem, QSizePolicy, QScrollArea
)
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QPixmap
from qgis.PyQt.QtCore import QUrl

from .styles import Styles
from .widget_factory import WidgetFactory
from .widget_helper import WidgetHelper


# =====================================================
# CLASSE PRINCIPAL
# =====================================================
class AboutDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Sobre o MTL Tools")
        self.setMinimumWidth(500)
        self.setMinimumHeight(560)
        
        # Inicializar posição de arrasto
        self.drag_position = None
        
        # =====================================================
        # ESTILO FRAMELESS COM BARRA CUSTOMIZADA
        # =====================================================
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self._apply_advanced_styling()
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.setSpacing(0)

        # =====================================================
        # BARRA DE TÍTULO CUSTOMIZADA
        # =====================================================
        title_bar = WidgetFactory.create_title_bar(self.close)
        main_layout.addWidget(title_bar)

        # =====================================================
        # SCROLL AREA PARA CABER EM TELAS PEQUENAS
        # =====================================================
        scroll = WidgetFactory.create_scroll_area()

        # =====================================================
        # FRAME PRINCIPAL COM GRADIENTE
        # =====================================================
        main_frame, frame_layout = WidgetFactory.create_main_frame()

        # =====================================================
        # LOGO COM EFEITO
        # =====================================================
        logo_container = WidgetFactory.create_logo_container()
        frame_layout.addWidget(logo_container)

        # =====================================================
        # SEPARADOR VISUAL
        # =====================================================
        separator_top = WidgetFactory.create_separator()
        frame_layout.addWidget(separator_top)

        # =====================================================
        # TÍTULO ESTILIZADO
        # =====================================================
        lbl_title = WidgetFactory.create_title_label("<h1>MTL Tools</h1>")
        frame_layout.addWidget(lbl_title)

        # =====================================================
        # SUBTÍTULO COMPACTO
        # =====================================================
        lbl_subtitle = WidgetFactory.create_subtitle_label("Ferramentas Avançadas para Cartografia")
        frame_layout.addWidget(lbl_subtitle)

        # =====================================================
        # SEPARADOR VISUAL
        # =====================================================
        separator_mid = WidgetFactory.create_separator()
        frame_layout.addWidget(separator_mid)

        # =====================================================
        # INFORMAÇÕES COM FORMATAÇÃO AVANÇADA
        # =====================================================
        lbl_info = WidgetFactory.create_info_label(WidgetHelper.get_info_html())
        frame_layout.addWidget(lbl_info)

        # =====================================================
        # ESPAÇO FLEXÍVEL REDUZIDO
        # =====================================================
        spacer = WidgetFactory.create_spacer()
        frame_layout.addItem(spacer)

        # =====================================================
        # SEPARADOR VISUAL FINAL
        # =====================================================
        separator_bottom = WidgetFactory.create_separator()
        frame_layout.addWidget(separator_bottom)

        # =====================================================
        # BOTÕES COM ESTILO AVANÇADO
        # =====================================================
        btn_layout, btn_close = WidgetFactory.create_button_layout()
        WidgetHelper.connect_button_close(btn_close, self.close)
        frame_layout.addLayout(btn_layout)

        # =====================================================
        # ADICIONAR AO SCROLL
        # =====================================================
        scroll.setWidget(main_frame)
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)

    # =====================================================
    # MÉTODO DE ESTILO
    # =====================================================
    def _apply_advanced_styling(self):
        """Aplica o stylesheet avançado do dialog."""
        self.setStyleSheet(Styles.get_main_stylesheet())

    # =====================================================
    # EVENTOS DE MOUSE
    # =====================================================
    def mousePressEvent(self, event):
        """Permite arrastar a janela pela barra de título."""
        if event.y() < 40:  # Altura da barra de título
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        """Move a janela ao arrastar."""
        if self.drag_position is not None:
            self.move(event.globalPos() - self.drag_position)
            event.accept()


# =====================================================
# FUNÇÃO PÚBLICA (PADRÃO DO SEU PLUGIN)
# =====================================================
def run_about_dialog(iface):
    dlg = AboutDialog(iface.mainWindow())
    dlg.exec()

# -*- coding: utf-8 -*-
"""
Centraliza todos os estilos QSS da aplicação About Dialog.
"""


class Styles:
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


class Styles:
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
