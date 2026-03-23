# -*- coding: utf-8 -*-
import os

from ...i18n.TranslationManager import STR


class MrkDropHandler:
    """Helpers puros para o fluxo de importacao de arquivos MRK."""

    MRK_EXTENSIONS = {".mrk"}

    @staticmethod
    def is_mrk_file(path: str) -> bool:
        if not path:
            return False
        _, ext = os.path.splitext(path)
        return ext.lower() in MrkDropHandler.MRK_EXTENSIONS

    @staticmethod
    def build_output_paths(file_path: str) -> tuple[str, str]:
        folder = os.path.dirname(file_path)
        base_name = os.path.splitext(os.path.basename(file_path))[0]

        points_name = f"{base_name}_{STR.MRK_POINTS_SUFFIX}.gpkg"
        track_name = f"{base_name}_{STR.MRK_TRACK_SUFFIX}.gpkg"

        return (
            os.path.join(folder, points_name),
            os.path.join(folder, track_name),
        )
