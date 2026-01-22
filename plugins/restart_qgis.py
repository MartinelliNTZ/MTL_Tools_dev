# -*- coding: utf-8 -*-
"""
Ferramenta: Salvar, Fechar e Reabrir Projeto
Autor: Matheus Martinelli
Parte do plugin: MTL Tools
"""

import os
import sys
import subprocess
import tempfile

from qgis.core import QgsProject, QgsApplication
from qgis.PyQt.QtWidgets import QMessageBox
from qgis.PyQt.QtCore import Qt,QCoreApplication


def _get_qgis_executable2():
    """Retorna o executável do QGIS (OSGeo4W ou Standalone)."""
    qgis_python = sys.executable
    base_dir = os.path.dirname(qgis_python)

    cand1 = os.path.join(base_dir, "qgis-bin.exe")
    cand2 = os.path.join(base_dir, "qgis.exe")

    if os.path.exists(cand1):
        return cand1
    if os.path.exists(cand2):
        return cand2
    return None
def _get_qgis_executable3():
    """Tenta localizar o executável do QGIS em ambientes OSGeo4W e Standalone."""

    # 1) Se o QGIS definir a variável de ambiente corretamente (Standalone ou OSGeo4W)
    prefix = os.getenv("QGIS_PREFIX_PATH")
    if prefix:
        cand1 = os.path.join(prefix, "bin", "qgis-bin.exe")
        cand2 = os.path.join(prefix, "bin", "qgis.exe")
        if os.path.exists(cand1):
            return cand1
        if os.path.exists(cand2):
            return cand2

    # 2) OSGeo4W padrão (QGIS 3.22+)
    osgeo_root = os.getenv("OSGEO4W_ROOT")
    if osgeo_root:
        cand = os.path.join(osgeo_root, "bin", "qgis-bin.exe")
        if os.path.exists(cand):
            return cand

        cand = os.path.join(osgeo_root, "bin", "qgis.exe")
        if os.path.exists(cand):
            return cand

    # 3) Standalone QGIS (instalador oficial)
    # Exemplo: C:\Program Files\QGIS 3.36.0\bin\qgis.exe
    python_exe = sys.executable
    base = os.path.dirname(python_exe)
    cand1 = os.path.join(base, "qgis-bin.exe")
    cand2 = os.path.join(base, "qgis.exe")

    if os.path.exists(cand1):
        return cand1
    if os.path.exists(cand2):
        return cand2
    
    # 4) Não encontrou
    return None
def _get_qgis_executable():
    """Obtém o executável real do QGIS diretamente do Qt (100% confiável)."""
    exe = QCoreApplication.applicationFilePath()
    if os.path.exists(exe):
        return exe
    return None


def _create_restart_script(project_path):
    """Cria o .bat temporário que reabre o QGIS com o mesmo projeto."""
    qgis_exec = _get_qgis_executable()
    if not qgis_exec:
        return None

    bat_path = os.path.join(tempfile.gettempdir(), "restart_qgis.bat")

    with open(bat_path, "w", encoding="utf-8") as f:
        f.write("@echo off\n")
        f.write("PING 127.0.0.1 -n 2 >NUL\n")
        f.write(f'start "" "{qgis_exec}" "{project_path}"\n')

    return bat_path


def run_restart_qgis(iface):
    """Fluxo principal da ferramenta."""
    project = QgsProject.instance()
    project_path = project.fileName()

    # 1) Verificar se o projeto está salvo
    if not project_path:
        msg = QMessageBox.warning(
            iface.mainWindow(),
            "Projeto não salvo",
            (
                "O projeto ainda não foi salvo.\n\n"
                "Para reiniciar o QGIS, é necessário salvar o arquivo.\n"
                "Deseja salvar agora?"
            ),
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
        )

        if msg == QMessageBox.Cancel:
            return

        if msg == QMessageBox.Yes:
            save_path, _ = iface.getSaveFileName(
                iface.mainWindow(),
                "Salvar Projeto",
                "",
                "Projetos QGIS (*.qgz)"
            )
            if not save_path:
                return

            project.write(save_path)
            project_path = save_path

        else:
            QMessageBox.information(
                iface.mainWindow(),
                "Ação cancelada",
                "Sem salvar o projeto, o QGIS não pode ser reaberto automaticamente."
            )
            return

    # 2) Gravar alterações antes de fechar
    project.write(project_path)

    # 3) Criar script .bat para reabrir QGIS
    bat_path = _create_restart_script(project_path)

    if not bat_path:
        QMessageBox.critical(
            iface.mainWindow(),
            "Erro",
            "Não foi possível encontrar o executável do QGIS.\n"
            "O reinício automático não será executado."
        )
        return

    
    def _run_bat():
        subprocess.Popen(bat_path, shell=True)

    app = QCoreApplication.instance()
    app.aboutToQuit.connect(_run_bat)

    iface.mainWindow().close()