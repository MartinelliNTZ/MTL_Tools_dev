# -*- coding: utf-8 -*-
from .BaseStep import BaseStep
from .ExecutionContext import ExecutionContext
from ..task.PhotoMetadataTask import PhotoMetadataTask
from ..config.LogUtils import LogUtils
from qgis.core import QgsField
from qgis.PyQt.QtCore import QVariant


class PhotoMetadataStep(BaseStep):
    """Step para aplicar metadados de fotos diretamente na camada."""

    def name(self) -> str:
        return "PhotoMetadataStep"

    @staticmethod
    def _normalize_attribute_value(value):
        if value is None:
            return None
        if isinstance(value, (str, int, float, bool)):
            return str(value)
        try:
            return str(value)
        except Exception:
            return None

    def create_task(self, context: ExecutionContext):
        context.require(["layer", "base_folder", "recursive", "tool_key"])

        layer = context.get("layer")
        return PhotoMetadataTask(
            layer_id=layer.id() if layer else "",
            base_folder=context.get("base_folder"),
            recursive=context.get("recursive", True),
            selected_required_fields=context.get("selected_required_fields", []),
            selected_custom_fields=context.get("selected_custom_fields", []),
            selected_mrk_fields=context.get("selected_mrk_fields", []),
            tool_key=context.get("tool_key"),
        )

    def on_success(self, context: ExecutionContext, result):
        if not result or not isinstance(result, dict):
            return

        layer = context.get("layer")
        if layer is None:
            LogUtils(
                tool=context.get("tool_key"),
                class_name=self.__class__.__name__,
            ).error("Camada ausente no contexto durante aplicação de metadados")
            return

        updates = result.get("updates", {}) or {}
        field_names = result.get("field_names", []) or []

        if not updates:
            LogUtils(
                tool=context.get("tool_key"),
                class_name=self.__class__.__name__,
            ).info("Nenhuma atualização de metadados de fotos para aplicar")
            return

        LogUtils(
            tool=context.get("tool_key"),
            class_name=self.__class__.__name__,
        ).debug(
            f"Aplicando metadados em {len(updates)} itens. Campos esperados: {field_names}"
        )

        # Adicionar campos faltantes
        missing_fields = [f for f in field_names if layer.fields().indexOf(f) == -1]
        started_editing = False
        if missing_fields:
            LogUtils(
                tool=context.get("tool_key"),
                class_name=self.__class__.__name__,
            ).debug(f"Adicionando campos faltantes: {missing_fields}")

            if not layer.isEditable():
                layer.startEditing()
                started_editing = True
            for field in missing_fields:
                layer.addAttribute(QgsField(field, QVariant.String))
            layer.updateFields()

        # Garantir modo de edição para aplicar valores
        if not layer.isEditable():
            layer.startEditing()
            started_editing = True

        # Mapear (mrk_folder, foto) -> fid (e compatibilidade por foto única)
        foto_to_fid = {}
        foto_mrk_to_fid = {}
        for feat in layer.getFeatures():
            foto_val = feat.attribute("foto")
            if foto_val is None:
                continue

            try:
                foto_int = int(foto_val)
            except Exception as e:
                LogUtils(
                    tool=context.get("tool_key"),
                    class_name=self.__class__.__name__,
                ).debug(
                    f"PhotoMetadataStep: failed parsing foto value {foto_val}: {e}"
                )
                continue

            mrk_folder_val = feat.attribute("mrk_folder")
            mrk_folder = str(mrk_folder_val or "").strip()
            foto_to_fid.setdefault(foto_int, feat.id())
            foto_mrk_to_fid[(mrk_folder, foto_int)] = feat.id()

        # Aplicar valores por batch
        layer.blockSignals(True)
        converted_values = 0
        conversion_fallbacks = 0
        apply_errors = 0
        try:
            for key, vals in updates.items():
                fid = None
                if isinstance(key, tuple) and len(key) == 2:
                    mrk_folder_key, foto_key = key
                    fid = foto_mrk_to_fid.get((str(mrk_folder_key or "").strip(), int(foto_key)))
                    if fid is None:
                        fid = foto_to_fid.get(int(foto_key))
                else:
                    try:
                        fid = foto_to_fid.get(int(key))
                    except Exception:
                        fid = None

                if fid is None:
                    continue
                for field_name, value in vals.items():
                    idx = layer.fields().indexOf(field_name)
                    if idx == -1:
                        continue
                    try:
                        safe_value = self._normalize_attribute_value(value)
                        if safe_value != value:
                            converted_values += 1
                            if safe_value is None and value is not None:
                                conversion_fallbacks += 1
                        layer.changeAttributeValue(fid, idx, safe_value)
                    except Exception as e:
                        apply_errors += 1
                        LogUtils(
                            tool=context.get("tool_key"),
                            class_name=self.__class__.__name__,
                        ).error(
                            f"Erro aplicando atributo foto={fid} field={field_name} "
                            f"type={type(value).__name__} value={repr(value)[:120]}: {e}"
                        )

            # Comentar commit para manter no buffer de edição caso o usuário queira revisar
        finally:
            layer.blockSignals(False)

        if started_editing:
            try:
                layer.commitChanges()
            except Exception as e:
                LogUtils(
                    tool=context.get("tool_key"), class_name=self.__class__.__name__
                ).error(f"Erro ao commitar alterações na camada: {e}")

        try:
            layer.triggerRepaint()
        except Exception as e:
            LogUtils(
                tool=context.get("tool_key"), class_name=self.__class__.__name__
            ).error(f"Erro ao repintar camada: {e}")
        LogUtils(
            tool=context.get("tool_key"),
            class_name=self.__class__.__name__,
        ).info(
            "Metadados de fotos aplicados",
            data={
                "updated_items": len(updates),
                "converted_values": converted_values,
                "conversion_fallbacks": conversion_fallbacks,
                "apply_errors": apply_errors,
            },
        )
