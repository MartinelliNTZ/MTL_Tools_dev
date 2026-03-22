# -*- coding: utf-8 -*-
import sys
import traceback
from .model.Tool import Tool
from .MenuManager import MenuManager
from ..resources.IconManager import IconManager as im
from .config.LogUtils import LogUtils
from ..utils.ToolKeys import ToolKey
from ..utils.QgisMessageUtil import QgisMessageUtil


class ToolRegistry:
    # Tipos de ferramenta (não usar enum separado conforme requisito)
    INSTANT = "INSTANT"
    DIALOG = "DIALOG"
    MAP_TOOL = "MAP_TOOL"
    BACKGROUND = "BACKGROUND"

    def __init__(self, iface):
        self.iface = iface
        self.logger = LogUtils(tool=ToolKey.SYSTEM, class_name="ToolRegistry")
        self.tools = self._create_tool_list()

    def _create_tool_list(self):
        tools = []

        export_layouts = Tool(
            name="Exportar todos os Layouts",
            icon=im.icon(im.EXPORT_ALL_LAYOUTS),
            category=MenuManager.LAYOUTS,
            tool_type=self.DIALOG,
            main_action=True,
            executor=self.run_export_layouts,
            executor_name="run_export_layouts",
            tooltip="Exporta todos os Layouts do projeto para arquivos PDF ou imagens",
        )
        tools.append(export_layouts)

        replace_layouts = Tool(
            name="Substituir textos nos Layouts",
            icon=im.icon(im.REPLACE_IN_LAYOUTS),
            category=MenuManager.LAYOUTS,
            tool_type=self.DIALOG,
            executor=self.run_replace_layouts,
            executor_name="run_replace_layouts",
            tooltip="Substitui textos em massa nos Layouts do projeto",
        )
        tools.append(replace_layouts)

        restart_qgis = Tool(
            name="Salvar, Fechar e Reabrir Projeto",
            icon=im.icon(im.RESTART_QGIS),
            category=MenuManager.SYSTEM,
            tool_type=self.INSTANT,
            main_action=True,
            executor=self.run_restart_qgis,
            executor_name="run_restart_qgis",
            tooltip="Salva, fecha e reabre projeto automaticamente",
        )
        tools.append(restart_qgis)

        load_folder = Tool(
            name="Carregar pasta de arquivos",
            icon=im.icon(im.LOAD_FOLDER_LAYER),
            category=MenuManager.VECTOR,
            tool_type=self.DIALOG,
            executor=self.run_load_folder,
            executor_name="run_load_folder",
            tooltip="Carrega uma pasta de arquivos como camadas",
        )
        tools.append(load_folder)

        gerar_rastro = Tool(
            name="Gerar Rastro Implemento",
            icon=im.icon(im.GENERATE_TRAIL),
            category=MenuManager.AGRICULTURE,
            tool_type=self.DIALOG,
            executor=self.run_gerar_rastro,
            executor_name="run_gerar_rastro",
            tooltip="Gera rastro de implemento agrícola",
        )
        tools.append(gerar_rastro)

        about = Tool(
            name="Sobre o Cadmus",
            icon=im.icon(im.ABOUT),
            category=MenuManager.SYSTEM,
            tool_type=self.DIALOG,
            executor=self.run_about_dialog,
            executor_name="run_about_dialog",
            tooltip="Informações sobre o plugin Cadmus",
        )
        tools.append(about)

        coord_click = Tool(
            name="Capturar Coordenadas",
            icon=im.icon(im.COORD_CLICK_TOOL),
            category=MenuManager.VECTOR,
            tool_type=self.INSTANT,
            executor=self.run_coord_click,
            executor_name="run_coord_click",
            tooltip="Captura coordenadas ao clicar no mapa",
        )
        tools.append(coord_click)

        vector_fields = Tool(
            name="Calcular Campos Vetoriais",
            icon=im.icon(im.VECTOR_FIELD),
            category=MenuManager.VECTOR,
            tool_type=self.INSTANT,
            main_action=True,
            executor=self.run_vector_fields,
            executor_name="run_vector_fields",
            tooltip="Calcula campos vetoriais automaticamente",
        )
        tools.append(vector_fields)

        drone_coords = Tool(
            name="Obter Coordenadas de Drone",
            icon=im.icon(im.DRONE_COORDINATES),
            category=MenuManager.AGRICULTURE,
            tool_type=self.DIALOG,
            executor=self.run_drone_coords,
            executor_name="run_drone_coords",
            tooltip="Gera coordenadas a partir de fotos de drone",
        )
        tools.append(drone_coords)

        multipart = Tool(
            name="Converter Multipart",
            icon=im.icon(im.VECTOR_MULTPART),
            category=MenuManager.VECTOR,
            tool_type=self.INSTANT,
            executor=self.run_multpart,
            executor_name="run_multpart",
            tooltip="Converte feições em multipart",
        )
        tools.append(multipart)

        copy_attributes = Tool(
            name="Copiar Atributos",
            icon=im.icon(im.COPY_ATTRIBUTES),
            category=MenuManager.VECTOR,
            tool_type=self.DIALOG,
            executor=self.run_copy_atributes,
            executor_name="run_copy_atributes",
            tooltip="Copia atributos entre camadas",
        )
        tools.append(copy_attributes)

        logcat = Tool(
            name="Logcat Viewer",
            icon=im.icon(im.LOGCAT),
            category=MenuManager.SYSTEM,
            tool_type=self.DIALOG,
            executor=self.run_logcat,
            executor_name="run_logcat",
            tooltip="Visualizador de logs Cadmus",
        )
        tools.append(logcat)

        settings = Tool(
            name="Configurações",
            icon=im.icon(im.SETTINGS),
            category=MenuManager.SYSTEM,
            tool_type=self.DIALOG,
            executor=self.run_settings,
            executor_name="run_settings",
            tooltip="Configurações do plugin Cadmus",
        )
        tools.append(settings)

        return tools

    def get_tools(self):
        return list(self.tools)

    # =======FERRAMENTAS INSTANTANEAS DE SISTEMA=======
    # =================================================
    # EXECUTAR: Restart QGIS
    # =================================================
    def run_restart_qgis(self):
        try:
            from ..plugins.RestartQgis import run_restart_qgis

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
            from ..plugins.VectorFieldsCalculationPlugin import (
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
            from ..plugins.VectorMultipartPlugin import VectorMultipartPlugin

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
            from ..plugins.CoordClickTool import CoordClickTool

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
            from ..plugins.ExportAllLayouts import run

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
            from ..plugins.GenerateTrailPlugin import run

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
                from ..plugins.logcat.logcat_plugin import run

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
            from ..plugins.DroneCoordinates import run

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
            from ..plugins.ReplaceInLayouts import run

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
            from ..plugins.LoadFolderLayers import run

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
            from ..plugins.AboutDialog import run

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
            from ..plugins.CopyAttributesPlugin import run

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
            from ..plugins.SettingsPlugin import run

            self.logger.info("Abrindo diálogo: Configurações")
            self.settings_dlg = run(self.iface)
            self.logger.info("Diálogo de configurações aberto com sucesso")
        except Exception as e:
            self.logger.error(f"Erro ao executar Configurações: {str(e)}")
            QgisMessageUtil.bar_critical(
                self.iface, f"Erro no diálogo de Configurações:\n{str(e)}"
            )
