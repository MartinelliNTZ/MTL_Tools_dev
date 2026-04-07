from typing import Dict, List, Any


class StringAdapter:
    """Adapta dicionários de metacampos para saída mínima de UI."""

    @staticmethod
    def to_key_label_description(fields_dict: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Recebe um dicionário no formato de Strings.REQUIRED_FIELDS/CUSTOM_FIELDS
        e retorna uma lista contendo somente key, label e description.
        """
        if not isinstance(fields_dict, dict):
            return []

        output: List[Dict[str, Any]] = []
        for key, meta in fields_dict.items():
            meta = meta if isinstance(meta, dict) else {}
            output.append(
                {
                    "key": key,
                    "label": meta.get("label"),
                    "description": meta.get("description"),
                }
            )
        return output

