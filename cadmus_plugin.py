# -*- coding: utf-8 -*-
import sys
import traceback
from qgis.core import QgsApplication
from pathlib import Path
from .utils.ToolKeys import ToolKey
from .utils.QgisMessageUtil import QgisMessageUtil
from .core.config.LogUtils import LogUtils
from .i18n.TranslationManager import STR
from .core.config.PluginBootstrap import PluginBootstrap
from .core.ToolRegistry import ToolRegistry
from .core.MenuManager import MenuManager


class CadmusPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.provider = None
        self.logger = None
        self.tool_registry = None
        self.menu_manager = None
        self.TOOL_KEY = ToolKey.SYSTEM

    # =====================================================
    # INICIAR GUI E PROCESSING
    # =====================================================
    def initGui(self):

        locale = QgsApplication.locale()  # ex: 'pt_BR'
        plugin_root = Path(__file__).resolve().parent

        # Inicializar componentes críticos via PluginBootstrap
        bootstrap = PluginBootstrap(self.iface)
        self.provider = bootstrap.bootstrap(plugin_root)

        # Criar logger para CadmusPlugin
        self.logger = LogUtils(
            tool=self.TOOL_KEY, class_name="Cadmus", level=LogUtils.DEBUG
        )

        self.logger.info("Plugin inicializado")
        self.logger.info(f"Locale: {locale}. TM.STR: {STR.APP_NAME}")

        # -------------------------------
        # INTEGRAÇÃO COM NOVA ARQUITETURA
        # -------------------------------
        try:
            # Criar ToolRegistry com todas as ferramentas
            self.tool_registry = ToolRegistry(self.iface)
            tools = self.tool_registry.tools

            # Criar MenuManager para gerenciar menus e toolbar
            self.menu_manager = MenuManager(self.iface, tools, self.logger)

            # Criar menu principal e submenus
            self.menu_manager.create_menu()

            # Criar toolbar com botões dropdown
            self.logger.debug("Criando toolbar para o plugin")
            self.menu_manager.create_toolbar()

            # Popular menus com ferramentas ordenadas
            self.menu_manager.populate_menus()

            self.logger.info(f"Nova arquitetura integrada com sucesso. {self.menu_manager}. Registry{self.tool_registry.tools}.")
        except Exception as e:
            self.logger.error(f"Erro ao integrar nova arquitetura: {str(e)}")
            return

        # -------------------------






    # =====================================================
    # DESCARREGAR PLUGIN
    # =====================================================
    def unload(self):
        try:
            # Remover provider do Processing
            if self.provider:
                QgsApplication.processingRegistry().removeProvider(self.provider)
                self.logger.info("Processing Provider removido com sucesso")
        except Exception as e:
            self.logger.error(f"Erro ao remover Processing Provider: {str(e)}")

        try:
            # Descarregar MenuManager (remove menus e toolbar)
            if self.menu_manager:
                self.menu_manager.unload()
                self.logger.info("MenuManager descarregado com sucesso")
        except Exception as e:
            self.logger.error(f"Erro ao descarregar MenuManager: {str(e)}")

        self.logger.info("Plugin Cadmus descarregado")

    # =======FERRAMENTAS INSTANTANEAS DE SISTEMA=======
    # =================================================
    # EXECUTAR: Restart QGIS
    # =================================================
    def run_restart_qgis(self):
        try:
            from .plugins.RestartQgis import run_restart_qgis

            self.logger.info("Iniciando plugin: Restart QGIS")
            run_restart_qgis(self.iface)
            self.logger.info("Plugin Restart QGIS executado com sucesso")
        except Exception as e:
            self.logger.error(f"Erro ao executar Restart QGIS: {str(e)}")
            QgisMessageUtil.bar_critical(
                self.iface, f"Erro no plugin Restart QGIS:\n{str(e)}"
            )

    # ========FERRAMENTAS INSTANTANEAS======
    # ======================================
    # EXECUTAR: Calcular Campos Vetoriais
    # ======================================
    def run_vector_fields(self):
        try:
            from .plugins.VectorFieldsCalculationPlugin import (
                VectorFieldsCalculationPlugin,
            )

            self.logger.info("Iniciando plugin: Calcular Campos Vetoriais")
            # manter referência viva
            self.vector_field_plugin = VectorFieldsCalculationPlugin(self.iface)
            self.vector_field_plugin.run_vector_field()
            self.logger.info("Plugin Calcular Campos Vetoriais executado com sucesso")
        except Exception as e:
            self.logger.error(f"Erro ao executar Calcular Campos Vetoriais: {str(e)}")
            QgisMessageUtil.bar_critical(
                self.iface, f"Erro no plugin Calcular Campos Vetoriais:{str(e)}"
            )

    # =====================================================
    # EXECUTAR: Converter para Multipart
    # =====================================================
    def run_multpart(self):
        try:
            from .plugins.VectorMultipartPlugin import VectorMultipartPlugin

            self.logger.info("Iniciando plugin: Converter para Multipart")
            # manter referência viva
            self.vector_multpart_plugin = VectorMultipartPlugin(self.iface)
            self.vector_multpart_plugin.run_multpart()
            self.logger.info("Plugin Converter para Multipart executado com sucesso")
        except Exception as e:
            self.logger.error(f"Erro ao executar Converter para Multipart: {str(e)}")
            QgisMessageUtil.bar_critical(
                self.iface, f"Erro no plugin Converter para Multipart: {str(e)}"
            )

    # =====FERRAMENTAS INSTANTANEA COM JANELA DE RESULTADOS=

    # =====================================================
    # EXECUTAR: Obter Coordenadas ao Clicar no Mapa
    # =====================================================
    def run_coord_click(self):
        try:
            from .plugins.CoordClickTool import CoordClickTool

            self.logger.info("Ativando ferramenta: Capturar Coordenadas")
            self.coord_click_tool = CoordClickTool(self.iface)
            self.iface.mapCanvas().setMapTool(self.coord_click_tool)
            self.logger.info("Ferramenta Capturar Coordenadas ativada com sucesso")
        except Exception as e:
            self.logger.error(f"Erro ao ativar Capturar Coordenadas: {str(e)}")
            QgisMessageUtil.bar_critical(
                self.iface, f"Erro na ferramenta Capturar Coordenadas:{str(e)}"
            )

    # ===FERRAMENTAS DE JANELA COM SAIDA QGIS===============
    # =====================================================
    # EXECUTAR: Export All Layouts
    # =====================================================
    def run_export_layouts(self):
        try:
            from .plugins.ExportAllLayouts import run

            self.logger.info("Abrindo diálogo: Exportar todos os Layouts")
            self.export_dlg = run(self.iface)
            self.logger.info("Diálogo Exportar Layouts fechado")
        except Exception as e:
            self.logger.error(f"Erro ao executar Exportar Layouts: {str(e)}")
            QgisMessageUtil.bar_critical(
                self.iface, f"Erro no plugin Exportar Layouts: {str(e)}"
            )

    # =====================================================
    # EXECUTAR: Gerar Rastro Implemento (painel)
    # =====================================================
    def run_gerar_rastro(self):
        try:
            from .plugins.GenerateTrailPlugin import run

            self.logger.info("Abrindo diálogo: Gerar Rastro Implemento")
            self.gerar_rastro_dlg = run(self.iface)
            self.logger.info("Diálogo Gerar Rastro Implemento aberto com sucesso")
        except Exception as e:
            self.logger.error(f"Erro ao executar Gerar Rastro Implemento: {str(e)}")
            QgisMessageUtil.bar_critical(
                self.iface, f"Erro no plugin Gerar Rastro Implemento: {str(e)}"
            )

    # =====================================================
    # EXECUTAR: Logcat Tool
    # =====================================================
    def run_logcat(self):
        """
        Abre o Logcat com proteção MÁXIMA contra crashes.
        Qualquer erro será capturado e registrado em arquivo de log.
        """
        try:
            self.logger.info("=" * 60)
            self.logger.info("LOGCAT: Iniciando abertura de diálogo")

            # Import isolado
            try:
                from .plugins.logcat.logcat_plugin import run

                self.logger.info("LOGCAT: Módulo logcat_plugin importado")
            except ImportError as import_err:
                error_msg = f"Erro ao importar logcat_plugin: {str(import_err)}"
                self.logger.critical(error_msg)
                QgisMessageUtil.bar_critical(
                    self.iface, f"Erro de importação:\n{str(import_err)}"
                )
                return

            self.logger.info("Abrindo diálogo: Logcat - Viewer de Logs")

            # Execução com proteção adicional
            try:
                self.logcat_dlg = run(self.iface)
                self.logger.info(
                    "LOGCAT: Diálogo aberto com sucesso (sem crashes detectados)"
                )
                self.logger.info("=" * 60)
            except Exception as run_error:
                # Erro na execução do Logcat
                error_msg = (
                    f"LOGCAT: Erro ao executar logcat_plugin.run(): {str(run_error)}"
                )
                self.logger.critical(error_msg)
                error_trace = traceback.format_exc()
                self.logger.critical(f"Stack trace:\n{error_trace}")
                QgisMessageUtil.bar_critical(
                    self.iface, f"Erro ao abrir Logcat:\n{str(run_error)}"
                )
                self.logger.info("=" * 60)

        except Exception as outer_error:
            # Erro na própria função run_logcat
            error_msg = f"LOGCAT: Erro CRÍTICO em run_logcat(): {str(outer_error)}"
            try:
                self.logger.critical(error_msg)
                error_trace = traceback.format_exc()
                self.logger.critical(f"Stack trace:\n{error_trace}")
                self.logger.info("=" * 60)
            except Exception as e:
                print(error_msg, file=sys.stderr)
                QgisMessageUtil.bar_critical(
                    self.iface,
                    f"Erro crítico no Logcat:\n{str(outer_error)}. Error: {e}",
                )

    # =====================================================
    # EXECUTAR: Obter Coordenadas de Drone
    # =====================================================
    def run_drone_coords(self):
        try:
            from .plugins.DroneCoordinates import run

            self.logger.info("Abrindo diálogo: Obter Coordenadas de Drone")
            self.drone_cordinates_dlg = run(self.iface)
            self.logger.info("Diálogo Obter Coordenadas de Drone aberto com sucesso")
        except Exception as e:
            self.logger.error(f"Erro ao executar Obter Coordenadas de Drone: {str(e)}")
            QgisMessageUtil.bar_critical(
                self.iface, f"Erro no plugin Obter Coordenadas de Drone:\n{str(e)}"
            )

    # ====FERRAMENTAS DE JANELA SEM SAIDAS=================
    # =====================================================
    # EXECUTAR: Replace Text in Layouts
    # =====================================================
    def run_replace_layouts(self):
        try:
            from .plugins.ReplaceInLayouts import run

            self.logger.info("Abrindo diálogo: Substituir textos nos Layouts")
            self.replace_layouts_dlg = run(self.iface)
            self.logger.info("Diálogo Substituir Layouts aberto com sucesso")
        except Exception as e:
            self.logger.error(f"Erro ao executar Substituir Layouts: {str(e)}")
            QgisMessageUtil.bar_critical(
                self.iface, f"Erro no plugin Substituir Layouts:\n{str(e)}"
            )

    # =====================================================
    # EXECUTAR: Load Folder Layers
    # =====================================================
    def run_load_folder(self):
        try:
            from .plugins.LoadFolderLayers import run

            self.logger.info("Iniciando plugin: Carregar pasta de arquivos")
            self.load_folder_dlg = run(self.iface)
            self.logger.info("Plugin Carregar pasta de arquivos executado com sucesso")
        except Exception as e:
            self.logger.error(f"Erro ao executar Carregar pasta de arquivos: {str(e)}")
            QgisMessageUtil.bar_critical(
                self.iface, f"Erro no plugin Carregar pasta:\n{str(e)}"
            )

    # =====================================================
    # EXECUTAR: About Dialog
    # =====================================================
    def run_about_dialog(self):
        try:
            from .plugins.AboutDialog import run

            self.logger.info("Abrindo diálogo: Sobre o Cadmus")
            self.about_dlg = run(self.iface)
            self.logger.info("Diálogo Sobre Cadmus fechado")
        except Exception as e:
            self.logger.error(f"Erro ao executar Sobre o Cadmus: {str(e)}")
            QgisMessageUtil.bar_critical(
                self.iface, f"Erro ao abrir Sobre Cadmus:\n{str(e)}"
            )

    # =====================================================
    # EXECUTAR: Copiar Atributos entre Camadas
    # =====================================================
    def run_copy_atributes(self):
        try:
            from .plugins.CopyAttributesPlugin import run

            self.logger.info("Abrindo diálogo: Copiar Atributos")
            self.copy_attributes_dlg = run(self.iface)
            self.logger.info("Diálogo Copiar Atributos aberto com sucesso")
        except Exception as e:
            self.logger.error(f"Erro ao executar Copiar Atributos: {str(e)}")
            QgisMessageUtil.bar_critical(
                self.iface, f"Erro no plugin Copiar Atributos:\n{str(e)}"
            )

    # =====================================================
    # EXECUTAR: Configurações
    # =====================================================
    def run_settings(self):
        try:
            from .plugins.SettingsPlugin import run

            self.logger.info("Abrindo diálogo: Configurações")
            self.settings_dlg = run(self.iface)
            self.logger.info("Diálogo de configurações aberto com sucesso")
        except Exception as e:
            self.logger.error(f"Erro ao executar Configurações: {str(e)}")
            QgisMessageUtil.bar_critical(
                self.iface, f"Erro no diálogo de Configurações:\n{str(e)}"
            )
