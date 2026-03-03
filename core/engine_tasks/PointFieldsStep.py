# -*- coding: utf-8 -*-
from .BaseStep import BaseStep
from .ExecutionContext import ExecutionContext
from ..task.PointFieldsTask import PointFieldsTask
from ..config.LogUtils import LogUtils
from qgis.core import QgsField
from qgis.PyQt.QtCore import QVariant
from qgis.PyQt.QtWidgets import QApplication
import tempfile


class PointFieldsStep(BaseStep):
    """
    Step para calcular campos X, Y de pontos.
    
    Padrão GenerateTrail:
    - Task salva em GPKG na worker thread
    - on_success() apenas copia PATH no contexto (rápido, não trava UI)
    """

    def name(self) -> str:
        return "point_fields"

    def create_task(self, context: ExecutionContext):
        context.require(["layer", "field_map", "tool_key"])

        tmp_dir = context.get("tmp_dir")
        if not tmp_dir:
            tmp_dir = tempfile.mkdtemp(prefix="vector_fields_")
            context.set("tmp_dir", tmp_dir)

        return PointFieldsTask(
            layer=context.get("layer"),
            field_map=context.get("field_map"),
            tool_key=context.get("tool_key"),
            tmp_dir=tmp_dir
        )

    def on_success(self, context: ExecutionContext, result):
        """
        Apply attribute mappings computed by the task on the MAIN THREAD.
        Result expected shape: { 'updates': {fid: {field_name: value}}, 'missing_fields': [field_name,...] }
        """
        LogUtils.log(
            f"PointFieldsStep.on_success: applying results",
            level="INFO",
            tool=context.get("tool_key"),
            class_name=self.__class__.__name__
        )

        if not result or not isinstance(result, dict):
            LogUtils.log(
                f"PointFieldsStep.on_success: resultado inválido: {result}",
                level="ERROR",
                tool=context.get("tool_key"),
                class_name=self.__class__.__name__
            )
            return

        layer = context.get("layer")
        if layer is None:
            LogUtils.log(
                "PointFieldsStep.on_success: layer ausente no contexto",
                level="ERROR",
                tool=context.get("tool_key"),
                class_name=self.__class__.__name__
            )
            return

        const_prec = 8

        # 1) Add missing fields into the layer edit buffer (do not save)
        missing = result.get("missing_fields", []) or []
        started_editing = False
        if missing:
            if not layer.isEditable():
                layer.startEditing()
                started_editing = True
            for fname in missing:
                LogUtils.log(
                    f"PointFieldsStep: adicionando campo (edição) {fname}",
                    level="DEBUG",
                    tool=context.get("tool_key"),
                    class_name=self.__class__.__name__
                )
                layer.addAttribute(QgsField(fname, QVariant.Double, len=20, prec=const_prec))
            layer.updateFields()

        # 2) Build provider-compatible mapping (fid -> {field_index: value})
        name_to_idx = {f.name(): idx for idx, f in enumerate(layer.fields())}
        updates = result.get("updates", {}) or {}
        provider_updates = {}
        for fid, vals in updates.items():
            for fname, val in vals.items():
                idx = name_to_idx.get(fname)
                if idx is None:
                    LogUtils.log(
                        f"PointFieldsStep: campo não encontrado {fname}, pulando",
                        level="WARNING",
                        tool=context.get("tool_key"),
                        class_name=self.__class__.__name__
                    )
                    continue
                provider_updates.setdefault(fid, {})[idx] = val

        # 3) Apply in batches on main thread
        if not provider_updates:
            LogUtils.log(
                "PointFieldsStep: nada a aplicar",
                level="INFO",
                tool=context.get("tool_key"),
                class_name=self.__class__.__name__
            )
            return

        items = list(provider_updates.items())
        total = len(items)
        chunk = 2000
        
        # Bloquear signals da layer durante atualização em batch para evitar overhead
        layer.blockSignals(True)
        try:
            for i in range(0, total, chunk):
                if context.is_cancelled():
                    LogUtils.log(
                        "PointFieldsStep: cancelado durante aplicação",
                        level="INFO",
                        tool=context.get("tool_key"),
                        class_name=self.__class__.__name__
                    )
                    break

                batch_items = dict(items[i:i+chunk])
                # apply into edit buffer using changeAttributeValue
                for fid, idx_map in batch_items.items():
                    for idx, val in idx_map.items():
                        try:
                            layer.changeAttributeValue(fid, idx, val)
                        except Exception as e:
                            LogUtils.log(
                                f"PointFieldsStep: falha ao aplicar fid={fid} idx={idx} err={e}",
                                level="ERROR",
                                tool=context.get("tool_key"),
                                class_name=self.__class__.__name__
                            )
                LogUtils.log(
                    f"PointFieldsStep: applied edit-buffer batch {i}-{i+len(batch_items)} items={len(batch_items)}",
                    level="DEBUG",
                    tool=context.get("tool_key"),
                    class_name=self.__class__.__name__
                )
                QApplication.processEvents()
        finally:
            # Sempre desbloquear signals mesmo se houver erro ou cancelamento
            layer.blockSignals(False)

        LogUtils.log(
            f"PointFieldsStep.on_success: aplicação em buffer concluída {len(provider_updates)} features",
            level="INFO",
            tool=context.get("tool_key"),
            class_name=self.__class__.__name__
        )
