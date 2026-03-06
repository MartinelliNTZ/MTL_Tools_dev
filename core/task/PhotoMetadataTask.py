# -*- coding: utf-8 -*-
from typing import Optional, Dict, Any
from qgis.core import QgsProject

from .BaseTask import BaseTask
from ..config.LogUtilsNew import LogUtilsNew
from ...utils.mrk.photo_metadata import PhotoMetadata


class PhotoMetadataTask(BaseTask):
    """Task que cruza metadados de fotos com atributos de uma camada de pontos."""

    def __init__(
        self,
        layer_id: str,
        base_folder: str,
        recursive: bool,
        tool_key: str,
    ):
        super().__init__("Cruzando fotos", tool_key)
        self.layer_id = layer_id
        self.base_folder = base_folder
        self.recursive = recursive

    def _run(self) -> bool:
        if self.isCanceled():
            return False

        layer = QgsProject.instance().mapLayer(self.layer_id)
        if not layer or not layer.isValid():
            raise RuntimeError("Camada não encontrada para cruzamento de metadados")

        # Extrair lista de fotos a serem cruzadas (campo 'foto')
        pontos = []
        for feat in layer.getFeatures():
            foto = feat.attribute("foto")
            if foto is None:
                continue
            try:
                foto_int = int(foto)
            except Exception:
                continue
            pontos.append({"foto": foto_int})

        # Cruzar metadados
        enriched = PhotoMetadata.enrich(
            pontos,
            base_folder=self.base_folder,
            recursive=self.recursive,
        )

        updates = {}
        field_names = set()
        for item in enriched:
            foto = item.get("foto")
            if foto is None:
                continue
            data = {k: v for k, v in item.items() if k != "foto"}
            updates[int(foto)] = data
            field_names.update(data.keys())

        logger = LogUtilsNew(tool=self.tool_key, class_name=self.__class__.__name__)
        logger.debug(
            f"Cruzamento completo: {len(pontos)} fotos processadas, {len(updates)} atualizações geradas"
        )

        # Diagnóstico adicional para identificar fotos que não foram encontradas
        not_found = len(pontos) - len(updates)
        if not_found > 0:
            logger.debug(f"Fotos sem metadados encontrados: {not_found}")

        self.result = {
            "updates": updates,
            "field_names": list(field_names),
        }
        return True
