# -*- coding: utf-8 -*-

import os
import re
from datetime import datetime

from qgis.core import (
    QgsVectorLayer,
    QgsFeature,
    QgsGeometry,
    QgsPointXY,
    QgsField,
    QgsFields,
    QgsProject
)

from PyQt5.QtCore import QVariant
from PIL import Image, ExifTags


# ============================================================
# LOG
# ============================================================

def get_log_path():
    prj = QgsProject.instance().fileName()
    base = os.path.dirname(prj) if prj else os.path.join(
        os.path.expanduser("~"), "AppData", "Local", "MTLTools"
    )
    log_dir = os.path.join(base, "log")
    os.makedirs(log_dir, exist_ok=True)
    return os.path.join(log_dir, "log.txt")


def log_debug(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(get_log_path(), "a", encoding="utf-8") as f:
        f.write(f"[{ts}] {msg}\n")


# ============================================================
# HELPERS
# ============================================================

def dt_to_str(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S") if isinstance(dt, datetime) else None


def dt_parts(dt):
    """
    Retorna:
    full  -> YYYYMMDDHHMMSS
    date  -> YYYYMMDD
    time  -> HHMMSS
    """
    if not isinstance(dt, datetime):
        return None, None, None

    return (
        dt.strftime("%Y%m%d%H%M%S"),
        dt.strftime("%Y%m%d"),
        dt.strftime("%H%M%S")
    )


def to_int(v):
    try:
        return int(v)
    except Exception:
        return None


def to_float(v):
    try:
        return float(v)
    except Exception:
        return None


def to_str(v):
    return str(v) if v not in (None, "") else None


# ============================================================
# PROCESSADOR MRK
# ============================================================

class MrkPhotoProcessorModel:

    LINE_RE = re.compile(
        r"(?P<foto>\d+).*?"
        r"(?P<lat>-?\d+\.\d+),Lat.*?"
        r"(?P<lon>-?\d+\.\d+),Lon.*?"
        r"(?P<alt>-?\d+(\.\d+)?),Ellh",
        re.IGNORECASE
    )

    # --------------------------------------------------------

    def run(self, base_folder, scan_subfolders=True, merge_mrk=True, load_photos_metadata=True):
        flights = self._collect_flights(base_folder, scan_subfolders)

        if merge_mrk:
            all_points = []
            any_folder = None

            for data in flights.values():
                all_points.extend(data["points"])
                any_folder = data["folder"]

            if not all_points:
                return [], []

            vl_pts, vl_line = self._build_layers(
                "MERGE",
                all_points,
                any_folder,
                load_photos_metadata
            )

            return [vl_pts], [vl_line] if vl_line else []

        # ----------------------------
        # modo normal (sem merge)
        # ----------------------------
        pts_layers = []
        line_layers = []

        for flight, data in flights.items():
            vl_pts, vl_line = self._build_layers(
                flight,
                data["points"],
                data["folder"],
                load_photos_metadata
            )
            pts_layers.append(vl_pts)
            if vl_line:
                line_layers.append(vl_line)

        return pts_layers, line_layers


    def _collect_flights(self, base_folder, recursive):
        flights = {}

        for root, _, files in os.walk(base_folder):
            for fname in files:
                if not fname.lower().endswith(".mrk"):
                    continue

                mrk_path = os.path.join(root, fname)
                flight_key = os.path.basename(root)

                flights.setdefault(flight_key, {
                    "folder": root,
                    "points": []
                })

                log_debug(f"Lendo MRK: {mrk_path}")

                with open(mrk_path, "r", encoding="utf-8", errors="ignore") as fh:
                    for line in fh:
                        m = self.LINE_RE.search(line)
                        if not m:
                            continue

                        flights[flight_key]["points"].append({
                            "foto": to_int(m.group("foto")),
                            "lat": to_float(m.group("lat")),
                            "lon": to_float(m.group("lon")),
                            "alt": to_float(m.group("alt"))
                        })

            if not recursive:
                break

        return flights

    # --------------------------------------------------------

    def _build_layers(self, name, points, folder, with_photos):

        fields = QgsFields()
        for fld, typ in [
            ("foto", QVariant.Int),
            ("alt", QVariant.Double),
            ("nome_arq", QVariant.String),
            ("tam_mb", QVariant.Double),
            ("tipo_arq", QVariant.String),

            # datas (texto)
            ("dt_criacao", QVariant.String),
            ("dt_full", QVariant.String),
            ("dt_date", QVariant.String),
            ("dt_time", QVariant.String),

            ("cam_model", QVariant.String),
            ("bit_depth", QVariant.Int),
            ("larg_px", QVariant.Int),
            ("alt_px", QVariant.Int),
            ("res_h_dpi", QVariant.Double),
            ("res_v_dpi", QVariant.Double),
            ("focal_mm", QVariant.Double),
            ("focal35mm", QVariant.Int),
            ("iso", QVariant.Int),
            ("abert_f", QVariant.Double),
        ]:
            fields.append(QgsField(fld, typ))

        vl_pts = QgsVectorLayer(
            "Point?crs=EPSG:4326",
            f"MRK_Pontos_{name}",
            "memory"
        )
        vl_pts.dataProvider().addAttributes(fields)
        vl_pts.updateFields()

        polyline = []
        vl_pts.startEditing()

        for p in sorted(points, key=lambda x: x["foto"]):
            meta = self._photo_metadata(folder, p["foto"]) if with_photos else {}

            dtc = meta.get("dt_criacao")
            dt_full, dt_date, dt_time = dt_parts(dtc)

            feat = QgsFeature(vl_pts.fields())
            feat.setGeometry(QgsGeometry.fromPointXY(
                QgsPointXY(p["lon"], p["lat"])
            ))

            feat.setAttributes([
                p["foto"],
                p["alt"],
                to_str(meta.get("nome_arq")),
                to_float(meta.get("tam_mb")),
                to_str(meta.get("tipo_arq")),

                dt_to_str(dtc),
                dt_full,
                dt_date,
                dt_time,

                to_str(meta.get("cam_model")),
                to_int(meta.get("bit_depth")),
                to_int(meta.get("larg_px")),
                to_int(meta.get("alt_px")),
                to_float(meta.get("res_h_dpi")),
                to_float(meta.get("res_v_dpi")),
                to_float(meta.get("focal_mm")),
                to_int(meta.get("focal35mm")),
                to_int(meta.get("iso")),
                to_float(meta.get("abert_f")),
            ])

            vl_pts.addFeature(feat)
            polyline.append(QgsPointXY(p["lon"], p["lat"]))

        vl_pts.commitChanges()
        vl_pts.updateExtents()

        log_debug(f"Camada pontos criada | total={vl_pts.featureCount()}")

        # ----------------------------------------------------
        # Linha
        # ----------------------------------------------------

        vl_line = None
        if len(polyline) > 1:
            vl_line = QgsVectorLayer(
                "LineString?crs=EPSG:4326",
                f"MRK_Trilha_{name}",
                "memory"
            )
            f_line = QgsFeature()
            f_line.setGeometry(QgsGeometry.fromPolylineXY(polyline))
            vl_line.dataProvider().addFeature(f_line)
            vl_line.updateExtents()

        return vl_pts, vl_line

    # --------------------------------------------------------

    def _photo_metadata(self, folder, foto_number):

        result = {
            "nome_arq": None,
            "tam_mb": None,
            "tipo_arq": None,
            "dt_criacao": None,
            "cam_model": None,
            "bit_depth": None,
            "larg_px": None,
            "alt_px": None,
            "res_h_dpi": None,
            "res_v_dpi": None,
            "focal_mm": None,
            "focal35mm": None,
            "iso": None,
            "abert_f": None,
        }

        foto_str = f"{foto_number:04d}"

        for fname in os.listdir(folder):
            if not fname.lower().endswith(".jpg"):
                continue

            nums = re.findall(r"\d{4}", fname)
            if not nums or nums[-1] != foto_str:
                continue

            path = os.path.join(folder, fname)
            st = os.stat(path)

            result["nome_arq"] = fname
            result["tam_mb"] = round(st.st_size / (1024 * 1024), 2)
            result["tipo_arq"] = "JPG"
            result["dt_criacao"] = datetime.fromtimestamp(st.st_ctime)

            try:
                with Image.open(path) as img:
                    exif_raw = img._getexif() or {}
                    exif = {ExifTags.TAGS.get(k, k): v for k, v in exif_raw.items()}

                    result["cam_model"] = exif.get("Model")
                    result["bit_depth"] = img.bits
                    result["larg_px"], result["alt_px"] = img.size

                    dpi = img.info.get("dpi", (None, None))
                    result["res_h_dpi"] = dpi[0]
                    result["res_v_dpi"] = dpi[1]

                    result["focal_mm"] = exif.get("FocalLength")
                    result["focal35mm"] = exif.get("FocalLengthIn35mmFilm")
                    result["iso"] = exif.get("ISOSpeedRatings")
                    result["abert_f"] = exif.get("FNumber")

            except Exception as e:
                log_debug(f"Erro EXIF | {path} | {e}")

            return result

        return result


