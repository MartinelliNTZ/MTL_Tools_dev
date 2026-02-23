# -*- coding: utf-8 -*-
from typing import List, Optional

from qgis.core import QgsApplication

from .ExecutionContext import ExecutionContext
from .BaseStep import BaseStep


class AsyncPipelineEngine:
    """
    Orquestrador genérico de Steps e QgsTasks.
    """

    def __init__(
        self,
        steps: List[BaseStep],
        context: ExecutionContext,
        *,
        on_finished=None,
        on_error=None,
        on_cancelled=None,
    ):
        self._steps = steps
        self._context = context

        self._on_finished = on_finished
        self._on_error = on_error
        self._on_cancelled = on_cancelled

        self._current_index = 0
        self._current_task = None
        self._is_running = False
        self._is_cancelled = False
    # -------------------------------------------------
    # Public API
    # -------------------------------------------------

    def start(self) -> None:
        if self._is_running:
            raise RuntimeError("Pipeline already running.")

        self._is_running = True
        self._is_cancelled = False
        self._current_index = 0

        self._run_next_step()

    def cancel(self) -> None:
        self._is_cancelled = True
        self._context.cancel()

        if self._current_task:
            try:
                self._current_task.cancel()
            except RuntimeError:
                pass

        self._finish_cancelled()

    def is_running(self) -> bool:
        return self._is_running

    # -------------------------------------------------
    # Internal Flow
    # -------------------------------------------------

    def _run_next_step(self) -> None:

        if self._is_cancelled or self._context.is_cancelled():
            self._finish_cancelled()
            return

        if self._current_index >= len(self._steps):
            self._finish_success()
            return

        step = self._steps[self._current_index]

        if not step.should_run(self._context):
            self._current_index += 1
            self._run_next_step()
            return

        task = step.create_task(self._context)

        if task is None:
            raise RuntimeError(f"Step '{step.name()}' returned no task.")

        self._current_task = task

        task.on_success = self._handle_task_success
        task.on_error = self._handle_task_error

        QgsApplication.taskManager().addTask(task)

    def _handle_task_success(self, result):

        step = self._steps[self._current_index]

        try:
            step.on_success(self._context, result)
        except Exception as exc:
            self._handle_task_error(exc)
            return

        self._current_index += 1
        self._run_next_step()

    def _handle_task_error(self, exception: Exception):

        step = self._steps[self._current_index]

        try:
            step.on_error(self._context, exception)
        except Exception:
            pass

        self._context.add_error(exception)
        self._finish_error()

    # -------------------------------------------------
    # Finalization
    # -------------------------------------------------

    def _finish_success(self):
        self._is_running = False
        self._current_task = None

        if self._on_finished:
            try:
                self._on_finished(self._context)
            except Exception:
                pass
    def _finish_error(self):
        self._is_running = False
        self._current_task = None

        if self._on_error:
            try:
                self._on_error(self._context.get_errors())
            except Exception:
                pass

    def _finish_cancelled(self):
        self._is_running = False
        self._current_task = None

        if self._on_cancelled:
            try:
                self._on_cancelled(self._context)
            except Exception:
                pass