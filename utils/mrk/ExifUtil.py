# -*- coding: utf-8 -*-
"""
Utilities para extracao de metadados EXIF/OS/PIL de imagens.
"""

import os
from datetime import datetime

from PIL import ExifTags, Image

from ...core.config.LogUtils import LogUtils
from ..ToolKeys import ToolKey


class ExifUtil:
    """Utilitario para extrair metadados de arquivo de imagem."""

    @staticmethod
    def _get_logger(tool_key: str = ToolKey.UNTRACEABLE) -> LogUtils:
        return LogUtils(tool=tool_key, class_name="ExifUtil")

    @staticmethod
    def extract_metadata_os(
        image_path: str, tool_key: str = ToolKey.UNTRACEABLE
    ) -> dict:
        """Extrai metadados do sistema operacional."""
        logger = ExifUtil._get_logger(tool_key)
        data = {}
        try:
            stat = os.stat(image_path)
            data["file"] = os.path.basename(image_path)
            data["path"] = image_path
            data["size_mb"] = round(stat.st_size / (1024 * 1024), 2)
            data["os_date"] = datetime.fromtimestamp(stat.st_ctime).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        except Exception as exc:
            logger.error(
                f"Erro ao extrair metadados do sistema para {image_path}: {exc}"
            )
        return data

    @staticmethod
    def extract_metadata_image(
        image_path: str, tool_key: str = ToolKey.UNTRACEABLE
    ) -> dict:
        """Extrai metadados de dimensao/formato/dpi via PIL."""
        logger = ExifUtil._get_logger(tool_key)
        data = {}
        try:
            with Image.open(image_path) as img:
                data["width_px"], data["height_px"] = img.size
                data["format"] = f"{img.format}_{img.mode}"
                dpi = img.info.get("dpi")
                if dpi:
                    dpi_x, dpi_y = dpi
                    data["dpi"] = f"{dpi_x}x{dpi_y}"
        except Exception as exc:
            logger.error(f"Erro ao extrair metadados PIL para {image_path}: {exc}")
        return data

    @staticmethod
    def extract_metadata_exif(
        image_path: str, tool_key: str = ToolKey.UNTRACEABLE
    ) -> dict:
        """Extrai todos os campos EXIF disponiveis."""
        logger = ExifUtil._get_logger(tool_key)
        data = {}
        try:
            with Image.open(image_path) as img:
                exif_raw = img._getexif() or {}
                exif = {ExifTags.TAGS.get(k, k): v for k, v in exif_raw.items()}
                for key, value in exif.items():
                    data[key] = value

                # Expande GPSInfo para chaves individuais (GPSLatitude, GPSLongitude, GPSMapDatum, etc.).
                gps_info = exif.get("GPSInfo")
                if isinstance(gps_info, dict):
                    gps_named = {
                        ExifTags.GPSTAGS.get(k, k): v for k, v in gps_info.items()
                    }
                    for gk, gv in gps_named.items():
                        data[gk] = gv
        except Exception as exc:
            logger.warning(f"Erro ao extrair EXIF de {image_path}: {exc}")
            data["erro"] = str(exc)
        return data
