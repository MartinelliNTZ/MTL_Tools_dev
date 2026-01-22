# -*- coding: utf-8 -*-
import os
import re
from datetime import datetime
from PIL import Image, ExifTags
from PyQt5.QtCore import QVariant
from ..log_utils import LogUtilsOld
from ..tool_keys import ToolKey

LOG_PATH = r"D:\mtl_photo_metadata_debug.txt"
TOOL_KEY = ToolKey.DRONE_COORDINATES
def _dbg(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"[{ts}] {msg}\n")


class PhotoMetadata:
    FIELDS_PHOTO = {
            "nome_arq":QVariant.String,
            "tam_mb":QVariant.Double,
            "tipo_arq":QVariant.String,

            # datas texto
            "dt_criacao":QVariant.String,
            "dt_full":QVariant.String,
            "dt_date":QVariant.String,
            "dt_time":QVariant.String,

            "cam_model":QVariant.String,
            "bit_depth":QVariant.Int,
            "larg_px":QVariant.Int,
            "alt_px":QVariant.Int,
            "res_h_dpi":QVariant.Double,
            "res_v_dpi":QVariant.Double,
            "focal_mm":QVariant.Double,
            "focal35mm":QVariant.Int,
            "iso":QVariant.Int,
            "abert_f":QVariant.Double,
    }


    # DJI_20251107021601_0002_V.JPG
    DJI_RE = re.compile(r"_(\d{4})_[A-Z]\.JPG$", re.IGNORECASE)
    @staticmethod
    def _format_dates(dt):
        """
        Recebe datetime e devolve strings padronizadas
        """
        return {
            "dt_criacao": dt.strftime("%Y-%m-%d %H:%M:%S"),
            "dt_full": dt.strftime("%Y%m%d%H%M"),
            "dt_date": dt.strftime("%Y%m%d"),
            "dt_time": dt.strftime("%H%M"),
        }


    @staticmethod
    def enrich(points, base_folder, recursive=True):
        _dbg("========================================")
        _dbg("ENRICH START")
        _dbg(f"BASE_FOLDER = {base_folder}")
        _dbg(f"RECURSIVE   = {recursive}")
        _dbg(f"PONTOS      = {len(points)}")

        # 🔴 INDEXAÇÃO ÚNICA (CRÍTICO)
        photo_index = PhotoMetadata._index_photos(base_folder, recursive)

        _dbg(f"FOTOS INDEXADAS = {len(photo_index)}")

        for p in points:
            foto = p.get("foto")
            if foto is None:
                continue

            key = f"{int(foto):04d}"
            meta = photo_index.get(key)

            if not meta:
                _dbg(f"FOTO {key} NAO ENCONTRADA")
                continue

            p.update(meta)

        _dbg("ENRICH END")
        _dbg("========================================")
        return points

    # --------------------------------------------------

    @staticmethod
    def _index_photos(base_folder, recursive):
        index = {}

        walker = os.walk(base_folder) if recursive else [
            (base_folder, [], os.listdir(base_folder))
        ]

        # Contar quantos arquivos JPG teremos para calcular percentual
        all_files = []
        for root, _, files in walker:
            for fname in files:
                if fname.lower().endswith(".jpg") and PhotoMetadata.DJI_RE.search(fname):
                    all_files.append((root, fname))
        LogUtilsOld.log(ToolKey.DRONE_COORDINATES,
            f"Indexando fotos: {len(all_files)} arquivos encontrados")
        total = len(all_files)
        if total == 0:
            return index

        next_log = 0.05  # 5%
        log_count = 0

        for i, (root, fname) in enumerate(all_files, start=1):
            m = PhotoMetadata.DJI_RE.search(fname)
            if not m:
                continue

            num = m.group(1)
            path = os.path.join(root, fname)

            try:
                st = os.stat(path)
            except Exception:
                continue

            # datas etc...
            dt = datetime.fromtimestamp(st.st_ctime)
            dates = PhotoMetadata._format_dates(dt)

            meta = {
                "nome_arq": fname,
                "tipo_arq": os.path.splitext(fname)[1].upper(),
                "tam_mb": round(st.st_size / (1024 * 1024), 2),
                **dates,
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

            # EXIF
            try:
                with Image.open(path) as img:
                    exif_raw = img._getexif() or {}
                    exif = {ExifTags.TAGS.get(k, k): v for k, v in exif_raw.items()}
                    meta["larg_px"], meta["alt_px"] = img.size
                    dpi = img.info.get("dpi")
                    if dpi:
                        meta["res_h_dpi"] = float(dpi[0])
                        meta["res_v_dpi"] = float(dpi[1])
                    meta["bit_depth"] = img.bits if hasattr(img, "bits") else None
                    meta["cam_model"] = exif.get("Model")
                    meta["iso"] = exif.get("ISOSpeedRatings")
                    fl = exif.get("FocalLength")
                    if isinstance(fl, tuple):
                        meta["focal_mm"] = round(fl[0] / fl[1], 2)
                    elif fl is not None:
                        meta["focal_mm"] = float(fl)
                    meta["focal35mm"] = exif.get("FocalLengthIn35mmFilm")
                    av = exif.get("MaxApertureValue") or exif.get("FNumber")
                    if isinstance(av, tuple):
                        meta["abert_f"] = round(av[0] / av[1], 2)
                    elif av is not None:
                        meta["abert_f"] = round(float(av), 2)
            except Exception:
                pass

            index[num] = meta

            # -----------------------------
            # LOG A CADA 5%
            percent_done = i / total
            if percent_done >= next_log:
                LogUtilsOld.log(ToolKey.DRONE_COORDINATES,
                    f"{int(percent_done*100)}%  {i} arquivos / {total}")
                next_log += 0.05  # próximo 5%

        return index
