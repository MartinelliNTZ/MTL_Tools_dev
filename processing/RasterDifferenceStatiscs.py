# -*- coding: utf-8 -*-
import os
import itertools
from ..core.config.LogUtils import LogUtils
import processing

from qgis.core import (
    QgsRasterLayer,
    QgsProcessingParameterFolderDestination,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterBoolean,
    QgsProcessing,
    QgsProcessingException,
)
from qgis.analysis import QgsRasterCalculator, QgsRasterCalculatorEntry
from ..utils.ToolKeys import ToolKey
from .BaseProcessingAlgorithm import BaseProcessingAlgorithm


class RasterDifferenceStatiscs(BaseProcessingAlgorithm):
    TOOL_KEY = ToolKey.RASTER_MASS_CLIPPER
    ALGORITHM_NAME = "raster_difference_statistics"
    ALGORITHM_DISPLAY_NAME = "Processar Diferença de Rasters"
    ALGORITHM_GROUP = BaseProcessingAlgorithm.GROUP_RASTER
    ICON = "cadmus_icon.ico"
    logger = LogUtils(
        tool="raster_diff_task", class_name="RasterDiffTask", level="DEBUG"
    )

    INPUT_FOLDER = "INPUT_FOLDER"
    OUTPUT_FOLDER = "OUTPUT_FOLDER"
    INPUT_LAYERS = "INPUT_LAYERS"
    DISPLAY_HELP = "DISPLAY_HELP"

    def initAlgorithm(self, config=None):
        self.logger.debug("initAlgorithm initialized")
        self.load_preferences()

        self.addParameter(
            QgsProcessingParameterFolderDestination(
                self.INPUT_FOLDER,
                "Pasta de rasters ou selecione camdas raster",
                defaultValue="",
            )
        )

        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUT_LAYERS,
                "Camadas de raster QGIS ou selecione pasta de rasters",
                QgsProcessing.TypeRaster,
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterFolderDestination(
                self.OUTPUT_FOLDER,
                "Pasta de saída para rasters gerados",
                defaultValue="",
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.DISPLAY_HELP,
                "Exibir campo de ajuda (Necessario executar e reiniciar)",
                defaultValue=self.prefs.get("display_help", True),
            )
        )

    @staticmethod
    def overlap(r1, r2):
        e1 = r1.extent()
        e2 = r2.extent()

        inter = e1.intersect(e2)

        return not inter.isEmpty()

    def _normalize_placeholders(self, input_folder, output_folder):
        """Retorna paths válidos, trata placeholders TEMPORARY_OUTPUT e INPUT/OUTPUT_FOLDER."""
        sanitized_input = input_folder or ""
        sanitized_output = output_folder or ""

        if sanitized_input.upper() == "TEMPORARY_OUTPUT" or sanitized_input.endswith(
            "INPUT_FOLDER"
        ):
            self.logger.debug(
                "Input_folder placeholder detectado, ignorando input_folder."
            )
            sanitized_input = ""

        if sanitized_output.upper() == "TEMPORARY_OUTPUT" or sanitized_output.endswith(
            "OUTPUT_FOLDER"
        ):
            self.logger.debug(
                "Output_folder placeholder detectado, ignorando output_folder."
            )
            sanitized_output = ""

        return sanitized_input, sanitized_output

    def _ensure_output_folder(self, output_folder, feedback):
        """Garante que a pasta de saída exista; cria temporária se necessária."""
        if not output_folder:
            import tempfile

            output_folder = tempfile.mkdtemp(prefix="cadmus_folderlayer_")
            feedback.pushInfo(
                f"Nenhuma pasta de saída informada. Usando temporária: {output_folder}"
            )
            self.logger.info(f"Output_folder gerada temporária: {output_folder}")

        os.makedirs(output_folder, exist_ok=True)
        return output_folder

    def _collect_rasters_from_folder(self, input_folder, feedback):
        """Recupera rasters válidos da pasta de entrada (recursivo)."""
        rasters = []
        if not input_folder:
            return rasters

        if not os.path.isdir(input_folder):
            self.logger.error(f"Pasta inválida: {input_folder}")
            raise QgsProcessingException(f"Pasta inválida: {input_folder}")

        self.logger.info(f"Lendo arquivos de pasta (recursivamente): {input_folder}")
        raster_paths = []

        for root, _, files in os.walk(input_folder):
            for f in files:
                if f.lower().endswith((".tif", ".tiff", ".vrt", ".img")):
                    raster_paths.append(os.path.join(root, f))

        if not raster_paths:
            feedback.pushInfo("Nenhum raster encontrado na pasta especificada.")
            self.logger.warning(
                "Nenhum arquivo raster válido encontrado na pasta de input."
            )

        for path in sorted(raster_paths):
            layer = QgsRasterLayer(path, os.path.splitext(os.path.basename(path))[0])
            if layer.isValid():
                rasters.append(layer)
                self.logger.debug(f"Raster carregado da pasta: {path}")
            else:
                feedback.pushInfo(f"Raster inválido ignorado: {path}")
                self.logger.warning(f"Raster inválido ignorado: {path}")

        self.logger.info(f"Total de rasters carregados da pasta: {len(rasters)}")
        return rasters

    def _collect_rasters_from_layers(self, input_layers):
        """Adiciona camadas raster válidas diretamente passadas como parâmetro."""
        rasters = []

        if not input_layers:
            return rasters

        for lay in input_layers:
            if isinstance(lay, QgsRasterLayer):
                rasters.append(lay)
            elif isinstance(lay, str):
                layer = QgsRasterLayer(lay, os.path.splitext(os.path.basename(lay))[0])
                if layer.isValid():
                    rasters.append(layer)
            # ignora inválidos sem falhar

        return rasters

    def _build_formula(self, nd1, nd2):
        """Retorna fórmula pronta para QgsRasterCalculator."""
        return (
            f'(("A@1" != {nd1}) AND ("B@1" != {nd2})) * ("A@1" - "B@1") + '
            f'(("A@1" = {nd1}) OR ("B@1" = {nd2})) * {nd1}'
        )

    def _process_pair(self, r1, r2, output_folder, context, feedback, stats_summary):
        """Processa um par de rasters e acumula estatísticas."""
        if not self.overlap(r1, r2):
            feedback.pushInfo(
                f"Sem sobreposição entre {r1.name()} e {r2.name()}. Pulando."
            )
            self.logger.info(f"Sem sobreposição: {r1.name()} x {r2.name()}")
            return

        nd1 = r1.dataProvider().sourceNoDataValue(1)
        nd2 = r2.dataProvider().sourceNoDataValue(1)
        nd1 = nd1 if nd1 is not None else -9999
        nd2 = nd2 if nd2 is not None else -9999

        fname = f"DIF_{r1.name()}_{r2.name()}.tif".replace(" ", "_")
        out_tif = os.path.join(output_folder, fname)

        formula = self._build_formula(nd1, nd2)

        entry1 = QgsRasterCalculatorEntry()
        entry1.ref = "A@1"
        entry1.raster = r1
        entry1.bandNumber = 1

        entry2 = QgsRasterCalculatorEntry()
        entry2.ref = "B@1"
        entry2.raster = r2
        entry2.bandNumber = 1

        try:
            calc = QgsRasterCalculator(
                formula,
                out_tif,
                "GTiff",
                r1.extent(),
                r1.width(),
                r1.height(),
                [entry1, entry2],
            )
            result = calc.processCalculation()
        except Exception as e:
            feedback.pushInfo(f"Erro no cálculo para {r1.name()} x {r2.name()}: {e}")
            self.logger.error(f"Erro em QgsRasterCalculator: {e}")
            return

        if result != 0:
            feedback.pushInfo(f"Erro no cálculo para {r1.name()} x {r2.name()}")
            self.logger.error(
                f"QgsRasterCalculator retornou código {result} para {r1.name()} x {r2.name()}"
            )
            return

        feedback.pushInfo(f"Raster diferença criado: {out_tif}")
        self.logger.info(f"Raster diferença criado: {out_tif}")

        stats_html = os.path.join(
            output_folder, f"{os.path.splitext(fname)[0]}_stats.html"
        )
        try:
            stats = processing.run(
                "native:rasterlayerstatistics",
                {
                    "INPUT": out_tif,
                    "BAND": 1,
                    "OUTPUT_HTML_FILE": stats_html,
                },
                context=context,
                feedback=feedback,
            )
            min_v = stats.get("MIN")
            max_v = stats.get("MAX")
            mean_v = stats.get("MEAN")
            std_v = stats.get("STD_DEV")

            feedback.pushInfo(
                f"Stats gerados para {fname}: MIN={min_v} MAX={max_v} MEAN={mean_v} STD_DEV={std_v}"
            )
            self.logger.info(f"Stats HTML criado: {stats_html}")

            stats_summary.append(
                {
                    "raster_path": out_tif,
                    "min": min_v,
                    "max": max_v,
                    "mean": mean_v,
                    "std_dev": std_v,
                }
            )
        except Exception as e:
            feedback.pushInfo(f"Falha ao gerar stats para {fname}: {e}")
            self.logger.error(f"Erro em native:rasterlayerstatistics para {fname}: {e}")
            stats_summary.append(
                {
                    "raster_path": out_tif,
                    "min": None,
                    "max": None,
                    "mean": None,
                    "std_dev": None,
                }
            )

    def _write_summary_html(self, output_folder, total, stats_summary):
        """Escreve o HTML final com resumo de todas as estatísticas."""
        summary_html = os.path.join(
            output_folder, "raster_difference_stats_summary.html"
        )

        with open(summary_html, "w", encoding="utf-8") as fh:
            fh.write(
                "<html><head><meta charset='utf-8'><title>Resumo de Estatísticas de Diferença</title></head><body>"
            )
            fh.write("<h1>Resumo de Estatísticas de Diferença de Rasters</h1>")
            fh.write("<p>Total de pares processados: %d</p>" % total)
            fh.write("<table border='1' cellpadding='6' cellspacing='0'>")
            fh.write(
                "<tr><th>Raster</th><th>MIN</th><th>MAX</th><th>INTERVALO</th><th>MEAN</th><th>STD_DEV</th></tr>"
            )

            for row in stats_summary:
                min_value = row.get("min")
                max_value = row.get("max")
                interval_value = ""
                try:
                    if min_value is not None and max_value is not None:
                        interval_value = float(max_value) - float(min_value)
                except Exception:
                    interval_value = ""

                fh.write("<tr>")
                fh.write(f"<td>{row.get('raster_path')}</td>")
                fh.write(f"<td>{min_value if min_value is not None else ''}</td>")
                fh.write(f"<td>{max_value if max_value is not None else ''}</td>")
                fh.write(f"<td>{interval_value}</td>")
                fh.write(f"<td>{row.get('mean', '')}</td>")
                fh.write(f"<td>{row.get('std_dev', '')}</td>")
                fh.write("</tr>")

            fh.write("</table>")
            fh.write("</body></html>")

        return summary_html

    def processAlgorithm(self, params, context, feedback):
        input_folder = self.parameterAsString(params, self.INPUT_FOLDER, context)
        input_layers = (
            self.parameterAsLayerList(params, self.INPUT_LAYERS, context) or []
        )
        output_folder = self.parameterAsString(params, self.OUTPUT_FOLDER, context)
        display_help = self.parameterAsBool(params, self.DISPLAY_HELP, context)

        self.logger.info(
            f"ProcessAlgorithm iniciado: input_folder={input_folder}, output_folder={output_folder}, input_layers={len(input_layers)}"
        )
        self.logger.debug(f"Parâmetros detalhados: {params}")

        input_folder, output_folder = self._normalize_placeholders(
            input_folder, output_folder
        )
        output_folder = self._ensure_output_folder(output_folder, feedback)

        if display_help:
            feedback.pushInfo("Processando diferença de rasters por pasta/camadas...")

        folder_rasters = self._collect_rasters_from_folder(input_folder, feedback)
        layer_rasters = self._collect_rasters_from_layers(input_layers)
        rasters = folder_rasters + layer_rasters

        if not input_folder and not rasters:
            raise QgsProcessingException(
                "Informe uma pasta de rasters ou selecione ao menos uma camada raster."
            )

        if len(rasters) < 2:
            self.logger.error(
                "Menos de 2 rasters disponíveis para cálculo de diferença."
            )
            raise QgsProcessingException(
                "É necessário ao menos 2 rasters para calcular diferenças."
            )

        pairs = list(itertools.combinations(rasters, 2))
        total = len(pairs)
        feedback.pushInfo(
            f"Encontradas {total} combinações de rasters para diferenciação."
        )
        self.logger.info(f"Total {total} pares carregados para processamento.")

        stats_summary = []

        for idx, (r1, r2) in enumerate(pairs, start=1):
            feedback.pushInfo(f"Processando {idx}/{total}: {r1.name()} x {r2.name()}")
            self._process_pair(r1, r2, output_folder, context, feedback, stats_summary)

        summary_html = self._write_summary_html(output_folder, total, stats_summary)

        feedback.pushInfo(f"Relatório consolidado gerado: {summary_html}")
        self.logger.info(f"Resumo consolidado de estatísticas criado: {summary_html}")

        display_help = (
            bool(self.parameterAsBool(params, self.DISPLAY_HELP, context))
            if self.DISPLAY_HELP in params
            else False
        )
        self.prefs.update(
            {"output_folder": output_folder, "display_help": display_help}
        )
        self.save_preferences()

        return {self.OUTPUT_FOLDER: output_folder, "SUMMARY_HTML": summary_html}
