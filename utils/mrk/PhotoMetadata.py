# -*- coding: utf-8 -*-
import os
import re
from datetime import datetime

from qgis.PyQt.QtCore import QVariant

from ...core.config.LogUtils import LogUtils
from ..ExplorerUtils import ExplorerUtils
from ..ToolKeys import ToolKey
from .CustomPhotosFieldsUtil import CustomPhotosFieldsUtil
from .ExifUtil import ExifUtil
from .MetadataFields import MetadataFields
from .XmpUtil import XmpUtil

TOOL_KEY = ToolKey.DRONE_COORDINATES


class PhotoMetadata:
    """Manager de metadata de fotos para o fluxo DroneCoordinates."""

    # Mantido para compatibilidade com chamadas existentes.
    FIELDS_PHOTO = {
        "nome_arq": QVariant.String,
        "tam_mb": QVariant.Double,
        "tipo_arq": QVariant.String,
        "dt_criacao": QVariant.String,
        "dt_full": QVariant.String,
        "dt_date": QVariant.String,
        "dt_time": QVariant.String,
        "cam_model": QVariant.String,
        "bit_depth": QVariant.Int,
        "larg_px": QVariant.Int,
        "alt_px": QVariant.Int,
        "res_h_dpi": QVariant.Double,
        "res_v_dpi": QVariant.Double,
        "focal_mm": QVariant.Double,
        "focal35mm": QVariant.Int,
        "iso": QVariant.Int,
        "abert_f": QVariant.Double,
    }

    DJI_RE = re.compile(r"_(\d{4})_[A-Z]\.JPG$", re.IGNORECASE)

    @staticmethod
    def _safe_parse_datetime(value):
        if not value:
            return None
        candidates = [
            ("%Y:%m:%d %H:%M:%S", value),
            ("%Y-%m-%d %H:%M:%S", value),
        ]
        for fmt, raw in candidates:
            try:
                return datetime.strptime(str(raw), fmt)
            except Exception:
                pass
        return None

    @staticmethod
    def _get_logger(tool_key: str = TOOL_KEY) -> LogUtils:
        return LogUtils(tool=tool_key, class_name="PhotoMetadata")

    @staticmethod
    def _format_dates(dt: datetime) -> dict:
        return {
            "dt_criacao": dt.strftime("%Y-%m-%d %H:%M:%S"),
            "dt_full": dt.strftime("%Y%m%d%H%M"),
            "dt_date": dt.strftime("%Y%m%d"),
            "dt_time": dt.strftime("%H%M"),
        }

    @staticmethod
    def _extract_flight_context(point: dict) -> dict:
        return {
            "FlightNumber": point.get("numdovoo"),
            "FlightName": point.get("nomedovoo"),
            "FolderLevel1": point.get("pasta1"),
            "FolderLevel2": point.get("pasta2"),
            # Mantem legado MRK acessivel
            "numdovoo": point.get("numdovoo"),
            "nomedovoo": point.get("nomedovoo"),
            "pasta1": point.get("pasta1"),
            "pasta2": point.get("pasta2"),
            "mrk_file": point.get("mrk_file"),
            "mrk_path": point.get("mrk_path"),
            "mrk_folder": point.get("mrk_folder"),
            "data_name": point.get("data_name"),
            "lat": point.get("lat"),
            "lon": point.get("lon"),
            "alt": point.get("alt"),
        }

    @staticmethod
    def _build_selected_keys(
        selected_required_fields=None,
        selected_custom_fields=None,
        selected_mrk_fields=None,
    ) -> set:
        return set(selected_required_fields or []) | set(selected_custom_fields or []) | set(
            selected_mrk_fields or []
        )

    @staticmethod
    def _filter_payload(payload: dict, selected_keys: set) -> dict:
        if not selected_keys:
            return payload
        return {key: value for key, value in payload.items() if key in selected_keys}

    @staticmethod
    def _extract_photo_payload(image_path: str, tool_key: str = TOOL_KEY) -> dict:
        logger = PhotoMetadata._get_logger(tool_key)

        os_data = ExifUtil.extract_metadata_os(image_path, tool_key=tool_key)
        image_data = ExifUtil.extract_metadata_image(image_path, tool_key=tool_key)
        exif_data = ExifUtil.extract_metadata_exif(image_path, tool_key=tool_key)
        xmp_data = XmpUtil.extract_metadata(image_path, tool_key=tool_key)

        payload = {}
        payload.update(os_data)
        payload.update(image_data)
        payload.update(exif_data)
        payload.update(xmp_data)

        # Aliases criticos para compatibilidade com campos esperados no calculo custom.
        alias_map = {
            "drone-dji:AltitudeType": "AltitudeType",
            "drone-dji:AbsoluteAltitude": "AbsoluteAltitude",
            "drone-dji:RelativeAltitude": "RelativeAltitude",
            "drone-dji:GimbalRollDegree": "GimbalRollDegree",
            "drone-dji:GimbalYawDegree": "GimbalYawDegree",
            "drone-dji:GimbalPitchDegree": "GimbalPitchDegree",
            "drone-dji:FlightRollDegree": "FlightRollDegree",
            "drone-dji:FlightYawDegree": "FlightYawDegree",
            "drone-dji:FlightPitchDegree": "FlightPitchDegree",
            "drone-dji:FlightXSpeed": "FlightXSpeed",
            "drone-dji:FlightYSpeed": "FlightYSpeed",
            "drone-dji:FlightZSpeed": "FlightZSpeed",
            "drone-dji:RtkFlag": "RtkFlag",
            "drone-dji:RtkStdLon": "RtkStdLon",
            "drone-dji:RtkStdLat": "RtkStdLat",
            "drone-dji:RtkStdHgt": "RtkStdHgt",
            "drone-dji:RtkDiffAge": "RtkDiffAge",
            "drone-dji:DewarpFlag": "DewarpFlag",
            "drone-dji:ShutterCount": "ShutterCount",
            "drone-dji:FocusDistance": "FocusDistance",
            "drone-dji:CameraSerialNumber": "CameraSerialNumber",
            "drone-dji:DroneSerialNumber": "DroneSerialNumber",
            "drone-dji:DroneModel": "DroneModel",
            "drone-dji:CaptureUUID": "CaptureUUID",
            "drone-dji:PictureQuality": "PictureQuality",
            "drone-dji:UTCAtExposure": "UTCAtExposure",
            "drone-dji:SensorTemperature": "SensorTemperature",
            "drone-dji:LensTemperature": "LensTemperature",
            "drone-dji:SensorFPS": "SensorFPS",
            "drone-dji:LensPosition": "LensPosition",
            "drone-dji:LRFStatus": "LRFStatus",
            "drone-dji:LRFTargetDistance": "LRFTargetDistance",
            "drone-dji:LRFTargetLon": "LRFTargetLon",
            "drone-dji:LRFTargetLat": "LRFTargetLat",
            "drone-dji:LRFTargetAlt": "LRFTargetAlt",
            "drone-dji:LRFTargetAbsAlt": "LRFTargetAbsAlt",
            "drone-dji:WhiteBalanceCCT": "WhiteBalanceCCT",
            "drone-dji:GpsStatus": "GpsStatus",
        }
        for source_key, target_key in alias_map.items():
            if target_key not in payload and source_key in payload:
                payload[target_key] = payload.get(source_key)

        # Mapeamento dinamico por sufixo para normalizados XMP/EXIF (ex.: "EXIF:GPSInfo:GPSMapDatum" -> "GPSMapDatum")
        required_by_suffix = {}
        for key, spec in MetadataFields.REQUIRED_FIELDS.items():
            normalized = str(spec.get("normalized", ""))
            if ":" in normalized:
                required_by_suffix[normalized.split(":")[-1]] = key

        for source_key, source_val in list(payload.items()):
            source_str = str(source_key)
            source_suffix = source_str.split(":")[-1]
            target_key = required_by_suffix.get(source_suffix)
            if target_key and target_key not in payload:
                payload[target_key] = source_val

        # Campos solicitados no novo padrao
        payload["FileType"] = os.path.splitext(image_path)[1].upper()

        # dt_* deve priorizar metadado da foto (DateTimeOriginal), com fallback para os_date.
        dt = PhotoMetadata._safe_parse_datetime(payload.get("DateTimeOriginal"))
        if dt is None:
            dt = PhotoMetadata._safe_parse_datetime(os_data.get("os_date"))
        if dt is not None:
            payload.update(PhotoMetadata._format_dates(dt))
        else:
            logger.debug(f"Falha ao obter datetime para dt_* em {image_path}")

        return payload

    @staticmethod
    def _index_photos_complete(
        base_folder: str,
        recursive: bool,
        tool_key: str = TOOL_KEY,
    ) -> tuple:
        logger = PhotoMetadata._get_logger(tool_key)

        photo_files = []
        walker = os.walk(base_folder) if recursive else [(base_folder, [], os.listdir(base_folder))]
        for root, _, files in walker:
            for fname in files:
                if not fname.lower().endswith(".jpg"):
                    continue
                if not PhotoMetadata.DJI_RE.search(fname):
                    continue
                photo_files.append(os.path.join(root, fname))

        raw_by_file = {}
        indexed_by_number = {}
        raw_dump_records = []

        for file_path in photo_files:
            fname = os.path.basename(file_path)
            seq_match = PhotoMetadata.DJI_RE.search(fname)
            if not seq_match:
                continue
            seq = seq_match.group(1)

            payload = PhotoMetadata._extract_photo_payload(file_path, tool_key=tool_key)
            raw_by_file[fname] = payload
            raw_dump_records.append(payload)
            indexed_by_number[seq] = payload

        # Tenta enriquecer com campos custom quando o dataset possui base minima.
        try:
            required_for_custom = [
                "DateTimeOriginal",
                "AbsoluteAltitude",
                "FlightXSpeed",
                "FlightYSpeed",
                "FlightZSpeed",
                "GimbalYawDegree",
                "FlightYawDegree",
                "GimbalPitchDegree",
                "FlightPitchDegree",
            ]
            missing_summary = {}
            for _, payload in raw_by_file.items():
                for req_key in required_for_custom:
                    if payload.get(req_key) in (None, ""):
                        missing_summary[req_key] = missing_summary.get(req_key, 0) + 1
            if missing_summary:
                logger.debug(
                    "Campos ausentes antes do calculo custom",
                    data={"missing_summary": missing_summary},
                )

            custom_enriched = CustomPhotosFieldsUtil.calculate_all_custom_fields(
                raw_by_file,
                tool_key=tool_key,
            )
            for fname, payload in custom_enriched.items():
                seq_match = PhotoMetadata.DJI_RE.search(fname)
                if not seq_match:
                    continue
                indexed_by_number[seq_match.group(1)] = payload
        except Exception as exc:
            logger.warning(
                f"Falha ao calcular CUSTOM_FIELDS para pasta {base_folder}: {exc}"
            )

        logger.info(
            "Indexacao completa de fotos finalizada",
            data={
                "base_folder": base_folder,
                "total_photos": len(photo_files),
                "indexed_keys": len(indexed_by_number),
            },
        )
        return indexed_by_number, raw_dump_records

    @staticmethod
    def enrich(
        points,
        base_folder,
        recursive=True,
        mrk_folder=None,
        selected_required_fields=None,
        selected_custom_fields=None,
        selected_mrk_fields=None,
    ):
        logger = PhotoMetadata._get_logger(TOOL_KEY)
        selected_keys = PhotoMetadata._build_selected_keys(
            selected_required_fields=selected_required_fields,
            selected_custom_fields=selected_custom_fields,
            selected_mrk_fields=selected_mrk_fields,
        )

        logger.info(
            "Iniciando enriquecimento de metadados de fotos",
            code="PHOTO_ENRICH_START",
            data={
                "base_folder": base_folder,
                "recursive": recursive,
                "mrk_folder": mrk_folder,
                "total_points": len(points),
                "selected_keys_count": len(selected_keys),
                "selected_keys_sample": sorted(list(selected_keys))[:20],
            },
        )

        points_by_folder = {}
        for point in points:
            folder = point.get("mrk_folder") or base_folder
            if folder and not os.path.isabs(folder) and base_folder:
                candidate = os.path.join(base_folder, folder)
                if os.path.isdir(candidate):
                    folder = candidate
            if folder and not os.path.isdir(folder) and base_folder:
                folder = base_folder
            points_by_folder.setdefault(folder, []).append(point)

        full_dump_payload = {
            "base_folder": base_folder,
            "recursive": recursive,
            "points_total": len(points),
            "groups": {},
        }

        total_found = 0
        total_missing = 0

        for folder, folder_points in points_by_folder.items():
            photo_index, raw_records = PhotoMetadata._index_photos_complete(
                folder,
                recursive=False,
                tool_key=TOOL_KEY,
            )

            full_dump_payload["groups"][folder] = {
                "points": len(folder_points),
                "indexed": len(photo_index),
                "raw_records": raw_records,
            }
            sample_keys = sorted(list(raw_records[0].keys()))[:40] if raw_records else []
            logger.debug(
                "Grupo indexado",
                data={
                    "folder": folder,
                    "points_count": len(folder_points),
                    "indexed_count": len(photo_index),
                    "sample_keys": sample_keys,
                },
            )

            empty_filtered = 0
            for point in folder_points:
                foto = point.get("foto")
                if foto is None:
                    continue

                key = f"{int(foto):04d}"
                photo_payload = photo_index.get(key)
                if not photo_payload:
                    total_missing += 1
                    continue

                total_found += 1
                merged_payload = {}
                merged_payload.update(photo_payload)
                merged_payload.update(PhotoMetadata._extract_flight_context(point))

                filtered_payload = PhotoMetadata._filter_payload(merged_payload, selected_keys)
                if selected_keys and not filtered_payload:
                    empty_filtered += 1
                point.update(filtered_payload)

            if selected_keys:
                logger.info(
                    "Resumo filtro grupo",
                    data={
                        "folder": folder,
                        "selected_keys_count": len(selected_keys),
                        "points_without_filtered_fields": empty_filtered,
                    },
                )

        dump_path = ExplorerUtils.create_temp_json(
            full_dump_payload,
            tool_key=TOOL_KEY,
            prefix="drone_photo_metadata_full",
        )

        logger.info(
            "Enriquecimento concluido",
            code="PHOTO_ENRICH_COMPLETE",
            data={
                "total_points": len(points),
                "matched": total_found,
                "not_found": total_missing,
                "json_dump_path": dump_path,
            },
        )

        return points
