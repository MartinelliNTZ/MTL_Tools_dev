# -*- coding: utf-8 -*-
from typing import List, Optional, Dict, Any
import os

from .BaseTask import BaseTask
from ..config.LogUtilsNew import LogUtilsNew
from ...utils.mrk.mrk_parser import MrkParser


class MrkParseTask(BaseTask):
    """Task para ler arquivos MRK e extrair pontos."""

    def __init__(
        self,
        paths: List[str],
        recursive: bool,
        merge: bool,
        extra_fields: Optional[Dict[str, Any]],
        tool_key: str,
    ):
        super().__init__("Lendo MRKs", tool_key)
        self.paths = paths
        self.recursive = recursive
        self.merge = merge
        self.extra_fields = extra_fields or {}

    def _run(self) -> bool:
        if self.isCanceled():
            return False

        LogUtilsNew(tool=self.tool_key, class_name=self.__class__.__name__).info(
            f"Iniciando leitura de MRKs (paths={self.paths}, recursive={self.recursive})"
        )

        all_points = []
        for path in self.paths:
            base = path
            if os.path.isfile(path):
                base = os.path.dirname(path)
            if not os.path.isdir(base):
                continue

            points = MrkParser.parse_folder(
                base,
                recursive=self.recursive,
                extra_fields=self.extra_fields,
            )

            if points:
                all_points.extend(points)

        self.result = {
            "points": all_points,
            "base_folder": self.paths[0] if self.paths else None,
        }
        return True
