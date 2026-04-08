from typing import Any, Dict, List, Optional
import re

from .MetadataFields import MetadataFields


def normalize_key(key: str) -> str:
    """Normaliza um nome de campo para snake_case."""
    if key is None:
        return ""
    key = re.sub(r"(?<!^)(?=[A-Z])", "_", str(key))
    key = key.replace(" ", "_").replace("-", "_").replace("/", "_")
    key = re.sub(r"_+", "_", key).strip("_")
    return key.lower()


class MetadataRecord:
    """Registro canonico de metadados por imagem com helpers tipados."""

    def __init__(self, data: Dict[str, Any]):
        """Cria um registro imutavel por convencao, com lookup normalizado de chaves."""
        self._data: Dict[str, Any] = dict(data or {})
        self._normalized_lookup: Dict[str, Any] = {
            normalize_key(k): v for k, v in self._data.items()
        }

    @staticmethod
    def _is_present(value: Any) -> bool:
        """Informa se um valor contem conteudo util para processamento."""
        if value is None:
            return False
        return str(value).strip().lower() not in {"", "none", "null", "nan"}

    @staticmethod
    def _to_float(value: Any) -> Optional[float]:
        """Converte valor para float com tratamento de entradas vazias ou invalidas."""
        if value is None:
            return None
        if isinstance(value, (int, float)):
            return float(value)
        text = str(value).strip().replace("+", "")
        if text.lower() in {"", "none", "null", "nan"}:
            return None
        try:
            return float(text)
        except ValueError:
            return None

    def get_raw(self, key: str, default: Any = None) -> Any:
        """Retorna o valor bruto armazenado para uma chave exata."""
        return self._data.get(key, default)

    def get_text(self, key: str, default: str = "") -> str:
        """Retorna um indicador como texto, aplicando valor padrao quando ausente."""
        value = self.get_indicator(key)
        if not self._is_present(value):
            return default
        return str(value)

    def get_float(self, key: str, default: Optional[float] = None) -> Optional[float]:
        """Retorna um indicador como float, aplicando valor padrao quando invalido."""
        value = self.get_indicator(key)
        num = self._to_float(value)
        return default if num is None else num

    def _first_value(self, keys: List[str]) -> Any:
        """Busca o primeiro valor disponivel entre candidatos e aliases conhecidos."""
        for key in keys:
            for candidate in MetadataFields.resolve_candidates(key):
                if candidate in self._data and self._is_present(self._data[candidate]):
                    return self._data[candidate]

                attr = MetadataFields.get_attribute(candidate)
                if attr and attr in self._data and self._is_present(self._data[attr]):
                    return self._data[attr]

            resolved = MetadataFields.resolve_key(key)
            if resolved in self._data and self._is_present(self._data[resolved]):
                return self._data[resolved]

            norm = normalize_key(key)
            if norm in self._normalized_lookup and self._is_present(self._normalized_lookup[norm]):
                return self._normalized_lookup[norm]

        return None

    def _derive_speed_3d_ms(self) -> Optional[float]:
        """Deriva velocidade 3D em m/s com fallback por conversao de km/h."""
        explicit_ms = self._to_float(self._first_value(["3DSpeed", "speed_3d_ms"]))
        if explicit_ms is not None:
            return explicit_ms
        kmh = self._to_float(self._first_value(["Speed3dKmh", "speed_3d_kmh"]))
        if kmh is None:
            return None
        return kmh / 3.6

    def _derive_incidence_angle(self) -> Optional[float]:
        """Deriva angulo de incidencia com fallback no pitch do gimbal."""
        explicit = self._to_float(self._first_value(["IncidenceAngle", "incidence_angle"]))
        if explicit is not None:
            return explicit
        pitch = self._to_float(self._first_value(["GimbalPitchDegree", "gimbal_pitch_degree"]))
        return abs(pitch) if pitch is not None else None

    def get_indicator(self, key: str) -> Any:
        """Resolve e retorna um indicador considerando aliases e campos derivados."""
        norm = normalize_key(key)
        if norm == "speed_3d_ms":
            return self._derive_speed_3d_ms()
        if norm == "incidence_angle":
            return self._derive_incidence_angle()
        if norm == "sensor_temp_c":
            return self._to_float(self._first_value(["SensorTemperature", "LensTemperature", "sensor_temp_c"]))
        return self._first_value([key, norm])

    def as_dict(self) -> Dict[str, Any]:
        """Exporta o registro bruto como dicionario."""
        return dict(self._data)


class RecordFactory:
    """Fabrica de objetos MetadataRecord a partir de uma lista de dicionarios."""

    @staticmethod
    def create_from_list(raw_records: List[Dict[str, Any]]) -> List[MetadataRecord]:
        """Cria objetos MetadataRecord em lote e retorna a lista resultante."""
        records = [MetadataRecord(record) for record in raw_records]
        print(f"Factory criou {len(records)} MetadataRecord")
        return records
