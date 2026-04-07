# -*- coding: utf-8 -*-
"""Manager legado de metadata de fotos (mantido para compatibilidade)."""

import os
from typing import Dict, List, Union

from ...core.config.LogUtils import LogUtils
from ..ToolKeys import ToolKey
from .CustomPhotosFieldsUtil import CustomPhotosFieldsUtil
from .ExifUtil import ExifUtil
from .XmpUtil import XmpUtil


class Manager:
    """Coordena extração de metadados EXIF/XMP (legado)."""

    IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".tif", ".tiff")

    def __init__(self, tool_key: str = ToolKey.DRONE_COORDINATES):
        self.tool_key = tool_key
        self.logger = LogUtils(tool=tool_key, class_name="OBSOLETManager")

    @classmethod
    def _is_image_file(cls, path: str) -> bool:
        return os.path.isfile(path) and path.lower().endswith(cls.IMAGE_EXTENSIONS)

    @classmethod
    def _list_image_files(cls, folder_path: str) -> List[str]:
        result = []
        for entry in sorted(os.listdir(folder_path)):
            full_path = os.path.join(folder_path, entry)
            if os.path.isfile(full_path) and entry.lower().endswith(cls.IMAGE_EXTENSIONS):
                result.append(full_path)
        return result

    @staticmethod
    def _get_exif_full_value(exif_data: Dict[str, object], normalized: str) -> object:
        if not isinstance(exif_data, dict):
            return None

        if normalized.startswith("EXIF:GPSInfo:"):
            gps_key = normalized.split(":", 2)[-1]
            gps_info = exif_data.get("GPSInfo")
            if isinstance(gps_info, dict):
                return gps_info.get(gps_key)
            return None

        key = normalized.split(":")[-1]
        return exif_data.get(key)

    @staticmethod
    def _get_xmp_full_value(xmp_data: Dict[str, object], normalized: str) -> object:
        if not isinstance(xmp_data, dict):
            return None

        if normalized.startswith("xmp_bloco_1:"):
            key = normalized.split(":", 1)[-1]
            return xmp_data.get(key) or xmp_data.get(f"xmp_bloco_1:{key}")

        if ":" in normalized and not normalized.startswith("EXIF:"):
            return xmp_data.get(normalized)

        return xmp_data.get(normalized)

    def _collect_required_fields(
        self,
        os_data: Dict[str, object],
        image_data: Dict[str, object],
        exif_data: Dict[str, object],
        xmp_data: Dict[str, object],
        fields_dict: Dict[str, Dict[str, object]],
    ) -> Dict[str, object]:
        output = {}

        for key, meta in fields_dict.items():
            normalized = str(meta.get("normalized", ""))

            value = os_data.get(key)
            if value is None:
                value = image_data.get(key)
            if value is None:
                value = exif_data.get(key)
            if value is None:
                value = xmp_data.get(key)

            if value is None and normalized.startswith("EXIF:"):
                value = self._get_exif_full_value(exif_data, normalized)

            if value is None and normalized.startswith("xmp_bloco_1:"):
                value = self._get_xmp_full_value(xmp_data, normalized)

            if value is None:
                std_key = normalized.split(":")[-1]
                value = exif_data.get(std_key, xmp_data.get(std_key))

            output[key] = value

        return output

    def collect_metadata_from_image(
        self, image_path: str, fields_dict: Dict[str, Dict[str, object]]
    ) -> Dict[str, object]:
        os_data = ExifUtil.extract_metadata_os(image_path, tool_key=self.tool_key)
        image_data = ExifUtil.extract_metadata_image(image_path, tool_key=self.tool_key)
        exif_data = ExifUtil.extract_metadata_exif(image_path, tool_key=self.tool_key)
        xmp_data = XmpUtil.extract_metadata(image_path, tool_key=self.tool_key)

        required = self._collect_required_fields(
            os_data,
            image_data,
            exif_data,
            xmp_data,
            fields_dict,
        )
        required["path"] = os_data.get("path", image_path)
        return required

    def collect_metadata(
        self,
        item_path: str,
        fields_dict: Dict[str, Dict[str, object]],
        compute_custom: bool = False,
    ) -> Union[Dict[str, object], Dict[str, Dict[str, object]]]:
        if os.path.isdir(item_path):
            images = self._list_image_files(item_path)
            result = {}
            for img_path in images:
                metadata = self.collect_metadata_from_image(img_path, fields_dict)
                key = metadata.get("file")
                if key:
                    result[key] = metadata
            if compute_custom:
                result = CustomPhotosFieldsUtil.calculate_all_custom_fields(
                    result, tool_key=self.tool_key
                )
            return result

        if self._is_image_file(item_path):
            metadata = self.collect_metadata_from_image(item_path, fields_dict)
            if compute_custom:
                return CustomPhotosFieldsUtil.calculate_all_custom_fields(
                    {metadata.get("file", os.path.basename(item_path)): metadata},
                    tool_key=self.tool_key,
                )
            return metadata

        self.logger.warning(f"Caminho invalido para coleta de metadata: {item_path}")
        return {}
