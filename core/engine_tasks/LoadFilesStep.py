# -*- coding: utf-8 -*-
from typing import Any, Dict, List
import time

from .BaseStep import BaseStep
from ..task.LoadFilesTask import LoadFilesTask
from ..config.LogUtils import LogUtils
from .ExecutionContext import ExecutionContext
import os
from qgis.core import QgsProject
from qgis.PyQt.QtWidgets import QApplication

from ...utils.ExplorerUtils import ExplorerUtils
from ...utils.ProjectUtils import ProjectUtils
from ...utils.QgisMessageUtil import QgisMessageUtil
import threading
from ..ui.ProgressDialog import ProgressDialog


class LoadFilesStep(BaseStep):
    def name(self) -> str:
        return "load_files"

    def create_task(self, context: ExecutionContext):
        context.require(["records", "tool_key"])
        records = context.get("records")
        tool_key = context.get("tool_key")
        return LoadFilesTask(records=records, tool_key=tool_key)

    def on_success(self, context: ExecutionContext, result: Any) -> None:
        logger = LogUtils(tool=context.get("tool_key"), class_name=self.__class__.__name__)

        valid = []
        if isinstance(result, dict):
            valid = result.get("valid_records", [])
        elif isinstance(result, list):
            valid = result

        logger.info(f"LoadFilesStep.on_success: registros válidos={len(valid)} thread={threading.current_thread().name}")

        # Agora, no thread principal, instanciar camadas e adicioná-las ao projeto
        project = QgsProject.instance()
        root = project.layerTreeRoot()

        # Evitar refresh pesado bloqueando signals do layer tree
        try:
            root.blockSignals(True)
        except Exception:
            pass

        loaded = 0
        total = len(valid)
        chunk = 10
        progress = None

        try:
            parent = context.get("parent", None)
            try:
                progress = ProgressDialog("Carregando camadas...", "Cancelar", 0, total, parent)
                progress.show()
            except Exception:
                progress = None
            for i in range(0, total, chunk):
                time.sleep(0.1)  # pequeno delay para permitir UI responder
                if context.is_cancelled():
                    logger.info("LoadFilesStep.on_success: cancelado durante adição de layers")
                    break

                batch = valid[i:i+chunk]

                # bloquear signals apenas durante adição do lote
                try:
                    root.blockSignals(True)
                except Exception:
                    pass

                for rec in batch:
                    try:
                        layer = ExplorerUtils.create_layer(rec, context.get("tool_key"))
                        if not layer or not layer.isValid():
                            logger.warning(f"LoadFilesStep: camada inválida para {rec.get('path')}")
                            continue

                        folder = context.get("folder", "")
                        if context.get("preserve", False):
                            rel = os.path.relpath(os.path.dirname(rec.get("path")), folder)
                            if rel == ".":
                                ProjectUtils.add_layer(layer, add_to_root=True)
                            else:
                                try:
                                    group = ProjectUtils.ensure_group(rel)
                                    ProjectUtils.add_layer_to_group(layer, group)
                                except Exception as ge:
                                    logger.error(f"Erro adicionando camada ao grupo {rel}: {ge}")
                                    ProjectUtils.add_layer(layer, add_to_root=True)
                        else:
                            ProjectUtils.add_layer(layer, add_to_root=True)

                        loaded += 1
                        # atualizar progresso se existir dialog
                        try:
                            if progress:
                                progress.set_value(loaded)
                                if progress.is_canceled():
                                    context.cancel()
                                    logger.info("LoadFilesStep: cancelado pelo usuário via ProgressDialog")
                                    break
                        except Exception:
                            pass
                    except Exception as e:
                        logger.error(f"LoadFilesStep: erro ao criar/adicionar camada {rec.get('path')}: {e}")
                        continue

                # desbloquear signals para permitir atualização da árvore e UI
                try:
                    root.blockSignals(False)
                except Exception:
                    pass

                # permitir UI responder entre lotes
                try:
                    QApplication.processEvents()
                except Exception:
                    pass

                logger.info(f"LoadFilesStep: batch {i}-{i+len(batch)-1} adicionadas; progresso {loaded}/{total}")
                # reloop - signals serão bloqueados novamente no próximo lote
        finally:
            try:
                root.blockSignals(False)
            except Exception:
                pass
            try:
                if progress:
                    progress.close()
            except Exception:
                pass

        context.set("loaded_count", loaded)
        logger.info(f"LoadFilesStep.on_success: terminada, loaded={loaded}")
