# -*- coding: utf-8 -*-
"""
Widget autossuficiente para seleção de pastas/arquivos.

Arquitetura ENCAPSULADA:
- Radios INTERNOS para alternar Pasta ↔ Arquivos
- SEMPRE retorna lista via get_paths()
- Validação automática de input (pasta vs arquivo)
- Plugin só chama: get_paths() e processa a lista

Uso:
    widget = PathSelectorWidget(title="Selecione")
    paths = widget.get_paths()  # ["pasta"] ou ["arq.txt"] ou ["a.txt", "b.txt"] ou []
"""

import os
from pathlib import Path
from qgis.PyQt.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QLineEdit, QPushButton, QFileDialog, QRadioButton, QButtonGroup
)
from qgis.PyQt.QtCore import Qt, pyqtSignal


class PathSelectorWidget(QWidget):
    """Widget completo e autossuficiente para seleção de paths.

    Características:
    - Pode operar em 3 modos:
      * radio (Pasta + Arquivos) [padrão]
      * folder (apenas pasta)
      * files (apenas arquivos)
    - Sempre retorna lista via get_paths()
    - Valida input automático (pasta vs arquivo)
    - Plugin nunca precisa saber detalhes internos

    Sinais:
        pathsChanged: emitido quando a lista de paths muda
    """

    # Modos internos (não expostos)
    MODE_RADIO = "radio"
    MODE_FOLDER = "folder"
    MODE_FILE = "file"
    MODE_FILES = "files"

    pathsChanged = pyqtSignal(list)  # Sempre emite lista

    def __init__(
        self,
        *,
        title: str = "Selecionar",
        file_filter: str = "Todos (*.*)",
        mode: str = MODE_RADIO,
        parent=None
    ):
        """Inicializa widget com tudo encapsulado.

        Parameters:
            title: Rótulo do campo input
            file_filter: Filtro de arquivos para dialog (ex: "MRK (*.mrk)")
            mode: "radio" | "folder" | "files"
            parent: Widget pai
        """
        super().__init__(parent)

        self._title = title
        self._file_filter = file_filter
        self._mode_config = mode
        self._last_path = None
        self._paths = []  # Cache de múltiplos arquivos

        # Definir modo inicial (semáforo para seleção)
        if mode == self.MODE_FILES:
            self._mode = self.MODE_FILES
        elif mode == self.MODE_FILE:
            self._mode = self.MODE_FILE
        else:
            # folder e radio iniciam como folder até o usuário mudar
            self._mode = self.MODE_FOLDER

        self._build_ui()
    
    def _build_ui(self):
        """Constrói UI completa (radio ou modo fixo, dependendo da configuração)."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(2)

        # ========== RADIOS (OPCIONAL) ==========
        if self._mode_config == self.MODE_RADIO:
            radio_layout = QHBoxLayout()
            radio_layout.setContentsMargins(0, 0, 0, 0)
            radio_layout.setSpacing(6)
            radio_layout.addWidget(QLabel("Selecionar:"))

            self._radio_folder = QRadioButton("📁 Pasta")
            self._radio_files = QRadioButton("📄 Arquivos")
            self._radio_files.setChecked(True)  # Padrão

            self._radio_group = QButtonGroup()
            self._radio_group.addButton(self._radio_folder, 0)
            self._radio_group.addButton(self._radio_files, 1)

            # Conectar radios internamente
            self._radio_folder.toggled.connect(self._on_radio_folder_changed)
            self._radio_files.toggled.connect(self._on_radio_files_changed)

            radio_layout.addWidget(self._radio_folder)
            radio_layout.addWidget(self._radio_files)
            radio_layout.addStretch()
            main_layout.addLayout(radio_layout)

        # ========== INPUT + BOTÃO ==========
        input_layout = QHBoxLayout()
        input_layout.setContentsMargins(0, 0, 0, 0)
        input_layout.setSpacing(4)
        input_layout.addWidget(QLabel(self._title))

        self._input = QLineEdit()
        self._input.setPlaceholderText("Nenhum caminho selecionado")
        self._input.setMaximumHeight(24)
        # Validar quando user digita/cola
        self._input.textChanged.connect(self._on_input_changed)
        input_layout.addWidget(self._input)

        btn = QPushButton("...")
        btn.setFixedWidth(36)
        btn.setFixedHeight(24)
        btn.clicked.connect(self._browse)
        input_layout.addWidget(btn)
        main_layout.addLayout(input_layout)
    
    def _on_radio_folder_changed(self, checked: bool):
        """Radio Pasta alternado"""
        if checked:
            self._mode = self.MODE_FOLDER
            # Limpar lista ao mudar para pasta (radio selecionou pasta singular)
            self._paths = []
            # User agora seleciona UMA pasta
    
    def _on_radio_files_changed(self, checked: bool):
        """Radio Arquivos alternado"""
        if checked:
            self._mode = self.MODE_FILES
            self._paths = []
    
    def _on_input_changed(self, text: str):
        """User digitou/colou algo no input - validar e atualizar lista"""
        text = text.strip()

        if not text:
            self._paths = []
            self.pathsChanged.emit([])
            return

        # Modo apenas pasta: aceita somente diretório
        if self._mode_config == self.MODE_FOLDER:
            if os.path.isdir(text):
                self._mode = self.MODE_FOLDER
                self._paths = [text]
                self._last_path = text
                self.pathsChanged.emit([text])
            return

        # Modo apenas arquivos: aceita somente arquivo
        if self._mode_config == self.MODE_FILE:
            if os.path.isfile(text):
                self._mode = self.MODE_FILE
                self._paths = [text]
                self._last_path = os.path.dirname(text)
                self.pathsChanged.emit([text])
            return

        # Modo rádio (pasta ou arquivos): o comportamento anterior
        if os.path.isdir(text):
            # É pasta → selecionar radio pasta e usar como lista
            if hasattr(self, "_radio_folder") and not self._radio_folder.isChecked():
                self._radio_folder.blockSignals(True)
                self._radio_folder.setChecked(True)
                self._radio_folder.blockSignals(False)
            self._mode = self.MODE_FOLDER
            self._paths = [text]
            self._last_path = text
            self.pathsChanged.emit([text])

        elif os.path.isfile(text):
            # É arquivo → selecionar radio arquivos e usar como lista com 1 item
            if hasattr(self, "_radio_files") and not self._radio_files.isChecked():
                self._radio_files.blockSignals(True)
                self._radio_files.setChecked(True)
                self._radio_files.blockSignals(False)
            self._mode = self.MODE_FILE
            self._paths = [text]
            self._last_path = os.path.dirname(text)
            self.pathsChanged.emit([text])

        else:
            # Não existe, mas user pode estar digitando → não atualizar lista ainda
            pass
    
    def _browse(self):
        """Abre dialog para selecionar"""
        initial_dir = self._get_initial_directory()
        
        try:
            if self._mode == self.MODE_FOLDER:
                self._browse_folder(initial_dir)
            else:  # MODE_FILE ou MODE_FILES
                self._browse_multiple_files(initial_dir)
        except Exception:
            pass
    
    def _get_initial_directory(self) -> str:
        """Retorna diretório inicial"""
        current_path = self._input.text().strip()
        
        if current_path and os.path.isdir(current_path):
            return current_path
        
        if self._last_path and os.path.isdir(self._last_path):
            return self._last_path
        
        return str(Path.home())
    
    def _browse_folder(self, initial_dir: str):
        """Abre dialog para pasta única"""
        folder = QFileDialog.getExistingDirectory(
            self,
            self._title,
            initial_dir
        )
        
        if folder:
            self._mode = self.MODE_FOLDER
            self._paths = [folder]
            self._last_path = folder
            self._input.setText(folder)
            self.pathsChanged.emit([folder])
    
    def _browse_multiple_files(self, initial_dir: str):
        """Abre dialog para múltiplos arquivos"""
        files, _ = QFileDialog.getOpenFileNames(
            self,
            self._title,
            initial_dir,
            self._file_filter
        )
        
        if files:
            # Verificar se todos os items selecionados são pastas ou se existe pelo menos 1 pasta
            # (alguns dialogs permitem selecionar pastas mesmo em modo de arquivo)
            has_folders = any(os.path.isdir(f) for f in files)
            
            if has_folders:
                # Se user selecionou pasta(s), usar a primeira como pasta base
                folder = next((f for f in files if os.path.isdir(f)), None)
                if folder:
                    self._mode = self.MODE_FOLDER
                    self._paths = [folder]
                    self._last_path = folder
                    self._input.setText(folder)
                    self.pathsChanged.emit([folder])
                    return
            
            # Caso normal: múltiplos arquivos
            if len(files) == 1:
                self._mode = self.MODE_FILE
            else:
                self._mode = self.MODE_FILES
            
            self._paths = files
            self._last_path = os.path.dirname(files[0])
            self._input.setText(f"{len(files)} arquivo(s) selecionado(s)")
            self.pathsChanged.emit(files)
    
    def get_paths(self) -> list:
        """
        Retorna lista de paths selecionados.
        
        SEMPRE retorna lista:
        - [] se nada selecionado
        - ["C:/pasta"] se pasta
        - ["C:/arquivo.mrk"] se 1 arquivo
        - ["C:/a.mrk", "C:/b.mrk"] se múltiplos
        
        Returns:
            list: Lista de paths (pode estar vazia)
        """
        return self._paths.copy()
    
    def set_path(self, path: str):
        """Define um caminho (compatibilidade)"""
        if path:
            self._input.setText(path)
            self._on_input_changed(path)
    
    def set_paths(self, paths: list):
        """Define múltiplos caminhos (compatibilidade)"""
        if paths:
            self._paths = paths.copy()
            self._input.setText(f"{len(paths)} arquivo(s) selecionado(s)")
            self.pathsChanged.emit(paths)
    
    def clear(self):
        """Limpa tudo"""
        self._input.setText("")
        self._paths = []
        self.pathsChanged.emit([])
    
    def is_empty(self) -> bool:
        """Verifica se está vazio"""
        return len(self._paths) == 0

