# -*- coding: utf-8 -*- 
import os
from pathlib import Path
from datetime import datetime
import shutil

from qgis.PyQt.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QMessageBox, QFileDialog, QCheckBox, QTextEdit
)
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtCore import Qt

from qgis.core import (
    QgsProject,
    QgsVectorLayer,
    QgsRasterLayer,
)

from ..utils.preferences import (
    load_tool_prefs,
    save_tool_prefs,
)
from ..utils.info_dialog import InfoDialog



# ============================================================
#  ** Janela Principal da Ferramenta **
# ============================================================

class LoadFolderLayersDialog(QDialog):

    TOOL_KEY = "load_folder_layers"

    FILE_TYPES = {
        "Shapefile (*.shp)": (".shp",),
        "GeoJSON (*.geojson *.json)": (".geojson", ".json"),
        "KML (*.kml)": (".kml",),
        "KMZ (*.kmz)": (".kmz",),
        "TIFF/GeoTIFF (*.tif *.tiff)": (".tif", ".tiff"),
        "ECW (*.ecw)": (".ecw",),
        "JPEG2000 (*.jp2)": (".jp2",),
        "ASCII GRID (*.asc)": (".asc",),
        "GPX (*.gpx)": (".gpx",),
        "CSV (*.csv)": (".csv",),
        "MapInfo TAB (*.tab)": (".tab",),
        "LAS/LAZ (*.las *.laz)": (".las", ".laz"),
    }

    def _normalize_layer_source(self, src: str):
        """Remove parâmetros e retorna caminho absoluto normalizado."""
        if "|" in src:
            src = src.split("|")[0]

        try:
            return os.path.normpath(str(Path(src).resolve()))
        except Exception:
            return os.path.normpath(src)


    def __init__(self, iface):
        super().__init__(iface.mainWindow())
        self.iface = iface
        self.setWindowTitle("MTL Tools — Carregar Pasta de Arquivos")
        self.setMinimumWidth(520)

        icon_path = os.path.join(os.path.dirname(__file__),"..", "resources","icons", "load_folder.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        # Caminho do arquivo de instruções
        self.instructions_file = os.path.join(
            os.path.dirname(__file__), "instructions", "load_folder_layers.md"
        )

        main = QVBoxLayout()

        # -------------------------------------------------------
        # INFO BUTTON (canto superior direito)
        # -------------------------------------------------------
        info_layout = QHBoxLayout()
        info_layout.addStretch()

        btn_info = QPushButton("ℹ️")
        btn_info.setFixedWidth(30)
        btn_info.clicked.connect(self.show_info)
        info_layout.addWidget(btn_info)

        main.addLayout(info_layout)

        # -------------------------------------------------------
        # PASTA DE ORIGEM
        # -------------------------------------------------------
        h_folder = QHBoxLayout()
        h_folder.addWidget(QLabel("Pasta raiz:"))
        self.txt_folder = QLineEdit()
        h_folder.addWidget(self.txt_folder)
        btn_browse = QPushButton("...")
        btn_browse.clicked.connect(self._pick_folder)
        h_folder.addWidget(btn_browse)
        main.addLayout(h_folder)

        # -------------------------------------------------------
        # CHECKS DE TIPOS DE ARQUIVOS
        # -------------------------------------------------------
        main.addWidget(QLabel("<b>Tipos de Arquivo:</b>"))
        self.chk_types = {}

        for label in self.FILE_TYPES.keys():
            chk = QCheckBox(label)
            main.addWidget(chk)
            self.chk_types[label] = chk

        # -------------------------------------------------------
        # OPÇÕES DE COMPORTAMENTO
        # -------------------------------------------------------
        self.chk_load_missing_only = QCheckBox("Carregar apenas arquivos ainda NÃO carregados no projeto")
        main.addWidget(self.chk_load_missing_only)

        self.chk_preserve_structure = QCheckBox("Criar grupos conforme estrutura de pastas/subpastas")
        main.addWidget(self.chk_preserve_structure)

        self.chk_backup = QCheckBox("Criar backup do projeto antes de carregar (somente se salvo)")
        main.addWidget(self.chk_backup)

        # -------------------------------------------------------
        # BOTÕES
        # -------------------------------------------------------
        h_btns = QHBoxLayout()
        h_btns.addStretch()
        btn_run = QPushButton("Carregar Arquivos")
        btn_run.clicked.connect(self.run_tool)
        h_btns.addWidget(btn_run)
        btn_close = QPushButton("Fechar")
        btn_close.clicked.connect(self.close)
        h_btns.addWidget(btn_close)
        main.addLayout(h_btns)

        self.setLayout(main)

        # Carregar preferências
        self._load_prefs()


    # ------------------------------------------------------------------
    def show_info(self):
        dlg = InfoDialog(self.instructions_file, self,"📘 Instruções de Uso – Carregar Pasta de Arquivos")
        dlg.exec()

    # ------------------------------------------------------------------
    def _pick_folder(self):
        d = QFileDialog.getExistingDirectory(self, "Selecione a pasta")
        if d:
            self.txt_folder.setText(d)

    # ------------------------------------------------------------------
    def _load_prefs(self):
        prefs = load_tool_prefs(self.TOOL_KEY)

        self.txt_folder.setText(prefs.get("folder", ""))

        saved_types = prefs.get("types", [])
        for label, chk in self.chk_types.items():
            chk.setChecked(label in saved_types)

        self.chk_load_missing_only.setChecked(prefs.get("missing_only", False))
        self.chk_preserve_structure.setChecked(prefs.get("preserve", True))
        self.chk_backup.setChecked(prefs.get("backup", True))

        if not QgsProject.instance().fileName():
            self.chk_backup.setChecked(False)
            self.chk_backup.setEnabled(False)

    # ------------------------------------------------------------------
    def _save_prefs(self):
        selected_types = []

        for label, chk in self.chk_types.items():
            if chk.isChecked():
                selected_types.append(label)

        data = {
            "folder": self.txt_folder.text(),
            "types": selected_types,
            "missing_only": self.chk_load_missing_only.isChecked(),
            "preserve": self.chk_preserve_structure.isChecked(),
            "backup": self.chk_backup.isChecked()
        }

        save_tool_prefs(self.TOOL_KEY, data)

    # ------------------------------------------------------------------
    def _make_backup(self):
        project_path = QgsProject.instance().fileName()
        if not project_path:
            return None

        p = Path(project_path)
        backup_dir = p.parent / "backup"
        backup_dir.mkdir(exist_ok=True)

        ts = datetime.now().strftime("%Y%m%d%H%M%S")
        dest = backup_dir / f"{p.stem}_before_load_{ts}{p.suffix}"

        shutil.copy2(project_path, dest)
        return str(dest)

    # ------------------------------------------------------------------
    def run_tool(self):

        folder = self.txt_folder.text().strip()
        if not folder or not os.path.isdir(folder):
            QMessageBox.warning(self, "Erro", "Selecione uma pasta válida.")
            return

        self._save_prefs()

        backup_file = None
        if self.chk_backup.isChecked():
            backup_file = self._make_backup()

        extensions = []
        for label, chk in self.chk_types.items():
            if chk.isChecked():
                extensions.extend(self.FILE_TYPES[label])

        if not extensions:
            QMessageBox.warning(self, "Erro", "Selecione pelo menos um tipo de arquivo.")
            return

        project = QgsProject.instance()

        already_loaded = set()
        if self.chk_load_missing_only.isChecked():
            for layer in project.mapLayers().values():
                src = self._normalize_layer_source(layer.source())
                already_loaded.add(src)

        loaded_count = 0

        for root, dirs, files in os.walk(folder):
            p_root = Path(root)

            for f in files:
                if not any(f.lower().endswith(e) for e in extensions):
                    continue

                full = str(p_root / f)
                full_norm = self._normalize_layer_source(full)

                if self.chk_load_missing_only.isChecked() and full_norm in already_loaded:
                    continue

                if f.lower().endswith((".tif", ".tiff", ".ecw", ".jp2", ".asc")):
                    layer = QgsRasterLayer(full, f)
                else:
                    layer = QgsVectorLayer(full, f, "ogr")

                if not layer or not layer.isValid():
                    continue

                if self.chk_preserve_structure.isChecked():
                    rel = os.path.relpath(root, folder)
                    if rel == ".":
                        group = project.layerTreeRoot()
                    else:
                        group = self._ensure_group(rel)

                    project.addMapLayer(layer, False)
                    group.insertLayer(0, layer)

                else:
                    project.addMapLayer(layer, True)

                loaded_count += 1

        QMessageBox.information(
            self,
            "Concluído",
            f"Foram carregados {loaded_count} arquivos.\n"
            + (f"Backup criado: {backup_file}" if backup_file else "")
        )

    # ------------------------------------------------------------------
    def _ensure_group(self, rel_path: str):
        project = QgsProject.instance()
        root = project.layerTreeRoot()

        parts = rel_path.split(os.sep)
        current = root

        for part in parts:
            found = current.findGroup(part)
            if not found:
                found = current.addGroup(part)
            current = found

        return current


# Função pública
def run_load_folder_layers(iface):
    dlg = LoadFolderLayersDialog(iface)
    dlg.exec()
