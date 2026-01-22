# -*- coding: utf-8 -*-
import os

from shapely import points
from qgis.PyQt.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QCheckBox, QLineEdit, QFileDialog
)
from qgis.PyQt.QtGui import QIcon
from qgis.core import QgsProject, QgsApplication
from ..utils.task.drone_task import DronePhotosTask
from ..utils.mrk.mrk_parser import MrkParser
from ..utils.mrk.photo_metadata import PhotoMetadata
from ..utils.vector_utils import VectorUtils
from ..utils.log_utils import LogUtils

from ..utils.preferences import load_tool_prefs, save_tool_prefs
from ..utils.tool_keys import ToolKey
from ..utils.info_dialog import InfoDialog


class DroneCordinates(QDialog):

    TOOL_KEY = ToolKey.DRONE_COORDINATES

    def __init__(self, iface):
        super().__init__(iface.mainWindow())
        self.iface = iface        

        self.setWindowTitle("MTL Tools — Coordenadas de Drone")
        self.setMinimumWidth(420)

        icon_path = os.path.join(os.path.dirname(__file__), "..", "icons", "coord.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        layout = QVBoxLayout(self)

        info_bar = QHBoxLayout()
        info_bar.addStretch()
        btn_info = QPushButton("ℹ️")
        btn_info.setFixedWidth(32)
        btn_info.clicked.connect(self._show_info)
        info_bar.addWidget(btn_info)
        layout.addLayout(info_bar)

        self.instructions_file = os.path.join(
            os.path.dirname(__file__),
            "instructions",
            "drone_coordinates_help.md"
        )

        h_folder = QHBoxLayout()
        h_folder.addWidget(QLabel("Pasta dos MRK:"))
        self.txt_folder = QLineEdit()
        h_folder.addWidget(self.txt_folder)
        btn_pick = QPushButton("...")
        btn_pick.clicked.connect(self._pick_folder)
        h_folder.addWidget(btn_pick)
        layout.addLayout(h_folder)

        self.chk_recursive = QCheckBox("Vasculhar subpastas")
        self.chk_merge = QCheckBox("Unir todos os MRK")
        self.chk_photos = QCheckBox("Cruzar com metadados das fotos(Não recomendado para grandes volumes)")

        layout.addWidget(self.chk_recursive)
        layout.addWidget(self.chk_merge)
        layout.addWidget(self.chk_photos)
        # ---- PONTOS ----
        self.chk_save_points = QCheckBox('Salvar pontos MRK em arquivo?(caso não marcado: camada temporária)')
        layout.addWidget(self.chk_save_points)

        h_out_pts = QHBoxLayout()
        h_out_pts.addWidget(QLabel('Salvar em:'))
        self.txt_output_pts = QLineEdit()
        h_out_pts.addWidget(self.txt_output_pts)
        btn_out_pts = QPushButton('...')
        btn_out_pts.clicked.connect(self._pick_output_points)
        h_out_pts.addWidget(btn_out_pts)
        layout.addLayout(h_out_pts)

        self.chk_apply_style_points = QCheckBox('Aplicar estilo (QML) nos pontos?')
        layout.addWidget(self.chk_apply_style_points)

        h_qml_pts = QHBoxLayout()
        h_qml_pts.addWidget(QLabel('QML pontos:'))
        self.txt_qml_pts = QLineEdit()
        h_qml_pts.addWidget(self.txt_qml_pts)
        btn_qml_pts = QPushButton('...')
        btn_qml_pts.clicked.connect(self._pick_qml_points)
        h_qml_pts.addWidget(btn_qml_pts)
        layout.addLayout(h_qml_pts)

        
        # salvar em arquivo ou temporário
        self.chk_save_track = QCheckBox('Salvar trajeto em arquivo? (caso não marcado: camada temporária)')
        layout.addWidget(self.chk_save_track)

        h_out = QHBoxLayout()
        h_out.addWidget(QLabel('Salvar em:'))
        self.txt_output = QLineEdit()
        h_out.addWidget(self.txt_output)
        btn_out = QPushButton('...')
        btn_out.clicked.connect(self._pick_output_file)
        h_out.addWidget(btn_out)
        layout.addLayout(h_out)
        # aplicar estilo
        self.chk_apply_style_track = QCheckBox('Aplicar estilo (QML) no rastro? ')
        layout.addWidget(self.chk_apply_style_track)

        h_qml = QHBoxLayout()
        h_qml.addWidget(QLabel('QML:'))
        self.txt_qml = QLineEdit()
        h_qml.addWidget(self.txt_qml)
        btn_qml = QPushButton('...')
        btn_qml.clicked.connect(self._pick_qml)
        h_qml.addWidget(btn_qml)
        layout.addLayout(h_qml)



        h_btns = QHBoxLayout()
        h_btns.addStretch()
        btn_run = QPushButton("Executar")
        btn_run.clicked.connect(self._run)
        btn_close = QPushButton("Fechar")
        btn_close.clicked.connect(self.close)
        h_btns.addWidget(btn_run)
        h_btns.addWidget(btn_close)
        layout.addLayout(h_btns)

        self._load_prefs()

    def _show_info(self):
        dlg = InfoDialog(self.instructions_file, self, "📘 Instruções")
        dlg.exec()
        
    def _pick_output_file(self):
        filters = (
            "Shapefile (*.shp);;"
            "GeoPackage (*.gpkg);;"
            "GeoJSON (*.geojson *.json);;"
            "KML (*.kml);;"
            "CSV (*.csv)"
        )
        f, _ = QFileDialog.getSaveFileName(
            self, "Salvar rastro do drone", "", filters
        )
        if f:
            self.txt_output.setText(f)
    def _pick_qml(self):
        f, _ = QFileDialog.getOpenFileName(
            self, 'Selecionar QML', '', 'QML (*.qml)'
        )
        if f:
            self.txt_qml.setText(f)


    def _pick_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self, "Selecione a pasta dos MRK"
        )
        if folder:
            self.txt_folder.setText(folder)
            
    def _pick_output_points(self):
        f, _ = QFileDialog.getSaveFileName(
            self, "Salvar pontos MRK", "",
            "Shapefile (*.shp);;"
            "GeoPackage (*.gpkg);;"
            "GeoJSON (*.geojson *.json);;"
            "KML (*.kml)"
        )
        if f:
            self.txt_output_pts.setText(f)

    def _pick_qml_points(self):
        f, _ = QFileDialog.getOpenFileName(
            self, 'Selecionar QML (Pontos)', '', 'QML (*.qml)'
        )
        if f:
            self.txt_qml_pts.setText(f)


    def _load_prefs(self):
        prefs = load_tool_prefs(self.TOOL_KEY)
        self.txt_folder.setText(prefs.get("folder", ""))
        self.chk_recursive.setChecked(prefs.get("recursive", True))
        self.chk_merge.setChecked(prefs.get("merge", True))
        self.chk_photos.setChecked(prefs.get("photos", True))
        self.chk_save_track.setChecked(prefs.get("save_file", False))
        self.chk_save_points.setChecked(prefs.get("save_file_pts", False))
        self.txt_output.setText(prefs.get("output_path", ""))
        self.txt_output_pts.setText(prefs.get("output_path_pts", ""))
        self.chk_apply_style_track.setChecked(prefs.get("apply_style_track", False))
        self.txt_qml.setText(prefs.get("qml_path_track", ""))
        self.chk_apply_style_points.setChecked(prefs.get("apply_style_points", False))
        self.txt_qml_pts.setText(prefs.get("qml_path_points", ""))


    def _save_prefs(self):
        save_tool_prefs(self.TOOL_KEY, {
            "folder": self.txt_folder.text(),
            "recursive": self.chk_recursive.isChecked(),
            "merge": self.chk_merge.isChecked(),
            "photos": self.chk_photos.isChecked(),
            "save_file": self.chk_save_track.isChecked(),
            "save_file_pts": self.chk_save_points.isChecked(),
            "output_path": self.txt_output.text(),
            "output_path_pts": self.txt_output_pts.text(),
            "apply_style_track": self.chk_apply_style_track.isChecked(),
            "qml_path_track": self.txt_qml.text(),
            "apply_style_points": self.chk_apply_style_points.isChecked(),
            "qml_path_points": self.txt_qml_pts.text()
        })

    def _run(self):
            LogUtils.log(self.TOOL_KEY, "Iniciando processamento de coordenadas de drone")
            base = self.txt_folder.text().strip()
            if not os.path.isdir(base):
                return

            # 1️⃣ MRK → pontos
            extra_fields = None

            if self.chk_photos.isChecked():
                extra_fields = PhotoMetadata.FIELDS_PHOTO

            points = MrkParser.parse_folder(
                base,
                recursive=self.chk_recursive.isChecked(),
                extra_fields=extra_fields
            )
            LogUtils.log(self.TOOL_KEY, f"MRKs processados ({len(points)} pontos)")

            if not points:
                LogUtils.log(self.TOOL_KEY, F"nenhum ponto encontrado nos MRKs em {base}")
                return


            # --- Cruzar com fotos ---
            LogUtils.log(self.TOOL_KEY, F"check photos: {self.chk_photos.isChecked()}, points: {len(points)}")
            if self.chk_photos.isChecked() and points:
                LogUtils.log(self.TOOL_KEY, f"Cruzando MRKs com fotos em {base}")

                # callback que será chamado quando a task terminar
                def continue_flow(result_points):
                    LogUtils.log(self.TOOL_KEY, f"MRKs enriquecidos com fotos ({len(result_points)} pontos)")
                    self._continue_with_points(result_points, extra_fields=extra_fields)
                

                

                task = DronePhotosTask(
                    description="Cruzando MRKs com fotos",
                    points=points,
                    base_folder=base,
                    recursive=self.chk_recursive.isChecked(),
                    callback=continue_flow   # <<< aqui é o importante
                )
                LogUtils.log(self.TOOL_KEY, F"Adicionando task de cruzamento de fotos ao gerenciador de tarefas do QGIS{task}")

                QgsApplication.taskManager().addTask(task)
                task_manager = QgsApplication.taskManager()
                LogUtils.log(self.TOOL_KEY, f"{task_manager.tasks()}  # para checar tasks adicionadas")

            else:
                # Sem cruzamento de fotos, segue normal
                self._continue_with_points(points, extra_fields=extra_fields)

    def _continue_with_points(self, points,extra_fields=None):
        # 3️⃣ Camada pontos
        LogUtils.log(self.TOOL_KEY, f"continue_with_points: criando camada de pontos ({len(points)} pontos)")
        vl_pts = MrkParser.to_point_layer(
            points,
            name="MRK_Pontos",
            extra_fields=extra_fields
        )



        # 4️⃣ Linha
        vl_line = VectorUtils.points_to_path(points)

        save_to_file = self.chk_save_track.isChecked()
        out_path = self.txt_output.text().strip() if save_to_file else None
        apply_style = self.chk_apply_style_track.isChecked()
        qml_path = self.txt_qml.text().strip() or None

        # pontos sempre temporários (igual MRK)
        # ---- PONTOS ----
        if self.chk_save_points.isChecked() and self.txt_output_pts.text().strip():
            pts_layer = VectorUtils.save_layer_obsolet(vl_pts, self.txt_output_pts.text().strip())
            if pts_layer:
                QgsProject.instance().addMapLayer(pts_layer)
        else:
            pts_layer = vl_pts
            QgsProject.instance().addMapLayer(pts_layer)
        # aplicar estilo nos pontos
        if self.chk_apply_style_points.isChecked() and pts_layer:
            try:
                qml = self.txt_qml_pts.text().strip()
                if qml and os.path.exists(qml):
                    ok = pts_layer.loadNamedStyle(qml)
                    if isinstance(ok, tuple):
                        ok = ok[0]
                    if ok:
                        pts_layer.triggerRepaint()
            except Exception:
                pass



        # rastro (linha)
        if vl_line:
            if save_to_file and out_path:
                saved_layer = VectorUtils.save_layer_obsolet(
                    vl_line,
                    out_path
                )
                out_layer = saved_layer
                if out_layer:
                    QgsProject.instance().addMapLayer(out_layer)
            else:
                out_layer = vl_line
                QgsProject.instance().addMapLayer(out_layer)

            # aplicar estilo
            if apply_style and out_layer:
                try:
                    out_layer.reload()
                    out_layer.updateFields()

                    qml_to_use = qml_path
                    if not qml_to_use:
                        qml_to_use = os.path.join(
                            os.path.dirname(__file__),
                            '..', 'styles', 'Drone_Rastro.qml'
                        )
                        qml_to_use = os.path.normpath(qml_to_use)

                    if os.path.exists(qml_to_use):
                        ok = out_layer.loadNamedStyle(qml_to_use)
                        if isinstance(ok, tuple):
                            ok = ok[0]
                        if ok:
                            out_layer.triggerRepaint()
                except Exception:
                    pass


        self._save_prefs()


def run_drone_cordinates(iface):
    dlg = DroneCordinates(iface)
    dlg.setModal(False)
    dlg.show()
    return dlg 
