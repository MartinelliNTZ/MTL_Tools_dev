from typing import Dict, List, Any
from dataclasses import is_dataclass


class StringAdapter:
    """Adapta dicionários de metacampos para saída mínima de UI."""

    @staticmethod
    def to_key_label_description(fields_dict: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Recebe um dicionário no formato de Strings.REQUIRED_FIELDS/CUSTOM_FIELDS
        e retorna uma lista contendo somente key, label e description.
        """
        if not isinstance(fields_dict, dict):
            return []

        output: List[Dict[str, Any]] = []
        for key, meta in fields_dict.items():
            if isinstance(meta, dict):
                label = meta.get("label")
                description = meta.get("description")
            elif is_dataclass(meta):
                label = getattr(meta, "label", None)
                description = getattr(meta, "description", None)
            else:
                label = None
                description = None
            output.append(
                {
                    "key": key,
                    "label": label,
                    "description": description,
                }
            )
        return output
