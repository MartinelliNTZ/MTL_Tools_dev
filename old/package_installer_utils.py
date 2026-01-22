import os
import subprocess
import sys


class PackageInstallerUtils:

    @staticmethod
    def is_package_installed(module_name):
        try:
            __import__(module_name)
            return True
        except ImportError:
            return False

    @staticmethod
    def _get_qgis_python():
        """
        Retorna o python.exe correto do QGIS,
        evitando sys.executable que aponta para qgis-bin.exe
        """

        # 1) tenta o Python que está executando os módulos
        base = os.path.dirname(sys.executable)

        # casos comuns no Windows QGIS
        candidates = [
            os.path.join(base, "python.exe"),
            os.path.join(base, "python-qgis.exe"),
        ]

        for c in candidates:
            if os.path.exists(c):
                return c

        # fallback: usa sys.executable mesmo assim
        return sys.executable

    @staticmethod
    def install_package(package_name):

        python_path = PackageInstallerUtils._get_qgis_python()

        cmd = [
            python_path,
            "-m",
            "pip",
            "install",
            package_name
        ]

        try:
            proc = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                shell=False
            )

            if proc.returncode == 0:
                return True, proc.stdout

            return False, proc.stderr

        except Exception as e:
            return False, str(e)
