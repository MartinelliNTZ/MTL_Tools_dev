# -*- coding: utf-8 -*-
"""
Botão simples que ocupa toda a tela.

Características:
- Widget QPushButton com SizePolicy Expanding
- Ocupa espaço disponível horizontalmente e verticalmente
- Padronizado via WidgetFactory

Uso:
    widget = FullScreenButtonWidget("Clique em mim")
    widget.clicked.connect(callback)
"""

from qgis.PyQt.QtWidgets import QPushButton, QSizePolicy


class FullScreenButtonWidget(QPushButton):
    """
    Botão simples que ocupa toda a tela disponível.
    
    Características:
    - Expande para preencher espaço horizontal e vertical
    - Simplificado e reutilizável
    """
    
    def __init__(self, text: str = "Botão", parent=None):
        """
        Inicializa botão full-screen.
        
        Parameters:
            text: Texto exibido no botão
            parent: Widget pai
        """
        super().__init__(text, parent)
        
        # Configurar política de tamanho para expandir
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
