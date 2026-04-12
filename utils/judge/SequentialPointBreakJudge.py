# -*- coding: utf-8 -*-
from datetime import datetime

from qgis.PyQt.QtCore import QVariant
from qgis.core import QgsVectorLayer, QgsWkbTypes

from ...core.config.LogUtils import LogUtils
from ..ToolKeys import ToolKey
from ..vector.VectorLayerAttributes import VectorLayerAttributes
from ..vector.VectorLayerGeometry import VectorLayerGeometry
from ..vector.VectorLayerSource import VectorLayerSource


class SequentialPointBreakJudge:
    """Juiz genérico para segmentar sequências de pontos em tiros/faixas."""

    OUTPUT_FIELDS = {
        "tiro_id": {"name": "tiro_id", "type": QVariant.Int, "len": 10, "prec": 0},
        "tiro_valido": {
            "name": "tiro_val",
            "type": QVariant.Int,
            "len": 1,
            "prec": 0,
        },
        "score": {"name": "score", "type": QVariant.Int, "len": 10, "prec": 0},
        "azimute_instantaneo": {
            "name": "azi_inst",
            "type": QVariant.Double,
            "len": 20,
            "prec": 8,
        },
        "azimute_medio": {
            "name": "azi_med",
            "type": QVariant.Double,
            "len": 20,
            "prec": 8,
        },
        "delta_azimute": {
            "name": "del_azi",
            "type": QVariant.Double,
            "len": 20,
            "prec": 8,
        },
        "delta_tempo": {
            "name": "del_tmp",
            "type": QVariant.Double,
            "len": 20,
            "prec": 8,
        },
        "delta_distancia": {
            "name": "del_dst",
            "type": QVariant.Double,
            "len": 20,
            "prec": 8,
        },
        "velocidade_instant": {
            "name": "vel_inst",
            "type": QVariant.Double,
            "len": 20,
            "prec": 8,
        },
    }

    def __init__(
        self,
        *,
        layer=None,
        source_path: str = "",
        tool_key: str = ToolKey.UNTRACEABLE,
    ):
        self.layer = layer
        self.source_path = source_path or (layer.source() if layer is not None else "")
        self.tool_key = tool_key
        self.logger = LogUtils(tool=tool_key, class_name=self.__class__.__name__)

    def judge(
        self,
        *,
        field_id: str,
        field_time: str,
        point_frequency_seconds: float,
        strip_width_meters: float,
        azimuth_window: int = 10,
        light_azimuth_threshold: float = 20.0,
        severe_azimuth_threshold: float = 45.0,
        minimum_break_score: int = 3,
        minimum_point_count: int = 20,
        time_tolerance_multiplier: float = 3.0,
        conflict_resolver=None,
    ):
        layer = self._load_layer()
        self._validate_layer(layer, field_id, field_time)
        field_name_map = self._resolve_output_fields(
            layer, conflict_resolver=conflict_resolver
        )

        ordered = self._load_ordered_points(layer, field_id, field_time)
        if not ordered:
            raise RuntimeError("Nenhum ponto válido encontrado para julgamento.")

        self.logger.info(
            "Iniciando julgamento de pontos",
            source_path=self.source_path,
            features=len(ordered),
            field_id=field_id,
            field_time=field_time,
        )

        updates = self._evaluate_points(
            ordered_points=ordered,
            layer=layer,
            point_frequency_seconds=point_frequency_seconds,
            strip_width_meters=strip_width_meters,
            azimuth_window=azimuth_window,
            light_azimuth_threshold=light_azimuth_threshold,
            severe_azimuth_threshold=severe_azimuth_threshold,
            minimum_break_score=minimum_break_score,
            time_tolerance_multiplier=time_tolerance_multiplier,
        )

        shot_sizes = {}
        for values in updates.values():
            shot_id = values["tiro_id"]
            shot_sizes[shot_id] = shot_sizes.get(shot_id, 0) + 1

        for values in updates.values():
            shot_id = values["tiro_id"]
            values["tiro_valido"] = 1 if shot_sizes.get(shot_id, 0) >= minimum_point_count else 0

        field_specs = []
        for logical_name, spec in self.OUTPUT_FIELDS.items():
            field_specs.append(
                (
                    field_name_map[logical_name],
                    spec["type"],
                    spec["len"],
                    spec["prec"],
                )
            )

        VectorLayerAttributes.ensure_fields(layer, field_specs, self.logger)
        provider_updates = self._map_updates_to_resolved_fields(
            updates, field_name_map
        )
        VectorLayerAttributes.apply_updates_by_field_name(
            layer, provider_updates, self.logger
        )

        layer.updateFields()
        layer.triggerRepaint()

        valid_shots = sum(1 for _, size in shot_sizes.items() if size >= minimum_point_count)
        invalid_shots = len(shot_sizes) - valid_shots

        summary = {
            "total_points": len(ordered),
            "total_shots": len(shot_sizes),
            "valid_shots": valid_shots,
            "invalid_shots": invalid_shots,
            "source_path": self.source_path,
            "field_name_map": field_name_map,
        }
        self.logger.info("Julgamento concluído", summary=summary)
        return summary

    def _load_layer(self):
        if self.layer is not None:
            return self.layer

        layer = VectorLayerSource.load_vector_layer_from_source_path(
            self.source_path,
            external_tool_key=self.tool_key,
        )
        if not layer:
            raise RuntimeError("Não foi possível carregar a camada a partir do source path.")
        return layer

    def _validate_layer(self, layer, field_id: str, field_time: str):
        if not isinstance(layer, QgsVectorLayer) or not layer.isValid():
            raise RuntimeError("Camada vetorial inválida.")

        if layer.geometryType() != QgsWkbTypes.PointGeometry:
            raise RuntimeError("A camada deve ser do tipo ponto.")

        if not layer.isEditable():
            raise RuntimeError("A camada precisa estar em modo de edição.")

        if layer.fields().lookupField(field_id) == -1:
            raise RuntimeError(f"Campo de ID não encontrado: {field_id}")

        if layer.fields().lookupField(field_time) == -1:
            raise RuntimeError(f"Campo de timestamp não encontrado: {field_time}")

    def _load_ordered_points(self, layer, field_id: str, field_time: str):
        ordered = []
        for feature in layer.getFeatures():
            geometry = feature.geometry()
            if not geometry or geometry.isEmpty():
                continue

            point = VectorLayerGeometry.get_representative_point(geometry)
            if point is None:
                continue
            timestamp = self._parse_timestamp(feature.attribute(field_time))
            if timestamp is None:
                continue

            ordered.append(
                {
                    "fid": feature.id(),
                    "seq_id_sort": self._build_sort_key(feature.attribute(field_id)),
                    "timestamp": timestamp,
                    "point": point,
                }
            )

        ordered.sort(
            key=lambda item: (
                item["seq_id_sort"],
                item["timestamp"],
                item["fid"],
            )
        )
        return ordered

    def _evaluate_points(
        self,
        *,
        ordered_points,
        layer,
        point_frequency_seconds: float,
        strip_width_meters: float,
        azimuth_window: int,
        light_azimuth_threshold: float,
        severe_azimuth_threshold: float,
        minimum_break_score: int,
        time_tolerance_multiplier: float,
    ):
        updates = {}
        azimuth_history = []
        current_shot_id = 1

        first = ordered_points[0]
        updates[first["fid"]] = self._build_default_output(current_shot_id)

        for index in range(1, len(ordered_points)):
            previous = ordered_points[index - 1]
            current = ordered_points[index]

            instant_azimuth = VectorLayerGeometry.calculate_point_azimuth(
                previous["point"], current["point"]
            )

            window_values = azimuth_history[-max(1, int(azimuth_window)) :]
            mean_azimuth = (
                VectorLayerGeometry.circular_mean_degrees(window_values)
                if window_values
                else instant_azimuth
            )

            delta_azimuth = VectorLayerGeometry.angular_difference_degrees(
                instant_azimuth, mean_azimuth
            )
            delta_time = max(0.0, current["timestamp"] - previous["timestamp"])
            delta_distance = VectorLayerGeometry.measure_distance_between_points(
                previous["point"], current["point"], layer.crs()
            )
            instant_speed = delta_distance / delta_time if delta_time > 0 else 0.0

            score = 0
            if delta_azimuth > light_azimuth_threshold:
                score += 1
            if delta_azimuth > severe_azimuth_threshold:
                score += 2

            score = self._apply_time_score(
                score=score,
                delta_time=delta_time,
                point_frequency_seconds=point_frequency_seconds,
                time_tolerance_multiplier=time_tolerance_multiplier,
            )

            if delta_distance > float(strip_width_meters) * 0.8:
                score += 1

            if score >= minimum_break_score:
                current_shot_id += 1

            updates[current["fid"]] = {
                "tiro_id": current_shot_id,
                "tiro_valido": False,
                "score": int(score),
                "azimute_instantaneo": float(instant_azimuth),
                "azimute_medio": float(mean_azimuth),
                "delta_azimute": float(delta_azimuth),
                "delta_tempo": float(delta_time),
                "delta_distancia": float(delta_distance),
                "velocidade_instant": float(instant_speed),
            }

            azimuth_history.append(instant_azimuth)

        return updates

    def _build_default_output(self, shot_id: int):
        return {
            "tiro_id": shot_id,
            "tiro_valido": 0,
            "score": 0,
            "azimute_instantaneo": 0.0,
            "azimute_medio": 0.0,
            "delta_azimute": 0.0,
            "delta_tempo": 0.0,
            "delta_distancia": 0.0,
            "velocidade_instant": 0.0,
        }

    @staticmethod
    def _apply_time_score(
        *,
        score: int,
        delta_time: float,
        point_frequency_seconds: float,
        time_tolerance_multiplier: float,
    ) -> int:
        threshold = float(point_frequency_seconds) * float(time_tolerance_multiplier)
        if delta_time > threshold:
            score += 1
        if delta_time > threshold * 3.0:
            score += 3
        return score

    def _resolve_output_fields(self, layer, *, conflict_resolver=None):
        max_length = 10 if self.source_path.lower().endswith(".shp") else 255
        resolved = {}
        for logical_name, spec in self.OUTPUT_FIELDS.items():
            field_name = VectorLayerAttributes.resolve_output_field_name(
                layer,
                spec["name"],
                conflict_resolver=conflict_resolver,
                max_length=max_length,
            )
            if field_name is None:
                raise RuntimeError("Operação cancelada pelo usuário.")
            resolved[logical_name] = field_name
        return resolved

    @staticmethod
    def _map_updates_to_resolved_fields(updates, field_name_map):
        remapped = {}
        for fid, values in (updates or {}).items():
            remapped[fid] = {
                field_name_map[logical_name]: value
                for logical_name, value in values.items()
            }
        return remapped

    @staticmethod
    def _build_sort_key(value):
        try:
            return (0, int(value))
        except Exception:
            try:
                return (0, float(value))
            except Exception:
                return (1, str(value or "").strip().lower())

    @staticmethod
    def _parse_timestamp(value):
        if value is None:
            return None

        if hasattr(value, "toSecsSinceEpoch"):
            try:
                return float(value.toSecsSinceEpoch())
            except Exception:
                pass

        if isinstance(value, datetime):
            return float(value.timestamp())

        if isinstance(value, (int, float)):
            numeric = float(value)
            return SequentialPointBreakJudge._coerce_numeric_timestamp(numeric)

        text = str(value).strip()
        if not text:
            return None

        for parser in (
            lambda x: datetime.fromisoformat(x.replace("Z", "+00:00")).timestamp(),
            lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S").timestamp(),
            lambda x: datetime.strptime(x, "%d/%m/%Y %H:%M:%S").timestamp(),
            lambda x: datetime.strptime(x, "%Y-%m-%dT%H:%M:%S").timestamp(),
            lambda x: datetime.strptime(x, "%Y%m%d%H%M%S").timestamp(),
            lambda x: datetime.strptime(x, "%Y%m%d_%H%M%S").timestamp(),
        ):
            try:
                return float(parser(text))
            except Exception:
                continue

        digits = "".join(ch for ch in text if ch.isdigit())
        if len(digits) == 14:
            try:
                return float(datetime.strptime(digits, "%Y%m%d%H%M%S").timestamp())
            except Exception:
                pass

        try:
            return SequentialPointBreakJudge._coerce_numeric_timestamp(float(text))
        except Exception:
            return None

    @staticmethod
    def _coerce_numeric_timestamp(value: float):
        absolute = abs(float(value))

        if 1e12 <= absolute < 1e15:
            return float(value) / 1000.0

        if 1e9 <= absolute < 1e12:
            return float(value)

        return float(value)
