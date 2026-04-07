# -*- coding: utf-8 -*-
import sys
import traceback
from ..model.Tool import Tool
from ...resources.IconManager import IconManager as im
from .LogUtils import LogUtils
from ...utils.ToolKeys import ToolKey
from ...utils.QgisMessageUtil import QgisMessageUtil
from ...i18n.TranslationManager import STR
from ...utils.StringManager import StringManager
from ..enum import ToolTypeEnum


class ToolRegistry:
    # Tipos de ferramenta (não usar enum separado conforme requisito)
    SYSTEM, LAYOUTS, FOLDER, VECTOR, AGRICULTURE, RASTER = (
        StringManager.MENU_CATEGORIES.keys()
    )

    def __init__(self, iface):
        self.iface = iface
        self.logger = LogUtils(tool=ToolKey.SYSTEM, class_name="ToolRegistry")
        self.tools = self._create_tool_list()

    def _create_tool_list(self):
        tools = []

        # =====================================================
        # LAYOUTS (Ordem: Export=10, Replace=20)
        # =====================================================

        export_layouts = Tool(
            name=STR.EXPORT_ALL_LAYOUTS_TITLE,
            icon=im.icon(im.EXPORT_ALL_LAYOUTS),
            category=self.LAYOUTS,
            tool_type=ToolTypeEnum.DIALOG,
            main_action=True,
            executor=self.run_export_layouts,
            tooltip=STR.EXPORT_ALL_LAYOUTS_TOOLTIP,
            order=10,
            show_in_toolbar=True,
        )
        tools.append(export_layouts)

        replace_layouts = Tool(
            name=STR.REPLACE_IN_LAYOUTS_TITLE,
            icon=im.icon(im.REPLACE_IN_LAYOUTS),
            category=self.LAYOUTS,
            tool_type=ToolTypeEnum.DIALOG,
            executor=self.run_replace_layouts,
            tooltip=STR.REPLACE_IN_LAYOUTS_TOOLTIP,
            order=20,
            show_in_toolbar=True,
        )
        tools.append(replace_layouts)

        # =====================================================
        # SYSTEM (Ordem: Restart=10, Logcat=20, Settings=30, About=40)
        # =====================================================

        restart_qgis = Tool(
            name=STR.RESTART_QGIS_TITLE,
            icon=im.icon(im.RESTART_QGIS),
            category=self.SYSTEM,
            tool_type=ToolTypeEnum.INSTANT,
            main_action=True,
            executor=self.run_restart_qgis,
            tooltip=STR.RESTART_QGIS_TOOLTIP,
            order=10,
            show_in_toolbar=True,
        )
        tools.append(restart_qgis)

        logcat = Tool(
            name=STR.LOGCAT_TITLE,
            icon=im.icon(im.LOGCAT),
            category=self.SYSTEM,
            tool_type=ToolTypeEnum.DIALOG,
            executor=self.run_logcat,
            tooltip=STR.LOGCAT_TOOLTIP,
            order=20,
            show_in_toolbar=True,
        )
        tools.append(logcat)

        settings = Tool(
            name=STR.SETTINGS_TITLE,
            icon=im.icon(im.SETTINGS),
            category=self.SYSTEM,
            tool_type=ToolTypeEnum.DIALOG,
            executor=self.run_settings,
            tooltip=STR.SETTINGS_TOOLTIP,
            order=30,
            show_in_toolbar=True,
        )
        tools.append(settings)

        about = Tool(
            name=STR.ABOUT_CADMUS,
            icon=im.icon(im.ABOUT),
            category=self.SYSTEM,
            tool_type=ToolTypeEnum.DIALOG,
            executor=self.run_about_dialog,
            tooltip=STR.ABOUT_DIALOG_TOOLTIP,
            order=40,
            show_in_toolbar=True,
        )
        tools.append(about)

        # =====================================================
        # FOLDER (Ordem: Load=10)
        # =====================================================

        load_folder = Tool(
            name=STR.LOAD_FOLDER_LAYERS_TITLE,
            icon=im.icon(im.LOAD_FOLDER_LAYER),
            category=self.FOLDER,
            tool_type=ToolTypeEnum.DIALOG,
            main_action=True,
            executor=self.run_load_folder,
            tooltip=STR.LOAD_FOLDER_LAYERS_TOOLTIP,
            order=10,
            show_in_toolbar=True,
        )
        tools.append(load_folder)

        create_project = Tool(
            name="Novo Projeto",
            icon=im.icon(im.LOAD_FOLDER_LAYER),
            category=self.FOLDER,
            tool_type=ToolTypeEnum.INSTANT,
            executor=self.run_create_project,
            tooltip="Cria uma estrutura de projeto com pasta, arquivo .qgz, vectors e rasters.",
            order=15,
            show_in_toolbar=True,
        )
        tools.append(create_project)

        vector_to_svg = Tool(
            name=STR.VECTOR_TO_SVG_TITLE,
            icon=im.icon(im.CADMUS_ICON),
            category=self.FOLDER,
            tool_type=ToolTypeEnum.DIALOG,
            executor=self.run_vector_to_svg,
            tooltip=STR.VECTOR_TO_SVG_TOOLTIP,
            order=20,
            show_in_toolbar=True,
        )
        tools.append(vector_to_svg)

        # =====================================================
        # VECTOR (Ordem: Fields=10, Coords=20, Pasta=30, Multipart=40, Copy=50)
        # =====================================================

        vector_fields = Tool(
            name=STR.VECTOR_FIELDS_TITLE,
            icon=im.icon(im.VECTOR_FIELD),
            category=self.VECTOR,
            tool_type=ToolTypeEnum.INSTANT,
            main_action=True,
            executor=self.run_vector_fields,
            tooltip=STR.VECTOR_FIELDS_TOOLTIP,
            order=10,
            show_in_toolbar=True,
        )
        tools.append(vector_fields)

        remove_kml_fields = Tool(
            name=STR.REMOVE_KML_FIELDS_TITLE,
            icon=im.icon(im.CADMUS_ICON),
            category=self.VECTOR,
            tool_type=ToolTypeEnum.INSTANT,
            executor=self.run_remove_kml_fields,
            tooltip=STR.REMOVE_KML_FIELDS_TOOLTIP,
            order=15,
            show_in_toolbar=True,
        )
        tools.append(remove_kml_fields)

        coord_click = Tool(
            name=STR.COORD_CLICK_TOOL_TITLE,
            icon=im.icon(im.COORD_CLICK_TOOL),
            category=self.VECTOR,
            tool_type=ToolTypeEnum.MAP_TOOL,
            executor=self.run_coord_click,
            tooltip=STR.COORD_CLICK_TOOL_TOOLTIP,
            order=20,
            show_in_toolbar=True,
        )
        tools.append(coord_click)

        multipart = Tool(
            name=STR.CONVERTER_MULTIPART_TITLE,
            icon=im.icon(im.VECTOR_MULTPART),
            category=self.VECTOR,
            tool_type=ToolTypeEnum.INSTANT,
            executor=self.run_multpart,
            tooltip=STR.CONVERTER_MULTIPART_TOOLTIP,
            order=40,
            show_in_toolbar=True,
        )
        tools.append(multipart)

        copy_attributes = Tool(
            name=STR.COPY_ATTRIBUTES_TITLE,
            icon=im.icon(im.COPY_ATTRIBUTES),
            category=self.VECTOR,
            tool_type=ToolTypeEnum.DIALOG,
            executor=self.run_copy_atributes,
            tooltip=STR.COPY_ATTRIBUTES_TOOLTIP,
            order=50,
            show_in_toolbar=True,
        )
        tools.append(copy_attributes)

        # =====================================================
        # AGRICULTURE (Ordem: Drone=10, Trail=20)
        # =====================================================

        drone_coords = Tool(
            name=STR.DRONE_COORDINATES_TITLE,
            icon=im.icon(im.DRONE_COORDINATES),
            category=self.AGRICULTURE,
            tool_type=ToolTypeEnum.DIALOG,
            main_action=True,
            executor=self.run_drone_coords,
            tooltip=STR.DRONE_COORDINATES_TOOLTIP,
            order=10,
            show_in_toolbar=True,
        )
        tools.append(drone_coords)

        gerar_rastro = Tool(
            name=STR.GENERATE_TRAIL_TITLE,
            icon=im.icon(im.GENERATE_TRAIL),
            category=self.AGRICULTURE,
            tool_type=ToolTypeEnum.DIALOG,
            executor=self.run_gerar_rastro,
            tooltip=STR.GENERATE_TRAIL_TOOLTIP,
            order=20,
            show_in_toolbar=True,
        )
        tools.append(gerar_rastro)

        # =====================================================
        # RASTER (Ordem: Mass Clipper=10)
        # =====================================================

        raster_mass_clipper = Tool(
            name=STR.RASTER_MASS_CLIPPER_TITLE,
            icon=im.icon(im.RASTER_MASS_CLIPPER),
            category=self.RASTER,
            tool_type=ToolTypeEnum.PROCESSING,
            main_action=True,
            executor=self.run_raster_mass_clipper,
            tooltip=STR.RASTER_MASS_CLIPPER_TOOLTIP,
            order=10,
            show_in_toolbar=True,
        )
        tools.append(raster_mass_clipper)

        raster_mass_sampler = Tool(
            name=STR.RASTER_MASS_SAMPLER_TITLE,
            icon=im.icon(im.RASTER_MASS_SAMPLER),
            category=self.RASTER,
            tool_type=ToolTypeEnum.PROCESSING,
            executor=self.run_raster_mass_sampler,
            tooltip=STR.RASTER_MASS_SAMPLER_TOOLTIP,
            order=20,
            show_in_toolbar=True,
        )
        tools.append(raster_mass_sampler)

        return tools

    def get_tools(self):
        return list(self.tools)

    # =======FERRAMENTAS INSTANTANEAS DE SISTEMA=======
    # =================================================
    # EXECUTAR: Restart QGIS
    # =================================================
    def run_restart_qgis(self):
        try:
            from ...plugins.RestartQgis import run_restart_qgis

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
            from ...plugins.VectorFieldsCalculationPlugin import (
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
            from ...plugins.VectorMultipartPlugin import VectorMultipartPlugin

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

    # =====================================================
    # EXECUTAR: Remover Campos KML
    # =====================================================
    def run_remove_kml_fields(self):
        try:
            from ...plugins.RemoveKmlFieldsPlugin import RemoveKmlFieldsPlugin

            self.logger.info("Iniciando plugin: Remover Campos KML")
            self.remove_kml_fields_plugin = RemoveKmlFieldsPlugin(self.iface)
            self.remove_kml_fields_plugin.run_remove_kml_fields()
            self.logger.info("Plugin Remover Campos KML executado com sucesso")
        except Exception as e:
            self.logger.error(f"Erro ao executar Remover Campos KML: {str(e)}")
            QgisMessageUtil.bar_critical(
                self.iface, f"Erro no plugin Remover Campos KML: {str(e)}"
            )

    # =====FERRAMENTAS INSTANTANEA COM JANELA DE RESULTADOS=

    # =====================================================
    # EXECUTAR: Obter Coordenadas ao Clicar no Mapa
    # =====================================================
    def run_coord_click(self):
        try:
            from ...plugins.CoordClickTool import CoordClickTool

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
            from ...plugins.ExportAllLayouts import run

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
            from ...plugins.GenerateTrailPlugin import run

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
                from ...plugins.logcat.logcat_plugin import run

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
            from ...plugins.DroneCoordinates import run

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
            from ...plugins.ReplaceInLayouts import run

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
            from ...plugins.LoadFolderLayers import run

            self.logger.info("Iniciando plugin: Carregar pasta de arquivos")
            self.load_folder_dlg = run(self.iface)
            self.logger.info("Plugin Carregar pasta de arquivos executado com sucesso")
        except Exception as e:
            self.logger.error(f"Erro ao executar Carregar pasta de arquivos: {str(e)}")
            QgisMessageUtil.bar_critical(
                self.iface, f"Erro no plugin Carregar pasta:\n{str(e)}"
            )

    # =====================================================
    # EXECUTAR: Novo Projeto
    # =====================================================
    def run_create_project(self):
        try:
            from ...plugins.CreateProjectPlugin import run

            self.logger.info("Iniciando plugin: Novo Projeto")
            self.create_project_plugin = run(self.iface)
            self.logger.info("Plugin Novo Projeto executado com sucesso")
        except Exception as e:
            self.logger.error(f"Erro ao executar Novo Projeto: {str(e)}")
            QgisMessageUtil.bar_critical(
                self.iface, f"Erro no plugin Novo Projeto:\n{str(e)}"
            )

    # =====================================================
    # EXECUTAR: Vector To SVG
    # =====================================================
    def run_vector_to_svg(self):
        try:
            from ...plugins.VectorToSvgPlugin import run

            self.logger.info("Abrindo diálogo: VectorToSvgPlugin")
            self.vector_to_svg_dlg = run(self.iface)
            self.logger.info("Diálogo VectorToSvgPlugin aberto com sucesso")
        except Exception as e:
            self.logger.error(f"Erro ao executar VectorToSvgPlugin: {str(e)}")
            QgisMessageUtil.bar_critical(
                self.iface, f"Erro no plugin VectorToSvgPlugin:\n{str(e)}"
            )

    # =====================================================
    # EXECUTAR: Raster Mass Clipper (Processing)
    # =====================================================
    def run_raster_mass_clipper(self):
        try:
            import processing

            algorithm_id = "cadmus:raster_mass_clipper"
            self.logger.info(
                f"Abrindo dialogo do Processing para algoritmo: {algorithm_id}"
            )
            processing.execAlgorithmDialog(algorithm_id, {})
            self.logger.info(
                "Dialogo do Raster Mass Clipper aberto com sucesso pelo provider"
            )
        except Exception as e:
            self.logger.error(f"Erro ao executar Raster Mass Clipper: {str(e)}")
            QgisMessageUtil.bar_critical(
                self.iface,
                f"Erro ao abrir Raster Mass Clipper no Processing:\n{str(e)}",
            )

    # =====================================================
    # EXECUTAR: Raster Mass Sampler (Processing)
    # =====================================================
    def run_raster_mass_sampler(self):
        try:
            import processing

            algorithm_id = "cadmus:raster_mass_sampler"
            self.logger.info(
                f"Abrindo dialogo do Processing para algoritmo: {algorithm_id}"
            )
            processing.execAlgorithmDialog(algorithm_id, {})
            self.logger.info(
                "Dialogo do Raster Mass Sampler aberto com sucesso pelo provider"
            )
        except Exception as e:
            self.logger.error(f"Erro ao executar Raster Mass Sampler: {str(e)}")
            QgisMessageUtil.bar_critical(
                self.iface,
                f"Erro ao abrir Raster Mass Sampler no Processing:\n{str(e)}",
            )

    # =====================================================
    # EXECUTAR: About Dialog
    # =====================================================
    def run_about_dialog(self):
        try:
            from ...plugins.AboutDialog import run

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
            from ...plugins.CopyAttributesPlugin import run

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
            from ...plugins.SettingsPlugin import run

            self.logger.info("Abrindo diálogo: Configurações")
            self.settings_dlg = run(self.iface)
            self.logger.info("Diálogo de configurações aberto com sucesso")
        except Exception as e:
            self.logger.error(f"Erro ao executar Configurações: {str(e)}")
            QgisMessageUtil.bar_critical(
                self.iface, f"Erro no diálogo de Configurações:\n{str(e)}"
            )
