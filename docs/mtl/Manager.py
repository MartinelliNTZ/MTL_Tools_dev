# -*- coding: utf-8 -*-
"""
Manager que orquestra a extração de metadados Exif e XMP.

O objetivo é manter a lógica de coordenação separada das utilidades específicas
(XmpUtil e ExifUtil), permitindo testabilidade e uso simples em um script.
"""
import os
from typing import Dict, List, Union

from ExifUtil import ExifUtil
from Strings import Strings
from XmpUtil import XmpUtil


class Manager:
    """Coordena as duas utilidades de metadados (EXIF e XMP)."""

    IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".tif", ".tiff")

    @staticmethod
    def _is_image_file(path: str) -> bool:
        """Verifica se um caminho corresponde a extensão de imagem conhecida."""
        return os.path.isfile(path) and path.lower().endswith(Manager.IMAGE_EXTENSIONS)

    @staticmethod
    def _list_image_files(folder_path: str) -> List[str]:
        """Retorna a lista de arquivos de imagem em um diretório (não-recursivo)."""
        result = []
        for entry in sorted(os.listdir(folder_path)):
            full_path = os.path.join(folder_path, entry)
            if os.path.isfile(full_path) and entry.lower().endswith(Manager.IMAGE_EXTENSIONS):
                result.append(full_path)
        return result

    @staticmethod
    def _get_exif_full_value(exif_data: Dict[str, object], normalized: str) -> object:
        """Resolve valores EXIF, incluindo GPSInfo aninhado, usando o normalized path."""
        if not isinstance(exif_data, dict):
            return None

        if normalized.startswith("EXIF:GPSInfo:"):
            gps_key = normalized.split(":", 2)[-1]
            gps_info = exif_data.get("GPSInfo")
            if isinstance(gps_info, dict):
                return gps_info.get(gps_key)
            return None

        # Ex: EXIF:Model -> Model
        key = normalized.split(":")[-1]
        return exif_data.get(key)

    @staticmethod
    def _get_xmp_full_value(xmp_data: Dict[str, object], normalized: str) -> object:
        """Resolve valores XMP a partir da chave normalizada."""
        if not isinstance(xmp_data, dict):
            return None

        # A chave pode ser xmp_bloco_1:drone-dji:AltitudeType -> drone-dji:AltitudeType
        if normalized.startswith("xmp_bloco_1:"):
            key = normalized.split(":", 1)[-1]
            return xmp_data.get(key) or xmp_data.get(f"xmp_bloco_1:{key}")

        # Também há casos diretos no XmpUtil (drone-dji:<campo>)
        if ":" in normalized and not normalized.startswith("EXIF:"):
            key = normalized
            return xmp_data.get(key)

        return xmp_data.get(normalized)

    @staticmethod
    def _collect_required_fields(os_data: Dict[str, object], image_data: Dict[str, object], exif_data: Dict[str, object], xmp_data: Dict[str, object]) -> Dict[str, object]:
        """Retorna dicionário contendo apenas os campos de REQUIRED_FIELDS."""
        output = {}

        for key, meta in Strings.REQUIRED_FIELDS.items():
            normalized = meta.get("normalized", "")

            # prioridade de busca: os, image, exif, xmp
            value = os_data.get(key)
            if value is None:
                value = image_data.get(key)
            if value is None:
                value = exif_data.get(key)
            if value is None:
                value = xmp_data.get(key)

            if value is None and normalized.startswith("EXIF:"):
                value = Manager._get_exif_full_value(exif_data, normalized)

            if value is None and normalized.startswith("xmp_bloco_1:"):
                value = Manager._get_xmp_full_value(xmp_data, normalized)

            if value is None:
                # tenta encontrar no dicionário por nome de atributo completo
                std_key = normalized.split(":")[-1]
                value = exif_data.get(std_key, xmp_data.get(std_key))

            output[key] = value

        return output

    @staticmethod
    def collect_metadata_from_image(image_path: str) -> Dict[str, object]:
        """Extrai metadados de imagem usando ExifUtil e XmpUtil e aplica filtro REQUIRED_FIELDS."""
        os_data = ExifUtil.extract_metadata_os(image_path)
        image_data = ExifUtil.extract_metadata_image(image_path)
        exif_data = ExifUtil.extract_metadata_exif(image_path)
        xmp_data = XmpUtil.extract_metadata(image_path)

        required = Manager._collect_required_fields(os_data, image_data, exif_data, xmp_data)

        # inclui sempre o caminho de origem no retorno final
        required["path"] = os_data.get("path", image_path)

        return required

    @classmethod
    def collect_metadata(cls, item_path: str) -> Union[Dict[str, object], Dict[str, Dict[str, object]]]:
        """Orquestra a extração de metadados por caminho de arquivo ou diretório."""
        if os.path.isdir(item_path):
            images = cls._list_image_files(item_path)
            result = {}
            for img_path in images:
                metadata = cls.collect_metadata_from_image(img_path)
                key = metadata.get("file")
                if key:
                    result[key] = metadata
            return result

        if cls._is_image_file(item_path):
            return cls.collect_metadata_from_image(item_path)

        raise ValueError(f"Caminho inválido ou não é imagem: {item_path}")


if __name__ == "__main__":
    print("Manager disponível para uso via importação, execute pelo main.py")
