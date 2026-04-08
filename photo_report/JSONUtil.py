import json
from pathlib import Path
from typing import Any, Dict, List

from .MetadataFields import MetadataFields
from .StringAdapter import StringAdapter


class JSONUtil:
    """Responsavel por leitura e normalizacao dos JSONs de metadata."""

    @staticmethod
    def _normalize_record(
        record: Dict[str, Any],
        *,
        group_path: str = "",
        file_key: str = "",
    ) -> Dict[str, Any]:
        """Normaliza um registro bruto para o formato canonico baseado em MetadataFields."""
        if not isinstance(record, dict):
            return {}

        normalized = MetadataFields.normalize_record_to_keys(record)

        catalog = MetadataFields.all_fields()
        known_keys = StringAdapter.filter_known_keys(normalized.keys(), catalog)
        out = {key: normalized.get(key) for key in known_keys}

        # Preserva campos extras nao catalogados (pipeline custom pode gerar campos novos).
        for key, value in normalized.items():
            if key not in out:
                out[key] = value

        if out.get("File") in (None, "") and file_key:
            out["File"] = file_key
        if out.get("Path") in (None, "") and file_key:
            out["Path"] = str(Path(group_path) / file_key) if group_path else file_key

        return out

    @staticmethod
    def load_json_file(json_path: str) -> Any:
        """Le um arquivo JSON do disco e retorna o objeto desserializado."""
        path = Path(json_path)
        if not path.exists():
            raise FileNotFoundError(f"JSON nao encontrado: {json_path}")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def load_records(json_path: str = "metadata_completa_custom.json") -> List[Dict[str, Any]]:
        """Carrega registros de metadata suportando formato json2 e formato legado."""
        data = JSONUtil.load_json_file(json_path)

        if isinstance(data, dict) and isinstance(data.get("groups"), dict):
            images: List[Dict[str, Any]] = []
            total_raw = 0
            for group_path, group_payload in data["groups"].items():
                raw_records = (group_payload or {}).get("raw_records", {})
                if not isinstance(raw_records, dict):
                    continue
                total_raw += len(raw_records)
                for file_key, raw_record in raw_records.items():
                    images.append(
                        JSONUtil._normalize_record(
                            raw_record,
                            group_path=group_path,
                            file_key=file_key,
                        )
                    )
            print(f"Carregadas {len(images)} imagens de json2 (raw_records={total_raw})")
            return images

        if isinstance(data, dict):
            images: List[Dict[str, Any]] = []
            for file_key, record in data.items():
                if isinstance(record, dict):
                    images.append(JSONUtil._normalize_record(record, file_key=file_key))
            print(f"Carregadas {len(images)} imagens de {len(data)} chaves")
            return images

        raise ValueError(f"Formato JSON nao suportado em {json_path}")
