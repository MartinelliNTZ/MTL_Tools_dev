# -*- coding: utf-8 -*-
from qgis.PyQt.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton,
    QHBoxLayout, QLineEdit, QGroupBox
)
from qgis.PyQt.QtGui import QGuiApplication


class CoordResultDialog(QDialog):

    # ==================================================
    # INIT
    # ==================================================
    def __init__(self, iface, info):
        super().__init__(iface.mainWindow())
        self.iface = iface
        self.info = info

        self.setWindowTitle("Coordenadas do Ponto")
        self.setMinimumWidth(640)

        self._build_ui()
        self.update_info(info)

    # ==================================================
    # UI BUILDER
    # ==================================================
    def _build_ui(self):
        self.main_layout = QVBoxLayout()

        self.grp_wgs = self._build_wgs_group()
        self.grp_utm = self._build_utm_group()
        self.grp_alt = self._build_alt_group()
        self.grp_addr = self._build_address_group()

        self.main_layout.addWidget(self.grp_wgs)
        self.main_layout.addWidget(self.grp_utm)
        self.main_layout.addWidget(self.grp_alt)
        self.main_layout.addWidget(self.grp_addr)
        self.main_layout.addWidget(self._build_close_button())

        self.setLayout(self.main_layout)

    # ==================================================
    # GROUPS
    # ==================================================
    def _build_wgs_group(self):
        grp = QGroupBox("WGS 84 (EPSG:4326)")
        layout = QVBoxLayout()

        self.lat_dec_edit = self._line_edit()
        self.lon_dec_edit = self._line_edit()
        self.lat_dms_edit = self._line_edit()
        self.lon_dms_edit = self._line_edit()

        layout.addLayout(self._line("Latitude (Decimal)", self.lat_dec_edit))
        layout.addLayout(self._line("Longitude (Decimal)", self.lon_dec_edit))
        layout.addLayout(self._line("Latitude (DMS)", self.lat_dms_edit))
        layout.addLayout(self._line("Longitude (DMS)", self.lon_dms_edit))

        self.lbl_utm_zone = QLabel()
        layout.addWidget(self.lbl_utm_zone)

        layout.addWidget(self._copy_button(
            "Copiar WGS 84 (Completo)", self.copy_wgs84
        ))

        grp.setLayout(layout)
        return grp

    def _build_utm_group(self):
        grp = QGroupBox("UTM SIRGAS 2000")
        layout = QVBoxLayout()

        self.lbl_utm_info = QLabel()
        layout.addWidget(self.lbl_utm_info)

        self.utm_x_edit = self._line_edit()
        self.utm_y_edit = self._line_edit()

        layout.addLayout(self._line("Easting (X)", self.utm_x_edit))
        layout.addLayout(self._line("Northing (Y)", self.utm_y_edit))

        layout.addWidget(self._copy_button(
            "Copiar UTM (Completo)", self.copy_utm
        ))

        grp.setLayout(layout)
        return grp

    def _build_alt_group(self):
        grp = QGroupBox("Altimetria (OpenTopoData)")
        layout = QVBoxLayout()

        self.alt_edit = QLineEdit("Carregando...")
        self.alt_edit.setReadOnly(True)

        layout.addWidget(QLabel("Altitude aproximada (m)"))
        layout.addWidget(self.alt_edit)

        grp.setLayout(layout)
        return grp

    def _build_address_group(self):
        grp = QGroupBox("Localização Administrativa (OSM)")
        layout = QVBoxLayout()

        self.lbl_municipio = QLabel()
        self.lbl_state_district = QLabel()
        self.lbl_state = QLabel()
        self.lbl_region = QLabel()
        self.lbl_country = QLabel()

        layout.addWidget(self.lbl_municipio)
        layout.addWidget(self.lbl_state_district)
        layout.addWidget(self.lbl_state)
        layout.addWidget(self.lbl_region)
        layout.addWidget(self.lbl_country)

        layout.addWidget(self._copy_button(
            "Copiar Localização (Completo)", self.copy_address
        ))

        grp.setLayout(layout)
        return grp

    def _build_close_button(self):
        btn = QPushButton("Fechar")
        btn.clicked.connect(self.close)
        return btn

    # ==================================================
    # HELPERS
    # ==================================================
    def _line_edit(self):
        e = QLineEdit()
        e.setReadOnly(True)
        return e

    def _line(self, label, edit):
        h = QHBoxLayout()
        btn = QPushButton("Copiar")
        btn.clicked.connect(
            lambda: QGuiApplication.clipboard().setText(edit.text())
        )
        h.addWidget(QLabel(label))
        h.addWidget(edit)
        h.addWidget(btn)
        return h

    def _copy_button(self, text, slot):
        btn = QPushButton(text)
        btn.clicked.connect(slot)
        return btn

    # ==================================================
    # UPDATE (USADO PELO MAPTOOL)
    # ==================================================
    def update_info(self, info):
        self.info = info

        # WGS
        self.lat_dec_edit.setText(f"{info['lat']:.8f}")
        self.lon_dec_edit.setText(f"{info['lon']:.8f}")
        self.lat_dms_edit.setText(info['lat_dms'])
        self.lon_dms_edit.setText(info['lon_dms'])

        self.lbl_utm_zone.setText(
            f"Zona UTM: {info['zona_num']}{info['zona_letra']} | "
            f"Hemisfério: {info['hemisferio']}"
        )

        # UTM
        self.lbl_utm_info.setText(
            f"EPSG:{info['epsg']} | Zona {info['zona_num']}{info['zona_letra']} | "
            f"Hemisfério {info['hemisferio']}"
        )

        self.utm_x_edit.setText(f"{info['utm_x']:.3f}")
        self.utm_y_edit.setText(f"{info['utm_y']:.3f}")

        # Reset async fields
        self.alt_edit.setText("Carregando...")
        self.set_address(None)

    # ==================================================
    # TASK CALLBACKS
    # ==================================================
    def set_altitude(self, value):
        self.alt_edit.setText(
            "Indisponível" if value is None else f"{value:.2f} m"
        )

    def set_address(self, data):
        if not data:
            self.lbl_municipio.setText("Município: carregando...")
            self.lbl_state_district.setText("Região Intermediária: carregando...")
            self.lbl_state.setText("Estado: carregando...")
            self.lbl_region.setText("Região: carregando...")
            self.lbl_country.setText("País: carregando...")
            return

        self.lbl_municipio.setText(f"Município: {data.get('municipio', '-')}")
        self.lbl_state_district.setText(
            f"Região Intermediária: {data.get('state_district', '-')}"
        )
        self.lbl_state.setText(f"Estado: {data.get('state', '-')}")
        self.lbl_region.setText(f"Região: {data.get('region', '-')}")
        self.lbl_country.setText(f"País: {data.get('country', '-')}")

    # ==================================================
    # COPY
    # ==================================================
    def copy_wgs84(self):
        i = self.info
        QGuiApplication.clipboard().setText(
            f"WGS84\n"
            f"Lat={i['lat']:.8f}\nLon={i['lon']:.8f}\n"
            f"Lat DMS={i['lat_dms']}\nLon DMS={i['lon_dms']}\n"
            f"Zona={i['zona_num']}{i['zona_letra']} | Hem={i['hemisferio']}"
        )

    def copy_utm(self):
        i = self.info
        QGuiApplication.clipboard().setText(
            f"UTM SIRGAS 2000\n"
            f"EPSG:{i['epsg']}\n"
            f"X={i['utm_x']:.3f}\nY={i['utm_y']:.3f}"
        )

    def copy_address(self):
        QGuiApplication.clipboard().setText(
            f"{self.lbl_municipio.text()}\n"
            f"{self.lbl_state_district.text()}\n"
            f"{self.lbl_state.text()}\n"
            f"{self.lbl_region.text()}\n"
            f"{self.lbl_country.text()}"
        )
