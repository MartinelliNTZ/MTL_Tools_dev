# -*- coding: utf-8 -*-
import sys
import traceback
from .model.Tool import Tool
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

    # Categorias de ferramentas
    SYSTEM = "SYSTEM"  # 1
    LAYOUTS = "LAYOUTS"  # 2
    FOLDER = "FOLDER"  # 3
    VECTOR = "VECTOR"  # 4
    AGRICULTURE = "AGRICULTURE"  # 5
    RASTER = "RASTER"  # 6

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
            name="Exportar todos os Layouts",
            icon=im.icon(im.EXPORT_ALL_LAYOUTS),
            category=self.LAYOUTS,
            tool_type=self.DIALOG,
            main_action=True,
            executor=self.run_export_layouts,
            tooltip="Exporta todos os Layouts do projeto para arquivos PDF ou imagens.",
            order=10,
            show_in_toolbar=True,
        )
        tools.append(export_layouts)
        print(f"ToolRegistry: added {export_layouts.name} category {export_layouts.category} main {export_layouts.main_action}")

        replace_layouts = Tool(
            name="Substituir textos nos Layouts",
            icon=im.icon(im.REPLACE_IN_LAYOUTS),
            category=self.LAYOUTS,
            tool_type=self.DIALOG,
            executor=self.run_replace_layouts,
            tooltip="Substitui textos em massa nos Layouts do projeto.\n"
                    "Permite criar um mapa de substituição a partir de uma camada vetorial ou tabela, onde um campo é usado para identificar os Layouts e outro campo é usado para o novo valor a ser inserido.\n"
                    "Útil para atualizar informações como títulos, legendas ou rótulos em múltiplos Layouts de forma rápida e consistente.",
            order=20,
            show_in_toolbar=True,
        )
        tools.append(replace_layouts)

        # =====================================================
        # SYSTEM (Ordem: Restart=10, Logcat=20, Settings=30, About=40)
        # =====================================================

        restart_qgis = Tool(
            name="Salvar, Fechar e Reabrir Projeto",
            icon=im.icon(im.RESTART_QGIS),
            category=self.SYSTEM,
            tool_type=self.INSTANT,
            main_action=True,
            executor=self.run_restart_qgis,
            tooltip="Salva o projeto atual, fecha o QGIS e reabre o mesmo projeto automaticamente.\n"
                    "Útil para resolver travamentos, bugs visuais ou de renderização sem perder o trabalho.",
            order=10,
            show_in_toolbar=True,
        )
        tools.append(restart_qgis)

        logcat = Tool(
            name="Logcat Viewer",
            icon=im.icon(im.LOGCAT),
            category=self.SYSTEM,
            tool_type=self.DIALOG,
            executor=self.run_logcat,
            tooltip="Abre o Logcat, uma ferramenta de visualização dos logs do plugin Cadmus.",
            order=20,
            show_in_toolbar=True,
        )
        tools.append(logcat)

        settings = Tool(
            name="Configurações",
            icon=im.icon(im.SETTINGS),
            category=self.SYSTEM,
            tool_type=self.DIALOG,
            executor=self.run_settings,
            tooltip="Configurações do plugin Cadmus.",
            order=30,
            show_in_toolbar=True,
        )
        tools.append(settings)

        about = Tool(
            name="Sobre o Cadmus",
            icon=im.icon(im.ABOUT),
            category=self.SYSTEM,
            tool_type=self.DIALOG,
            executor=self.run_about_dialog,
            tooltip="Informações sobre o plugin Cadmus.",
            order=40,
            show_in_toolbar=True,
        )
        tools.append(about)

        # =====================================================        # FOLDER (Ordem: Load=10)
        # =====================================================

        load_folder = Tool(
            name="Carregar Pasta de Arquivos",
            icon=im.icon(im.LOAD_FOLDER_LAYER),
            category=self.FOLDER,
            tool_type=self.DIALOG,
            main_action=True,
            executor=self.run_load_folder,
            tooltip="Carrega em massa uma pasta de arquivos como camadas no QGIS.",
            order=10,
            show_in_toolbar=True,
        )
        tools.append(load_folder)
        print(f"ToolRegistry: added {load_folder.name} category {load_folder.category} main {load_folder.main_action}")

        # =====================================================        # FOLDER (Ordem: Load Folder=10)
        # =====================================================

        load_folder = Tool(
            name="Carregar pasta de arquivos",
            icon=im.icon(im.LOAD_FOLDER_LAYER),
            category=self.FOLDER,
            tool_type=self.DIALOG,
            executor=self.run_load_folder,
            tooltip="Carrega em massa uma pasta de arquivos como camadas no QGIS.",
            order=10,
            show_in_toolbar=True,
        )
        tools.append(load_folder)

        # =====================================================
        # VECTOR (Ordem: Fields=10, Coords=20, Pasta=30, Multipart=40, Copy=50)
        # =====================================================

        vector_fields = Tool(
            name="Calcular Campos Vetoriais",
            icon=im.icon(im.VECTOR_FIELD),
            category=self.VECTOR,
            tool_type=self.INSTANT,
            main_action=True,
            executor=self.run_vector_fields,
            tooltip="Calcula automaticamente campos: Área, Comprimento ou X/Y\n"
                    "Selecione uma camada vetorial ativa e execute a ferramenta\n"
                    "para adicionar os campos calculados.",
            order=10,
            show_in_toolbar=True,
        )
        tools.append(vector_fields)

        coord_click = Tool(
            name="Capturar Coordenadas",
            icon=im.icon(im.COORD_CLICK_TOOL),
            category=self.VECTOR,
            tool_type=self.MAP_TOOL,
            executor=self.run_coord_click,
            tooltip="Clique no mapa para consultar coordenadas do ponto.\n"
                    "A ferramenta abre um dialogo com WGS84, UTM,\n"
                    "altitude aproximada e endereco estimado,\n"
                    "alem de opcoes para copiar as informacoes.",
            order=20,
            show_in_toolbar=True,
        )
        tools.append(coord_click)


        multipart = Tool(
            name="Converter Multipart",
            icon=im.icon(im.VECTOR_MULTPART),
            category=self.VECTOR,
            tool_type=self.INSTANT,
            executor=self.run_multpart,
            tooltip="Promove feições para o tipo multiparte.\n"
                    "Selecione uma camada vetorial ativa e execute a ferramenta\n"
                    "para promover as feições.",
            order=40,
            show_in_toolbar=True,
        )
        tools.append(multipart)

        copy_attributes = Tool(
            name="Copiar Atributos",
            icon=im.icon(im.COPY_ATTRIBUTES),
            category=self.VECTOR,
            tool_type=self.DIALOG,
            executor=self.run_copy_atributes,
            tooltip="Copia atributos entre camadas.",
            order=50,
            show_in_toolbar=True,
        )
        tools.append(copy_attributes)

        # =====================================================
        # AGRICULTURE (Ordem: Drone=10, Trail=20)
        # =====================================================

        drone_coords = Tool(
            name="Obter Coordenadas de Drone",
            icon=im.icon(im.DRONE_COORDINATES),
            category=self.AGRICULTURE,
            tool_type=self.DIALOG,
            main_action=True,
            executor=self.run_drone_coords,
            tooltip="Le arquivos MRK de drone para gerar pontos das fotos\n"
                    "e uma linha com o rastro do voo.\n"
                    "Pode cruzar os pontos com metadados das imagens,\n"
                    "salvar os resultados e aplicar estilos QML.",
            order=10,
            show_in_toolbar=True,
        )
        tools.append(drone_coords)

        gerar_rastro = Tool(
            name="Gerar Rastro Implemento",
            icon=im.icon(im.GENERATE_TRAIL),
            category=self.AGRICULTURE,
            tool_type=self.DIALOG,
            executor=self.run_gerar_rastro,
            tooltip="Gera um rastro do movimento de um implemento agrícola com base em uma linha.",
            order=20,
            show_in_toolbar=True,
        )
        tools.append(gerar_rastro)

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

