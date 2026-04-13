# -*- coding: utf-8 -*-
from datetime import datetime

from qgis.PyQt.QtCore import QVariant
from qgis.core import QgsVectorLayer, QgsWkbTypes, QgsField, QgsFeature

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
        "score_direcao": {"name": "score_dir", "type": QVariant.Int, "len": 10, "prec": 0},
        "score_continuidade": {"name": "score_cont", "type": QVariant.Int, "len": 10, "prec": 0},
        "seg_tipo": {"name": "seg_tipo", "type": QVariant.String, "len": 20, "prec": 0},
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
        confirmation_window: int = 3,
        min_confirmed: int = 2,
        border_azimuth_threshold: float = 90.0,
        border_speed_threshold: float = 1.0,
        border_distance_threshold: float = 5.0,
        retroactive_window: int = 5,
        fusion_azimuth_tolerance: float = 10.0,
        max_desvio: int = 5,
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

        import time
        eval_start = time.time()
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
            confirmation_window=confirmation_window,
            min_confirmed=min_confirmed,
            border_azimuth_threshold=border_azimuth_threshold,
            border_speed_threshold=border_speed_threshold,
            border_distance_threshold=border_distance_threshold,
            retroactive_window=retroactive_window,
            max_desvio=max_desvio,
        )
        eval_time = time.time() - eval_start
        self.logger.info(
            "Avaliação de pontos finalizada",
            evaluation_time_seconds=round(eval_time, 2),
            updates_generated=len(updates)
        )

        self.logger.debug("Calculando tamanhos dos tiros")
        shot_sizes = {}
        for values in updates.values():
            shot_id = values["tiro_id"]
            shot_sizes[shot_id] = shot_sizes.get(shot_id, 0) + 1

        self.logger.debug("Marcando tiros válidos/inválidos")
        for values in updates.values():
            shot_id = values["tiro_id"]
            values["tiro_valido"] = 1 if shot_sizes.get(shot_id, 0) >= minimum_point_count else 0

        # Fusão de tiros pequenos consecutivos
        updates = self._fuse_small_shots(updates, minimum_point_count, fusion_azimuth_tolerance)

        # Recalcular tamanhos após fusão
        shot_sizes = {}
        for values in updates.values():
            shot_id = values["tiro_id"]
            shot_sizes[shot_id] = shot_sizes.get(shot_id, 0) + 1

        # Remarcar válidos após fusão
        for values in updates.values():
            shot_id = values["tiro_id"]
            values["tiro_valido"] = 1 if shot_sizes.get(shot_id, 0) >= minimum_point_count else 0

        # Marcar tiros órfãos (pequenos) como ID 0
        for fid, values in updates.items():
            shot_id = values["tiro_id"]
            if shot_sizes.get(shot_id, 0) < minimum_point_count:
                values["tiro_id"] = 0
                values["tiro_valido"] = 0

        self.logger.debug("Criando nova camada de memória com resultados")
        result_layer = self._create_memory_layer_with_updates(layer, updates, field_name_map)

        valid_shots = sum(1 for _, size in shot_sizes.items() if size >= minimum_point_count)
        invalid_shots = len(shot_sizes) - valid_shots

        summary = {
            "total_points": len(ordered),
            "total_shots": len(shot_sizes),
            "valid_shots": valid_shots,
            "invalid_shots": invalid_shots,
            "source_path": self.source_path,
            "field_name_map": field_name_map,
            "result_layer": result_layer,
        }
        total_time = time.time() - eval_start  # From eval_start
        self.logger.info(
            "Julgamento concluído",
            total_processing_time_seconds=round(total_time, 2),
            summary=summary
        )
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

        if layer.fields().lookupField(field_id) == -1:
            raise RuntimeError(f"Campo de ID não encontrado: {field_id}")

        if layer.fields().lookupField(field_time) == -1:
            raise RuntimeError(f"Campo de timestamp não encontrado: {field_time}")

    def _load_ordered_points(self, layer, field_id: str, field_time: str):
        import time
        load_start = time.time()
        self.logger.debug("Carregando pontos ordenados da camada")

        ordered = []
        total_features = layer.featureCount()
        processed = 0

        for feature in layer.getFeatures():
            processed += 1
            if processed % 10000 == 0 or processed == total_features:
                self.logger.debug(
                    f"Carregando features: {processed}/{total_features} ({(processed/total_features)*100:.1f}%)"
                )

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

        load_time = time.time() - load_start
        self.logger.info(
            "Pontos carregados e ordenados",
            total_features=total_features,
            valid_points=len(ordered),
            load_time_seconds=round(load_time, 2)
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
        confirmation_window: int,
        min_confirmed: int,
        border_azimuth_threshold: float,
        border_speed_threshold: float,
        border_distance_threshold: float,
        retroactive_window: int,
        max_desvio: int,
    ):
        import time
        start_time = time.time()
        total_points = len(ordered_points)
        self.logger.info(
            "Iniciando avaliação de pontos com melhorias",
            total_points=total_points,
            confirmation_window=confirmation_window,
            border_azimuth_threshold=border_azimuth_threshold
        )

        updates = {}
        azimuth_history = []
        current_shot_id = 1

        first = ordered_points[0]
        updates[first["fid"]] = self._build_default_output(current_shot_id)

        progress_interval = max(1, total_points // 10)  # Log every 10% or at least every point if small

        for index in range(1, len(ordered_points)):
            if index % progress_interval == 0 or index == total_points - 1:
                elapsed = time.time() - start_time
                progress_percent = (index / total_points) * 100
                self.logger.info(
                    f"Processando pontos: {index}/{total_points} ({progress_percent:.1f}%)",
                    elapsed_seconds=round(elapsed, 2),
                    current_shot_id=current_shot_id,
                    azimuth_history_size=len(azimuth_history)
                )

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

            # Calcular scores separados
            score_direcao = 0
            if delta_azimuth > light_azimuth_threshold:
                score_direcao += 1
            if delta_azimuth > severe_azimuth_threshold:
                score_direcao += 2

            score_continuidade = 0
            score_continuidade = self._apply_time_score(
                score=score_continuidade,
                delta_time=delta_time,
                point_frequency_seconds=point_frequency_seconds,
                time_tolerance_multiplier=time_tolerance_multiplier,
            )
            if delta_distance > float(strip_width_meters) * 0.8:
                score_continuidade += 1

            total_score = score_direcao + score_continuidade

            # Verificar se é outlier e tentar pular
            is_outlier = total_score >= minimum_break_score
            skip_outliers = False
            if is_outlier:
                for skip in range(1, max_desvio + 1):
                    if index + skip < len(ordered_points):
                        next_point = ordered_points[index + skip]
                        # Calcular score aproximado para o próximo
                        next_az = VectorLayerGeometry.calculate_point_azimuth(
                            previous["point"], next_point["point"]
                        )
                        next_mean = VectorLayerGeometry.circular_mean_degrees(azimuth_history[-azimuth_window:] or [next_az])
                        next_delta = VectorLayerGeometry.angular_difference_degrees(next_az, next_mean)
                        next_score_dir = 0
                        if next_delta > light_azimuth_threshold:
                            next_score_dir += 1
                        if next_delta > severe_azimuth_threshold:
                            next_score_dir += 2
                        next_delta_time = max(0.0, next_point["timestamp"] - previous["timestamp"])
                        next_score_cont = self._apply_time_score(
                            score=0,
                            delta_time=next_delta_time,
                            point_frequency_seconds=point_frequency_seconds,
                            time_tolerance_multiplier=time_tolerance_multiplier,
                        )
                        next_dist = VectorLayerGeometry.measure_distance_between_points(
                            previous["point"], next_point["point"], layer.crs()
                        )
                        if next_dist > float(strip_width_meters) * 0.8:
                            next_score_cont += 1
                        next_total = next_score_dir + next_score_cont
                        if next_total < minimum_break_score:
                            skip_outliers = True
                            # Recalcular delta_azimuth pulando
                            delta_azimuth = VectorLayerGeometry.angular_difference_degrees(next_az, next_mean)
                            delta_time = next_delta_time
                            delta_distance = next_dist
                            instant_speed = next_dist / next_delta_time if next_delta_time > 0 else 0.0
                            total_score = next_total
                            break

            # Detectar bordadura
            is_border = (
                delta_azimuth > border_azimuth_threshold and
                instant_speed < border_speed_threshold and
                delta_distance < border_distance_threshold
            )
            seg_tipo = "bordadura" if is_border else "faixa"

            # Janela de confirmação (se não pulou)
            should_break = False
            if not skip_outliers and total_score >= minimum_break_score:
                confirmed = 0
                for j in range(index + 1, min(index + 1 + confirmation_window, len(ordered_points))):
                    prev_p = ordered_points[j - 1]
                    curr_p = ordered_points[j]
                    conf_az = VectorLayerGeometry.calculate_point_azimuth(prev_p["point"], curr_p["point"])
                    conf_mean = VectorLayerGeometry.circular_mean_degrees(azimuth_history[-azimuth_window:] or [conf_az])
                    conf_delta = VectorLayerGeometry.angular_difference_degrees(conf_az, conf_mean)
                    conf_score = 0
                    if conf_delta > light_azimuth_threshold:
                        conf_score += 1
                    if conf_delta > severe_azimuth_threshold:
                        conf_score += 2
                    if conf_score >= minimum_break_score:
                        confirmed += 1
                if confirmed >= min_confirmed:
                    should_break = True

            # Retroativo: verificar se próximos pontos anulam
            if should_break:
                future_scores = []
                for k in range(index + 1, min(index + 1 + retroactive_window, len(ordered_points))):
                    # Simular score futuro (aproximado)
                    fut_prev = ordered_points[k - 1]
                    fut_curr = ordered_points[k]
                    fut_az = VectorLayerGeometry.calculate_point_azimuth(fut_prev["point"], fut_curr["point"])
                    fut_mean = VectorLayerGeometry.circular_mean_degrees(azimuth_history[-azimuth_window:] or [fut_az])
                    fut_delta = VectorLayerGeometry.angular_difference_degrees(fut_az, fut_mean)
                    fut_score = 0
                    if fut_delta > light_azimuth_threshold:
                        fut_score += 1
                    if fut_delta > severe_azimuth_threshold:
                        fut_score += 2
                    future_scores.append(fut_score)
                if all(s == 0 for s in future_scores):
                    should_break = False  # Cancelar quebra

            if should_break:
                current_shot_id += 1

            updates[current["fid"]] = {
                "tiro_id": current_shot_id,
                "tiro_valido": False,
                "score": int(total_score),
                "score_direcao": int(score_direcao),
                "score_continuidade": int(score_continuidade),
                "seg_tipo": seg_tipo,
                "azimute_instantaneo": float(instant_azimuth),
                "azimute_medio": float(mean_azimuth),
                "delta_azimute": float(delta_azimuth),
                "delta_tempo": float(delta_time),
                "delta_distancia": float(delta_distance),
                "velocidade_instant": float(instant_speed),
            }

            azimuth_history.append(instant_azimuth)

        total_elapsed = time.time() - start_time
        self.logger.info(
            "Avaliação de pontos concluída com melhorias",
            total_elapsed_seconds=round(total_elapsed, 2),
            final_shot_id=current_shot_id,
            updates_count=len(updates)
        )

        return updates

    def _fuse_small_shots(self, updates, minimum_point_count, fusion_azimuth_tolerance):
        """Funde tiros pequenos consecutivos com azimute médio similar."""
        if not updates:
            return updates

        # Agrupar por tiro_id
        shots = {}
        for fid, values in updates.items():
            shot_id = values["tiro_id"]
            if shot_id not in shots:
                shots[shot_id] = []
            shots[shot_id].append((fid, values))

        # Calcular tamanhos e azimutes médios
        shot_stats = {}
        for shot_id, features in shots.items():
            size = len(features)
            azimuths = [v["azimute_medio"] for _, v in features if v["azimute_medio"] > 0]
            mean_azimuth = VectorLayerGeometry.circular_mean_degrees(azimuths) if azimuths else 0
            shot_stats[shot_id] = {"size": size, "mean_azimuth": mean_azimuth}

        # Encontrar candidatos à fusão: tiros pequenos consecutivos
        sorted_shots = sorted(shot_stats.keys())
        fusions = []
        for i in range(len(sorted_shots) - 1):
            current_id = sorted_shots[i]
            next_id = sorted_shots[i + 1]
            if (shot_stats[current_id]["size"] < minimum_point_count and
                shot_stats[next_id]["size"] < minimum_point_count):
                delta_az = VectorLayerGeometry.angular_difference_degrees(
                    shot_stats[current_id]["mean_azimuth"], shot_stats[next_id]["mean_azimuth"]
                )
                if delta_az <= fusion_azimuth_tolerance:
                    fusions.append((current_id, next_id))

        # Aplicar fusões
        for from_id, to_id in fusions:
            for fid, values in shots[from_id]:
                values["tiro_id"] = to_id

        self.logger.info("Fusão de tiros pequenos aplicada", fusions_count=len(fusions))
        return updates

    def _build_default_output(self, shot_id: int):
        return {
            "tiro_id": shot_id,
            "tiro_valido": 0,
            "score": 0,
            "score_direcao": 0,
            "score_continuidade": 0,
            "seg_tipo": "faixa",
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
    def _create_memory_layer_with_updates(layer, updates, field_name_map):
        """Cria uma nova camada de memória com os updates aplicados."""
        import time
        start = time.time()

        # Criar nova camada de memória com mesmo CRS e geometria
        uri = f"Point?crs={layer.crs().authid()}"
        new_layer = QgsVectorLayer(uri, f"{layer.name()}_segmentado", "memory")
        if not new_layer.isValid():
            raise RuntimeError("Falha ao criar camada de memória")

        # Copiar campos da camada original
        new_fields = layer.fields()
        # Adicionar campos de saída
        for logical_name, spec in SequentialPointBreakJudge.OUTPUT_FIELDS.items():
            field_name = field_name_map[logical_name]
            if new_fields.lookupField(field_name) == -1:
                new_fields.append(QgsField(field_name, spec["type"], len=spec["len"], prec=spec["prec"]))

        # Para camadas de memória, usar dataProvider para adicionar campos
        new_layer.dataProvider().addAttributes(new_fields)
        new_layer.updateFields()

        # Adicionar features com updates
        new_layer.startEditing()
        for feature in layer.getFeatures():
            fid = feature.id()
            if fid in updates:
                # Criar uma nova feature com os campos da nova camada
                new_feature = QgsFeature(new_layer.fields())
                new_feature.setGeometry(feature.geometry())
                
                # Copiar atributos originais por nome de campo
                for idx, field in enumerate(feature.fields()):
                    field_name = field.name()
                    value = feature.attribute(field_name)
                    new_feature.setAttribute(field_name, value)
                
                # Adicionar novos atributos calculados
                for attr_name, attr_value in updates[fid].items():
                    resolved_name = field_name_map.get(attr_name, attr_name)
                    # Usar índice do campo para garantir que existe
                    field_idx = new_layer.fields().lookupField(resolved_name)
                    if field_idx >= 0:
                        new_feature.setAttribute(field_idx, attr_value)
                
                new_layer.addFeature(new_feature)

        new_layer.commitChanges()
        new_layer.updateFields()

        elapsed = time.time() - start
        LogUtils(tool=ToolKey.UNTRACEABLE, class_name="SequentialPointBreakJudge").info(
            "Nova camada de memória criada",
            original_features=layer.featureCount(),
            new_features=new_layer.featureCount(),
            creation_time_seconds=round(elapsed, 2)
        )

        return new_layer
