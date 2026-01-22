# utils/log_cleanup_utils.py
from pathlib import Path

class LogCleanupUtils:
    """
    Limpeza explícita de logs antigos.
    """

    @staticmethod
    def keep_last_n(plugin_root: Path, keep: int = 10):
        log_dir = plugin_root / "log"
        if not log_dir.exists():
            return

        logs = sorted(log_dir.glob("*.log"), key=lambda p: p.stat().st_mtime, reverse=True)

        for old in logs[keep:]:
            try:
                old.unlink()
            except Exception:
                pass
