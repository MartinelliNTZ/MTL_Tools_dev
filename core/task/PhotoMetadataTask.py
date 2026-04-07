# -*- coding: utf-8 -*-
from qgis.core import QgsProject

from .BaseTask import BaseTask
from ..config.LogUtils import LogUtils
from ...utils.mrk.PhotoMetadata import PhotoMetadata


class PhotoMetadataTask(BaseTask):
    """Task que cruza metadados de fotos com atributos de uma camada de pontos."""

    def __init__(
        self,
        layer_id: str,
        base_folder: str,
        recursive: bool,
        selected_required_fields: list,
        selected_custom_fields: list,
        selected_mrk_fields: list,
        tool_key: str,
    ):
        super().__init__("Cruzando fotos", tool_key)
        self.layer_id = layer_id
        self.base_folder = base_folder
        self.recursive = recursive
        self.selected_required_fields = selected_required_fields or []
        self.selected_custom_fields = selected_custom_fields or []
        self.selected_mrk_fields = selected_mrk_fields or []

    def _run(self) -> bool:
        if self.isCanceled():
            return False

        layer = QgsProject.instance().mapLayer(self.layer_id)
        if not layer or not layer.isValid():
            raise RuntimeError("Camada nÃ£o encontrada para cruzamento de metadados")

        logger = LogUtils(tool=self.tool_key, class_name=self.__class__.__name__)

        # Extrair lista de fotos a serem cruzadas (campo 'foto')
        # ðŸ”´ IMPORTANTE: TambÃ©m extrair 'mrk_folder' se disponÃ­vel (para mÃºltiplos voos)
        pontos = []

        for feat in layer.getFeatures():
            foto = feat.attribute("foto")
            if foto is None:
                continue
            try:
                foto_int = int(foto)
            except Exception:
                logger.warning(
                    f"Valor de foto nÃ£o Ã© um inteiro: {foto} na feiÃ§Ã£o ID {feat.id()}. Ignorando esta feiÃ§Ã£o."
                )
                continue

            ponto = {"foto": foto_int}

            # Carrega todos os atributos da feicao para preservar MRK_FIELDS/legado.
            # Isso garante que campos como lat/lon/mrk_* e contexto de voo cheguem ao PhotoMetadata.
            for field in feat.fields():
                name = field.name()
                if name == "foto":
                    continue
                ponto[name] = feat.attribute(name)

            # Verificar se o campo mrk_folder existe (adicionado por MrkParseTask)
            if feat.fieldNameIndex("mrk_folder") != -1:
                mrk_folder = feat.attribute("mrk_folder")
                if mrk_folder:
                    ponto["mrk_folder"] = mrk_folder

            pontos.append(ponto)

        logger.info(
            "Pontos extraÃ­dos da camada",
            data={
                "total_pontos": len(pontos),
                "com_mrk_folder": sum(1 for p in pontos if "mrk_folder" in p),
                "selected_required_fields": len(self.selected_required_fields),
                "selected_custom_fields": len(self.selected_custom_fields),
                "selected_mrk_fields": len(self.selected_mrk_fields),
            },
        )

        # Cruzar metadados
        # ðŸ”´ O mÃ©todo enrich() agora processa cada grupo de pontos separadamente
        # baseado em seu mrk_folder, evitando conflito de numeraÃ§Ã£o entre voos
        enriched = PhotoMetadata.enrich(
            pontos,
            base_folder=self.base_folder,
            recursive=self.recursive,
            selected_required_fields=self.selected_required_fields,
            selected_custom_fields=self.selected_custom_fields,
            selected_mrk_fields=self.selected_mrk_fields,
        )

        updates = {}
        field_names = set()
        for item in enriched:
            foto = item.get("foto")
            if foto is None:
                continue

            mrk_folder = str(item.get("mrk_folder", "") or "").strip()
            photo_key = (mrk_folder, int(foto))

            # NÃ£o incluir mrk_folder nos updates (Ã© apenas campo de contexto)
            data = {k: v for k, v in item.items() if k not in ("foto", "mrk_folder")}
            updates[photo_key] = data
            field_names.update(data.keys())

            # Compatibilidade legada: se cÃ¢mera nÃ£o tem mrk_folder, tambÃ©m mantemos Ã­ndice sÃ³ por foto
            if not mrk_folder:
                updates[int(foto)] = data

        # Garante criacao de colunas mesmo quando o valor venha vazio para todo o lote.
        # Isso evita "sumir" com campos selecionados no grid quando metadado nao existe na fonte.
        selected_all = (
            set(self.selected_required_fields)
            | set(self.selected_custom_fields)
            | set(self.selected_mrk_fields)
        )
        field_names.update(selected_all)

        logger.debug(
            f"Cruzamento completo: {len(pontos)} fotos processadas, {len(updates)} atualizaÃ§Ãµes geradas"
        )

        # DiagnÃ³stico adicional para identificar fotos que nÃ£o foram encontradas
        logger.debug(
            "Resumo de campos retornados da metadata",
            data={
                "field_names_count": len(field_names),
                "field_names_sample": sorted(list(field_names))[:30],
            },
        )
        not_found = len(pontos) - len(updates)
        if not_found > 0:
            logger.debug(f"Fotos sem metadados encontrados: {not_found}")

        self.result = {
            "updates": updates,
            "field_names": list(field_names),
        }
        return True
