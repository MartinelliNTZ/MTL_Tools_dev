# -*- coding: utf-8 -*-
"""Utilitarios para extracao e parsing de metadados XMP."""

import os
from datetime import datetime
from xml.etree import ElementTree as ET

from ...core.config.LogUtils import LogUtils
from ..ToolKeys import ToolKey


class XmpUtil:
    """Utilitario para extracao e normalizacao de dados XMP."""

    _NAMESPACE_PREFIXES = {
        "http://www.dji.com/drone-dji/1.0/": "drone-dji",
        "http://ns.adobe.com/xap/1.0/": "xmp",
        "http://purl.org/dc/elements/1.1/": "dc",
        "http://ns.adobe.com/camera-raw-settings/1.0/": "crs",
        "http://pix4d.com/camera/1.0": "Camera",
        "http://ns.adobe.com/exif/1.0/aux/": "aux",
        "http://ns.adobe.com/photoshop/1.0/": "photoshop",
        "http://ns.adobe.com/tiff/1.0/": "tiff",
        "http://www.w3.org/1999/02/22-rdf-syntax-ns#": "rdf",
    }

    _FIELD_PRIORITY = [
        "drone-dji:Version",
        "drone-dji:ImageSource",
        "drone-dji:GpsStatus",
        "drone-dji:AltitudeType",
        "drone-dji:AbsoluteAltitude",
        "drone-dji:RelativeAltitude",
        "drone-dji:GimbalRollDegree",
        "drone-dji:GimbalYawDegree",
        "drone-dji:GimbalPitchDegree",
        "drone-dji:FlightRollDegree",
        "drone-dji:FlightYawDegree",
        "drone-dji:FlightPitchDegree",
        "drone-dji:SurveyingMode",
        "drone-dji:DewarpFlag",
        "drone-dji:DewarpData",
        "drone-dji:CalibratedFocalLength",
        "drone-dji:CalibratedOpticalCenterX",
        "drone-dji:CalibratedOpticalCenterY",
        "drone-dji:UTCAtExposure",
        "drone-dji:ShutterType",
        "drone-dji:ShutterCount",
        "drone-dji:FocusDistance",
        "drone-dji:CameraSerialNumber",
        "drone-dji:DroneModel",
        "drone-dji:DroneSerialNumber",
        "drone-dji:CaptureUUID",
        "drone-dji:PictureQuality",
        "xmp:ModifyDate",
        "xmp:CreateDate",
        "xmp:CreatorTool",
        "dc:format",
    ]

    @staticmethod
    def _get_logger(tool_key: str = ToolKey.UNTRACEABLE) -> LogUtils:
        return LogUtils(tool=tool_key, class_name="XmpUtil")

    @staticmethod
    def _extract_xmp_text_raw(image_path: str) -> str:
        with open(image_path, "rb") as fh:
            raw = fh.read().decode("latin1", errors="ignore")

        start = raw.find("<x:xmpmeta")
        if start == -1:
            return ""

        end_marker = "</x:xmpmeta>"
        end = raw.find(end_marker, start)
        if end == -1:
            return ""

        end += len(end_marker)
        return raw[start:end]

    @staticmethod
    def _normalize_attribute_name(attr_name: str) -> str:
        if not attr_name.startswith("{"):
            return attr_name

        namespace, local_name = attr_name[1:].split("}", 1)
        prefix = XmpUtil._NAMESPACE_PREFIXES.get(namespace, namespace)
        return f"{prefix}:{local_name}"

    @staticmethod
    def _parse_xmp_xml(xmp_text: str) -> dict:
        data = {}

        try:
            root = ET.fromstring(xmp_text)
        except ET.ParseError as exc:
            data["xmp_erro"] = str(exc)
            return data

        description = root.find(
            ".//{http://www.w3.org/1999/02/22-rdf-syntax-ns#}Description"
        )
        if description is None:
            data["xmp_erro"] = "Bloco rdf:Description nao encontrado"
            return data

        for attr_name, attr_value in description.attrib.items():
            data[XmpUtil._normalize_attribute_name(attr_name)] = attr_value

        return data

    @staticmethod
    def _order_fields_by_priority(xmp_data: dict) -> dict:
        ordered = {}

        for key in XmpUtil._FIELD_PRIORITY:
            if key in xmp_data:
                ordered[key] = xmp_data[key]

        for key in sorted(xmp_data):
            if key not in ordered:
                ordered[key] = xmp_data[key]

        return ordered

    @staticmethod
    def _extract_file_metadata(image_path: str) -> dict:
        stat = os.stat(image_path)
        return {
            "arquivo": os.path.basename(image_path),
            "caminho": image_path,
            "tamanho_mb": round(stat.st_size / (1024 * 1024), 2),
            "data_criacao": datetime.fromtimestamp(stat.st_ctime).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
        }

    @staticmethod
    def extract_metadata(image_path: str, tool_key: str = ToolKey.UNTRACEABLE) -> dict:
        logger = XmpUtil._get_logger(tool_key)
        data = {}

        try:
            data = XmpUtil._extract_file_metadata(image_path)
            xmp_text = XmpUtil._extract_xmp_text_raw(image_path)
            if not xmp_text:
                data["xmp_encontrado"] = "nao"
                return data

            data["xmp_encontrado"] = "sim"
            xmp_data = XmpUtil._parse_xmp_xml(xmp_text)
            if "xmp_erro" in xmp_data:
                data.update(xmp_data)
                return data

            data.update(XmpUtil._order_fields_by_priority(xmp_data))
            return data
        except Exception as exc:
            logger.error(f"Erro ao extrair metadata XMP de {image_path}: {exc}")
            data.setdefault("arquivo", os.path.basename(image_path))
            data.setdefault("caminho", image_path)
            data["xmp_erro"] = str(exc)
            return data

    @staticmethod
    def process_directory(
        base_folder: str,
        output_file: str = "relatorio_xmp.txt",
        tool_key: str = ToolKey.UNTRACEABLE,
    ) -> str:
        logger = XmpUtil._get_logger(tool_key)
        output_path = os.path.join(base_folder, output_file)
        all_data = []

        for root, _, files in os.walk(base_folder):
            for name in sorted(files):
                if not name.lower().endswith((".jpg", ".jpeg")):
                    continue

                full_path = os.path.join(root, name)
                try:
                    all_data.append(XmpUtil.extract_metadata(full_path, tool_key=tool_key))
                except Exception as exc:
                    all_data.append(
                        {
                            "arquivo": name,
                            "caminho": full_path,
                            "erro": str(exc),
                        }
                    )

        with open(output_path, "w", encoding="utf-8") as fh:
            for index, item in enumerate(all_data, 1):
                fh.write(f"{'=' * 60}\n")
                fh.write(f"FOTO {index}\n")
                fh.write(f"{'=' * 60}\n")
                for key, value in item.items():
                    fh.write(f"{key}: {value}\n")
                fh.write("\n")

        logger.info(
            "Relatorio XMP gerado",
            data={"output_path": output_path, "total_photos": len(all_data)},
        )
        return output_path
