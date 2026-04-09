# -*- coding: utf-8 -*-
import os
from datetime import datetime
from typing import Any, Dict, List, Tuple

from qgis.PyQt.QtCore import QVariant
from qgis.core import QgsProject

from ..config.LogUtils import LogUtils
from .ReportGenerationService import ReportGenerationService
from ...utils.ExplorerUtils import ExplorerUtils
from ...utils.ToolKeys import ToolKey
from ...utils.mrk.ExifUtil import ExifUtil
from ...utils.mrk.MetadataFields import MetadataFields
from ...utils.mrk.XmpUtil import XmpUtil
from ...utils.vector.VectorLayerGeometry import VectorLayerGeometry


class PhotoFolderVectorizationService:
    """Gera camada vetorial e diagnostico a partir de pasta de fotos (sem MRK)."""

    def __init__(self, tool_key: str = ToolKey.REPORT_METADATA):
        self.tool_key = tool_key
        self.logger = LogUtils(tool=tool_key, class_name="PhotoFolderVectorizationService")

    @staticmethod
    def _to_float(value: Any):
        if value is None:
            return None
        if isinstance(value, (int, float)):
            return float(value)
        text = str(value).strip().replace("+", "")
        if text in ("", "None", "null"):
            return None
        try:
            return float(text)
        except Exception:
            return None

    @staticmethod
    def _extract_gps_decimal_from_dms(value, ref):
        if value is None:
            return None

        parts = []
        if isinstance(value, (list, tuple)):
            parts = list(value)
        else:
            return None

        if len(parts) < 3:
            return None

        def _part_to_float(p):
            if isinstance(p, (int, float)):
                return float(p)
            text = str(p).strip()
            if "/" in text:
                num, den = text.split("/", 1)
                return float(num) / float(den)
            return float(text)

        try:
            deg = _part_to_float(parts[0])
            minute = _part_to_float(parts[1])
            sec = _part_to_float(parts[2])
            dec = deg + (minute / 60.0) + (sec / 3600.0)
            ref_txt = str(ref or "").upper().strip()
            if ref_txt in ("S", "W"):
                dec = -dec
            return dec
        except Exception:
            return None

    def _extract_position(self, merged_payload: Dict[str, Any]) -> Tuple[Any, Any, Any, str]:
        """Retorna lat/lon/alt e fonte principal usada."""
        # Prioridade 1: XMP DJI decimal
        lat = self._to_float(merged_payload.get("drone-dji:GpsLatitude") or merged_payload.get("GpsLatitude"))
        lon = self._to_float(merged_payload.get("drone-dji:GpsLongitude") or merged_payload.get("GpsLongitude"))
        if lat is not None and lon is not None:
            alt = self._to_float(
                merged_payload.get("drone-dji:AbsoluteAltitude")
                or merged_payload.get("AbsoluteAltitude")
                or merged_payload.get("GPSAltitude")
            )
            return lat, lon, alt, "XMP"

        # Prioridade 2: EXIF DMS
        lat = self._extract_gps_decimal_from_dms(
            merged_payload.get("GPSLatitude"),
            merged_payload.get("GPSLatitudeRef"),
        )
        lon = self._extract_gps_decimal_from_dms(
            merged_payload.get("GPSLongitude"),
            merged_payload.get("GPSLongitudeRef"),
        )
        alt = self._to_float(merged_payload.get("GPSAltitude"))
        if lat is not None and lon is not None:
            return lat, lon, alt, "EXIF"

        return None, None, alt, "NONE"

    @staticmethod
    def _date_name_from_payload(payload: Dict[str, Any]) -> str:
        raw = payload.get("DateTimeOriginal") or payload.get("DateTime")
        if not raw:
            return ""
        text = str(raw).strip()
        for fmt in ("%Y:%m:%d %H:%M:%S", "%Y-%m-%d %H:%M:%S"):
            try:
                return datetime.strptime(text, fmt).strftime("%Y%m%d")
            except Exception:
                pass
        return ""

    def _list_photo_files(self, base_folder: str, recursive: bool) -> List[str]:
        output = []
        if not os.path.isdir(base_folder):
            return output

        if recursive:
            walker = os.walk(base_folder)
            for root, _, files in walker:
                for name in files:
                    if name.lower().endswith((".jpg", ".jpeg")):
                        output.append(os.path.join(root, name))
        else:
            for name in os.listdir(base_folder):
                full_path = os.path.join(base_folder, name)
                if os.path.isfile(full_path) and name.lower().endswith((".jpg", ".jpeg")):
                    output.append(full_path)

        return sorted(output)

    def generate_from_folder(
        self,
        base_folder: str,
        recursive: bool = True,
        generate_report: bool = True,
        layer_name: str = "Fotos_Sem_MRK",
    ) -> Dict[str, Any]:
        if not os.path.isdir(base_folder):
            raise ValueError(f"Pasta invalida: {base_folder}")

        files = self._list_photo_files(base_folder, recursive)
        self.logger.info(
            "Iniciando vetorizacao por fotos sem MRK",
            data={"base_folder": base_folder, "recursive": recursive, "total_files": len(files)},
        )

        points = []
        raw_records = {}
        quality = {
            "total_files": len(files),
            "with_coords": 0,
            "without_coords": 0,
            "with_xmp": 0,
            "with_exif_gps": 0,
            "missing_xmp_and_exif": 0,
        }
        x_geom_key = MetadataFields.resolve_output_name("Lon")
        y_geom_key = MetadataFields.resolve_output_name("Lat")

        for file_path in files:
            os_payload = ExifUtil.extract_metadata_os(file_path, tool_key=self.tool_key)
            exif_payload = ExifUtil.extract_metadata_exif(file_path, tool_key=self.tool_key)
            xmp_payload = XmpUtil.extract_metadata(file_path, tool_key=self.tool_key)

            merged = {}
            merged.update(os_payload)
            merged.update(exif_payload)
            merged.update(xmp_payload)

            has_xmp = str(merged.get("xmp_encontrado", "nao")).lower() == "sim"
            if has_xmp:
                quality["with_xmp"] += 1
            has_exif_gps = bool(merged.get("GPSLatitude") and merged.get("GPSLongitude"))
            if has_exif_gps:
                quality["with_exif_gps"] += 1

            lat, lon, alt, source = self._extract_position(merged)
            if source == "NONE":
                quality["without_coords"] += 1
                if (not has_xmp) and (not has_exif_gps):
                    quality["missing_xmp_and_exif"] += 1
            else:
                quality["with_coords"] += 1

            canonical = MetadataFields.normalize_record_to_keys(merged)
            canonical["Lat"] = lat
            canonical["Lon"] = lon
            canonical["Alt"] = alt
            canonical["DateName"] = self._date_name_from_payload(canonical)
            canonical["MrkFolder"] = base_folder
            canonical["CoordSource"] = source
            canonical["HasXmp"] = has_xmp
            canonical["HasExifGps"] = has_exif_gps
            canonical["QualityFlag"] = "LOW" if source == "NONE" else "OK"

            file_key = os.path.basename(file_path)
            raw_records[file_key] = canonical

            if lat is None or lon is None:
                continue

            output_record = MetadataFields.map_record_to_output_attributes(canonical)
            # Garantir chaves de geometria exatamente no nome esperado pela camada.
            output_record[x_geom_key] = lon
            output_record[y_geom_key] = lat
            output_record["CoordSource"] = source
            output_record["HasXmp"] = "True" if has_xmp else "False"
            output_record["HasExifGps"] = "True" if has_exif_gps else "False"
            output_record["QualityFlag"] = canonical["QualityFlag"]
            points.append(output_record)

        schema = []
        if points:
            sample = points[0]
            for key, value in sample.items():
                if key in ("Lat", "Lon"):
                    continue
                if isinstance(value, (int, float)):
                    qtype = QVariant.Double
                else:
                    qtype = QVariant.String
                schema.append((key, qtype, key))

        # Campos de diagnostico garantidos
        for extra_name, qtype in (
            ("CoordSource", QVariant.String),
            ("HasXmp", QVariant.String),
            ("HasExifGps", QVariant.String),
            ("QualityFlag", QVariant.String),
        ):
            if extra_name not in [s[2] for s in schema]:
                schema.append((extra_name, qtype, extra_name))

        layer = None
        if points:
            layer = VectorLayerGeometry.create_point_layer_from_dicts(
                points=points,
                name=layer_name,
                field_specs=schema,
                geometry_keys=(x_geom_key, y_geom_key),
                tool_key=self.tool_key,
            )
            if layer and layer.isValid():
                QgsProject.instance().addMapLayer(layer)

        full_dump_payload = {
            "base_folder": base_folder,
            "recursive": recursive,
            "points_total": len(points),
            "quality": quality,
            "groups": {
                base_folder: {
                    "points": len(points),
                    "indexed": len(raw_records),
                    "raw_records": raw_records,
                }
            },
        }

        json_path = ExplorerUtils.create_temp_json(
            full_dump_payload,
            tool_key=self.tool_key,
            prefix="photo_folder_metadata",
            subfolder=os.path.join(
                ExplorerUtils.REPORTS_TEMP_FOLDER,
                ExplorerUtils.REPORTS_JSON_FOLDER,
            ),
            file_stem_hint=ExplorerUtils.build_report_json_stem(
                base_folder=base_folder,
                points_total=len(points),
            ),
        )

        report_payload = None
        if generate_report and json_path:
            report_payload = ReportGenerationService(tool_key=self.tool_key).generate_from_json(
                json_path
            )

        if quality["with_coords"] == 0:
            self.logger.warning(
                "Nenhuma foto com coordenada valida encontrada",
                data={"quality": quality, "base_folder": base_folder},
            )

        payload = {
            "layer": layer,
            "json_path": json_path,
            "report_payload": report_payload,
            "quality": quality,
            "total_points": len(points),
            "total_files": len(files),
        }
        self.logger.info("Vetorizacao sem MRK concluida", data=payload)
        return payload
