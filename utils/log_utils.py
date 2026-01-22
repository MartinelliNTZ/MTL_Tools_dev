# utils/log_utils.py
import os
from datetime import datetime, timedelta

class LogUtilsOld:
    """
    Utilitário de logging para ferramentas do MTL Tools.
    Cria logs locais por ferramenta, com timestamp,
    e permite limpar logs antigos.
    """
    
    # Pasta raiz do projeto
    ROOT_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__),  ".."))
    # Pasta de logs: raiz/log
    BASE_FOLDER = os.path.join(ROOT_FOLDER, "log")

    @staticmethod
    def _ensure_folder():
        """Garante que a pasta de logs exista."""
        os.makedirs(LogUtilsOld.BASE_FOLDER, exist_ok=True)

    @staticmethod
    def log(tool_key: str, message: str):
        """
        Registra mensagem em arquivo de log da ferramenta.
        """
        LogUtilsOld._ensure_folder()

        date = datetime.now().strftime("%Y%m%d")
        time = datetime.now().strftime("%H:%M:%S")

        filename = f"{tool_key}_{date}.log"
        path = os.path.join(LogUtilsOld.BASE_FOLDER, filename)

        with open(path, "a", encoding="utf-8") as f:
            f.write(f"[{time}] {message}\n")

    @staticmethod
    def exception(tool_key: str, exc: Exception):
        """
        Registra exceções de forma padronizada.
        """
        LogUtilsOld.log(tool_key, f"EXCEPTION: {repr(exc)}")
        import traceback
        tb = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
        LogUtilsOld.log(tool_key, tb)

    @staticmethod
    def clear_old_logs(intervalo_coleta: int = 10):
        """
        Limpa logs mais antigos que 'intervalo_coleta' dias.
        """
        LogUtilsOld._ensure_folder()
        agora = datetime.now()
        limite = agora - timedelta(days=intervalo_coleta)

        for arquivo in os.listdir(LogUtilsOld.BASE_FOLDER):
            path = os.path.join(LogUtilsOld.BASE_FOLDER, arquivo)
            if os.path.isfile(path):
                data_modificacao = datetime.fromtimestamp(os.path.getmtime(path))
                if data_modificacao < limite:
                    os.remove(path)
                    print(f"Removido log antigo: {arquivo}")
