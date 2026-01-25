# utils/log_utils.py
import json
import threading
import uuid
import os
from pathlib import Path
from datetime import datetime
import traceback
from .log_sync import LOG_FILE_LOCK

class LogUtils:
    """
    Logger estruturado (JSONL), 1 arquivo por sessão QGIS.
    Thread-safe. Sem rotação automática.
    """


    """Níveis de log disponíveis."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
    # Cores para níveis de log
    LEVEL_COLORS = {
        'DEBUG': '#9CA3AF',      # Cinza (suave)
        'INFO': '#10B981',       # Verde (informação)
        'WARNING': '#F59E0B',    # Âmbar (atenção)
        'ERROR': '#DC2626',      # Vermelho forte (erro)
        'CRITICAL': '#991B1B'    # Vermelho escuro muito forte (crítico)
    }

    _initialized = False
    _log_file = None
    _session_id = None
    _plugin_name = "MTL Tools"
    _plugin_version = "unknown"

    @classmethod
    def init(cls, plugin_root: Path):
        """
        Inicializa o logger. Deve ser chamado uma única vez.
        """
        if cls._initialized:
            return

        cls._session_id = str(uuid.uuid4())

        cls._plugin_version = cls._read_plugin_version(plugin_root)

        log_dir = plugin_root / "log"
        log_dir.mkdir(parents=True, exist_ok=True)

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        pid = os.getpid()
        cls._log_file = log_dir / f"mtl_tools_{ts}_pid{pid}.log"

        cls._initialized = True

        cls._write_event(
            level="INFO",
            msg="Log session started",
            tool="system",
            class_name="LogUtils"
        )

    # ======================================================
    # API pública
    # ======================================================

    @classmethod
    def log(cls, msg: str, *, level="INFO", tool=None, class_name=None, **data):
        if not cls._initialized:
            return

        tool = tool or "unknown_tool"
        class_name = class_name or "UnknownClass"

        cls._write_event(level, msg, tool, class_name, data)

    @classmethod
    def debug(cls, msg: str, **kw):
        cls.log(msg, level="DEBUG", **kw)

    @classmethod
    def info(cls, msg: str, **kw):
        cls.log(msg, level="INFO", **kw)

    @classmethod
    def warning(cls, msg: str, **kw):
        cls.log(msg, level="WARNING", **kw)

    @classmethod
    def error(cls, msg: str, **kw):
        cls.log(msg, level="ERROR", **kw)

    @classmethod
    def exception(cls, exc: Exception, *, tool=None, class_name=None, **data):
        tb = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))

        tool = tool or "unknown_tool"
        class_name = class_name or "UnknownClass"

        data["exception"] = {
            "type": type(exc).__name__,
            "message": str(exc),
            "traceback": tb
        }

        cls.log(
            msg="Unhandled exception",
            level="ERROR",
            tool=tool,
            class_name=class_name,
            **data
        )

    # ======================================================
    # Internos
    # ======================================================

    @classmethod
    def _write_event(cls, level, msg, tool, class_name, data=None):
        # Garantir que nunca escrevemos None
        tool = tool or "unknown_tool"
        class_name = class_name or "UnknownClass"
        
        event = {
            "ts": datetime.now().isoformat(timespec="seconds"),
            "level": level,
            "plugin": cls._plugin_name,
            "plugin_version": cls._plugin_version,
            "session_id": cls._session_id,
            "pid": os.getpid(),
            "thread": threading.current_thread().name,
            "tool": tool,
            "class": class_name,
            "msg": msg,
            "data": data or {}
        }

        with LOG_FILE_LOCK:
            try:
                with open(cls._log_file, "a", encoding="utf-8") as f:
                    json.dump(event, f, ensure_ascii=False)
                    f.write("\n")
            except Exception:
                pass  # logger nunca quebra o plugin

    @staticmethod
    def _read_plugin_version(plugin_root: Path) -> str:
        meta = plugin_root / "metadata.txt"
        if not meta.exists():
            return "unknown"

        for line in meta.read_text(encoding="utf-8").splitlines():
            if line.startswith("version="):
                return line.split("=", 1)[1].strip()
        return "unknown"
