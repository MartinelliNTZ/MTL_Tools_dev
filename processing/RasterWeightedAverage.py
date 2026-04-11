# -*- coding: utf-8 -*-
import os

from qgis.analysis import QgsRasterCalculator, QgsRasterCalculatorEntry
from qgis.core import (
    QgsCoordinateTransform,
    QgsProcessing,
    QgsProcessingException,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
    QgsRasterLayer,
)
from qgis.core import (
    QgsProcessingAlgorithm,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterNumber,
    QgsProcessingParameterDefinition,
    QgsProcessingParameterFeatureSink
)
import processing

from ..core.config.LogUtils import LogUtils
from ..i18n.TranslationManager import STR
from ..utils.ToolKeys import ToolKey
from .BaseProcessingAlgorithm import BaseProcessingAlgorithm


class RasterWeightedAverage(BaseProcessingAlgorithm):
    """
    QgsProcessingAlgorithm: Calcula média ponderada entre 2 a 4 camadas raster.
    """

    TOOL_KEY = ToolKey.RASTER_WEIGHTED_AVERAGE
    ALGORITHM_NAME = "raster_weighted_average"
    ALGORITHM_DISPLAY_NAME = STR.RASTER_WEIGHTED_AVERAGE_TITLE
    ALGORITHM_GROUP = BaseProcessingAlgorithm.GROUP_RASTER
    ICON = "raster_mass_sampler.ico"
    INSTRUCTIONS_FILE = "raster_mass_sampler.html"
    logger = LogUtils(tool=TOOL_KEY, class_name="RasterWeightedAverage", level="DEBUG")

    INPUT_RASTER_1 = "INPUT_RASTER_1"
    INPUT_RASTER_2 = "INPUT_RASTER_2"
    INPUT_RASTER_3 = "INPUT_RASTER_3"
    INPUT_RASTER_4 = "INPUT_RASTER_4"
    WEIGHT_1 = "WEIGHT_1"
    WEIGHT_2 = "WEIGHT_2"
    WEIGHT_3 = "WEIGHT_3"
    WEIGHT_4 = "WEIGHT_4"
    OUTPUT_RESOLUTION = "OUTPUT_RESOLUTION"
    OUTPUT = "OUTPUT"
    DISPLAY_HELP = "DISPLAY_HELP"
    OPEN_OUTPUT_FOLDER = "OPEN_OUTPUT_FOLDER"

    def initAlgorithm(self, config=None):
            self.logger.debug("Inicializando algoritmo RasterWeightedAverage…")
            self.load_preferences()

            self.addParameter(
                QgsProcessingParameterRasterLayer(
                    self.INPUT_RASTER_1,
                    "Raster 1",
                )
            )

            self.addParameter(
                QgsProcessingParameterRasterLayer(
                    self.INPUT_RASTER_2,
                    "Raster 2",
                )
            )

            param = QgsProcessingParameterRasterLayer(
                self.INPUT_RASTER_3,
                "Raster 3 (opcional)",
                optional=True,
            )
            param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
            self.addParameter(param)

            param = QgsProcessingParameterRasterLayer(
                self.INPUT_RASTER_4,
                "Raster 4 (opcional)",
                optional=True,
            )
            param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
            self.addParameter(param)

            self.addParameter(
                QgsProcessingParameterNumber(
                    self.WEIGHT_1,
                    "Peso Raster 1",
                    type=QgsProcessingParameterNumber.Double,
                    defaultValue=self.prefs.get("weight_1", 50.0),
                    minValue=0.0,
                )
            )

            self.addParameter(
                QgsProcessingParameterNumber(
                    self.WEIGHT_2,
                    "Peso Raster 2",
                    type=QgsProcessingParameterNumber.Double,
                    defaultValue=self.prefs.get("weight_2", 50.0),
                    minValue=0.0,
                )
            )

            param = QgsProcessingParameterNumber(
                self.WEIGHT_3,
                "Peso Raster 3",
                type=QgsProcessingParameterNumber.Double,
                defaultValue=self.prefs.get("weight_3", 50.0),
                minValue=0.0,
                optional=True,
            )
            param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
            self.addParameter(param)

            param = QgsProcessingParameterNumber(
                self.WEIGHT_4,
                "Peso Raster 4",
                type=QgsProcessingParameterNumber.Double,
                defaultValue=self.prefs.get("weight_4", 50.0),
                minValue=0.0,
                optional=True,
            )
            param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
            self.addParameter(param)

            param = QgsProcessingParameterNumber(
                self.OUTPUT_RESOLUTION,
                "Resolução de Saída (pixels)",
                type=QgsProcessingParameterNumber.Double,
                defaultValue=self.prefs.get("output_resolution", 0),
                minValue=0.0,
                optional=True,
            )
            param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
            self.addParameter(param)

            self.addParameter(
                QgsProcessingParameterRasterDestination(self.OUTPUT, "Saída")
            )

            self.addParameter(
                QgsProcessingParameterBoolean(
                    self.OPEN_OUTPUT_FOLDER,
                    STR.OPEN_OUTPUT_FOLDER,
                    defaultValue=self.prefs.get("open_output_folder", True),
                )
            )

            self.addParameter(
                QgsProcessingParameterBoolean(
                    self.DISPLAY_HELP,
                    STR.DISPLAY_HELP_FIELD,
                    defaultValue=self.prefs.get("display_help", True),
                )
            )

    def processAlgorithm(self, params, context, feedback):
        self.logger.debug("Iniciando processAlgorithm…")

        try:
            # Recuperar rasters obrigatórios
            raster1 = self.parameterAsRasterLayer(params, self.INPUT_RASTER_1, context)
            raster2 = self.parameterAsRasterLayer(params, self.INPUT_RASTER_2, context)

            if not raster1 or not raster1.isValid():
                msg = "Raster 1 é obrigatório e inválido."
                self.logger.error(msg)
                raise QgsProcessingException(msg)

            if not raster2 or not raster2.isValid():
                msg = "Raster 2 é obrigatório e inválido."
                self.logger.error(msg)
                raise QgsProcessingException(msg)

            self.logger.debug(f"Raster 1: {raster1.name()}")
            self.logger.debug(f"  CRS: {raster1.crs().authid()}")
            self.logger.debug(f"  Resolução: {raster1.rasterUnitsPerPixelX()} x {raster1.rasterUnitsPerPixelY()}")
            self.logger.debug(f"  Extent: {raster1.extent()}")

            self.logger.debug(f"Raster 2: {raster2.name()}")
            self.logger.debug(f"  CRS: {raster2.crs().authid()}")
            self.logger.debug(f"  Resolução: {raster2.rasterUnitsPerPixelX()} x {raster2.rasterUnitsPerPixelY()}")
            self.logger.debug(f"  Extent: {raster2.extent()}")

            # Recuperar rasters opcionais
            raster3 = self.parameterAsRasterLayer(params, self.INPUT_RASTER_3, context)
            raster4 = self.parameterAsRasterLayer(params, self.INPUT_RASTER_4, context)

            if raster3 and raster3.isValid():
                self.logger.debug(f"Raster 3: {raster3.name()}")
                self.logger.debug(f"  CRS: {raster3.crs().authid()}")
            else:
                raster3 = None

            if raster4 and raster4.isValid():
                self.logger.debug(f"Raster 4: {raster4.name()}")
                self.logger.debug(f"  CRS: {raster4.crs().authid()}")
            else:
                raster4 = None

            # Recuperar pesos
            weight1 = self.parameterAsDouble(params, self.WEIGHT_1, context)
            weight2 = self.parameterAsDouble(params, self.WEIGHT_2, context)
            weight3 = self.parameterAsDouble(params, self.WEIGHT_3, context)
            weight4 = self.parameterAsDouble(params, self.WEIGHT_4, context)

            self.logger.debug(
                f"Pesos brutos: W1={weight1}, W2={weight2}, W3={weight3}, W4={weight4}"
            )

            # Recuperar resolução de saída
            output_resolution = self.parameterAsDouble(params, self.OUTPUT_RESOLUTION, context)
            if output_resolution is None or output_resolution <= 0:
                output_resolution = None
                self.logger.debug("Resolução de saída: nenhuma (usar resolução original)")
            else:
                self.logger.debug(f"Resolução de saída: {output_resolution}")

            # Recuperar parâmetros booleanos
            open_output_folder = self.parameterAsBool(params, self.OPEN_OUTPUT_FOLDER, context)
            display_help = self.parameterAsBool(params, self.DISPLAY_HELP, context)

            # Caminho de saída
            output_path = self.parameterAsOutputLayer(params, self.OUTPUT, context)
            self.logger.debug(f"Output path: {output_path}")

            # Construir lista de rasters com pesos
            rasters_with_weights = []
            if raster1:
                rasters_with_weights.append((raster1, weight1))
            if raster2:
                rasters_with_weights.append((raster2, weight2))
            if raster3:
                rasters_with_weights.append((raster3, weight3))
            if raster4:
                rasters_with_weights.append((raster4, weight4))

            num_rasters = len(rasters_with_weights)
            self.logger.debug(f"Total de rasters válidos a processar: {num_rasters}")

            if num_rasters < 2:
                msg = f"Pelo menos 2 rasters são necessários. Fornecidos: {num_rasters}"
                self.logger.error(msg)
                raise QgsProcessingException(msg)

            # Validar compatibilidade (CRS e resolução)
            self._validate_raster_compatibility(rasters_with_weights)

            # Reamostrar se resolução de saída foi definida
            if output_resolution is not None:
                self.logger.debug(f"Reamostrando rasters para resolução {output_resolution}…")
                rasters_with_weights = self._resample_rasters(
                    rasters_with_weights, output_resolution, context, feedback
                )
                self.logger.debug("Reamostragem concluída.")

            # Descarregar rasters não usados
            for ras in [raster3, raster4]:
                if ras is None or ras not in [r[0] for r in rasters_with_weights]:
                    pass

            # Construir fórmula para QgsRasterCalculator
            entries = []
            formula_parts = []
            total_weight = 0.0

            # Refs: "A@1", "B@1", "C@1", "D@1"
            refs = ["A", "B", "C", "D"]

            for i, (ras, weight) in enumerate(rasters_with_weights):
                entry = QgsRasterCalculatorEntry()
                entry.raster = ras
                entry.bandNumber = 1
                entry.ref = f"{refs[i]}@1"
                entries.append(entry)
                formula_parts.append(f"({entry.ref} * {weight})")
                total_weight += weight

            formula = f"({' + '.join(formula_parts)}) / {total_weight}"
            self.logger.debug(f"Fórmula gerada: {formula}")

            feedback.pushInfo(f"Processando {num_rasters} rasters com pesos: {total_weight}")
            feedback.pushInfo(f"Fórmula: {formula}")

            # Usar mesmo CRS e extent do primeiro raster
            base_raster = rasters_with_weights[0][0]

            # Calcular usando QgsRasterCalculator
            self.logger.debug("Iniciando QgsRasterCalculator…")
            calc = QgsRasterCalculator(
                formula,
                output_path,
                "GTiff",
                base_raster.extent(),
                base_raster.width(),
                base_raster.height(),
                entries,
            )

            self.logger.debug("Executando processCalculation()…")
            result = calc.processCalculation()

            if result != 0:
                msg = f"Erro no cálculo raster. Código de erro: {result}"
                self.logger.error(msg)
                self.logger.error(f"  Fórmula: {formula}")
                self.logger.error(f"  Base raster: {base_raster.name()}")
                self.logger.error(f"  Output: {output_path}")
                raise QgsProcessingException(msg)

            self.logger.debug("Cálculo concluído com sucesso.")

            # Salvar preferências
            self.prefs.update(
                {
                    "weight_1": float(weight1),
                    "weight_2": float(weight2),
                    "weight_3": float(weight3),
                    "weight_4": float(weight4),
                    "output_resolution": float(output_resolution) if output_resolution else None,
                    "display_help": bool(display_help),
                    "open_output_folder": bool(open_output_folder),
                }
            )
            self.save_preferences()
            self.logger.debug("Preferências salvas.")

            # Abrir pasta de saída se necessário
            if output_path and isinstance(output_path, str) and not output_path.startswith("memory:"):
                out_folder = os.path.dirname(output_path)
                if out_folder:
                    feedback.pushInfo(f"Arquivo salvo em: {out_folder}")
                    self.logger.debug(f"Output folder: {out_folder}")

                    if open_output_folder:
                        self.logger.debug("Abrindo pasta de saída…")
                        self.open_folder_in_explorer(out_folder)

            feedback.pushInfo("Média ponderada calculada com sucesso!")
            self.logger.debug("processAlgorithm finalizado com sucesso.")
            return {self.OUTPUT: output_path}

        except QgsProcessingException as e:
            self.logger.error(f"QgsProcessingException: {e}")
            raise
        except Exception as e:
            msg = f"Erro não tratado em processAlgorithm: {e}"
            self.logger.error(msg)
            self.logger.error(f"  Tipo: {type(e).__name__}")
            raise QgsProcessingException(msg)

    def _resample_rasters(self, rasters_with_weights, target_resolution, context, feedback):
        """
        Reamostra os rasters para a resolução de saída usando QGIS Processing.
        Retorna nova lista de tuplas (raster_reamostrado, peso).
        """
        import tempfile

        resampled_rasters = []
        base_raster = rasters_with_weights[0][0]
        extent = base_raster.extent()

        # Calcular dimensões baseado na resolução desejada
        width = max(1, int(extent.width() / target_resolution))
        height = max(1, int(extent.height() / target_resolution))

        self.logger.debug(f"Dimensões de saída: {width} x {height}")

        for idx, (ras, weight) in enumerate(rasters_with_weights):
            self.logger.debug(f"Reamostrando raster {idx+1}: {ras.name()}…")
            feedback.pushInfo(f"Reamostrando raster {idx+1}…")

            try:
                # Criar arquivo temporário
                temp_file = os.path.join(
                    tempfile.gettempdir(),
                    f"cadmus_resample_{idx}_{os.path.basename(ras.source())}"
                )

                # Usar qgis:rasterlayerresampler (nativo do QGIS)
                alg_params = {
                    'INPUT': ras,
                    'OUTPUT_WIDTH': width,
                    'OUTPUT_HEIGHT': height,
                    'OUTPUT': temp_file,
                }

                self.logger.debug(f"Executando qgis:rasterlayerresampler para {ras.name()}")
                result = processing.run(
                    'qgis:rasterlayerresampler',
                    alg_params,
                    context=context,
                    feedback=feedback,
                    is_child_algorithm=True
                )

                output_file = result.get('OUTPUT')
                if not output_file:
                    # Fallback: usar arquivo temporário
                    output_file = temp_file
                    self.logger.debug(f"Usando fallback temp file: {output_file}")

                # Carregar raster reamostrado
                resampled = QgsRasterLayer(output_file, f"Resampled_{idx}")
                if not resampled.isValid():
                    msg = f"Falha ao carregar raster reamostrado: {output_file}"
                    self.logger.error(msg)
                    raise QgsProcessingException(msg)

                self.logger.debug(f"Raster {idx+1} reamostrado com sucesso.")
                resampled_rasters.append((resampled, weight))

            except Exception as e:
                msg = f"Erro ao reamostrar raster {idx+1}: {e}"
                self.logger.error(msg)
                self.logger.error(f"  Exception type: {type(e).__name__}")
                raise QgsProcessingException(msg)

        self.logger.debug(f"Total de rasters reamostrados: {len(resampled_rasters)}")
        return resampled_rasters

    def _validate_raster_compatibility(self, rasters_with_weights):
        """Valida se os rasters são compatíveis (CRS e resolução)."""
        if not rasters_with_weights:
            return

        base_raster, _ = rasters_with_weights[0]
        base_crs = base_raster.crs()
        base_extent = base_raster.extent()

        self.logger.debug("Validando compatibilidade de rasters…")

        for i, (ras, _) in enumerate(rasters_with_weights[1:], 1):
            # Verificar CRS
            if ras.crs() != base_crs:
                self.logger.warning(
                    f"Raster {i+1} tem CRS diferente: {ras.crs().authid()} vs {base_crs.authid()}"
                )

            # Verificar intersecção
            if not ras.extent().intersects(base_extent):
                self.logger.warning(
                    f"Raster {i+1} não intersecta com Raster 1"
                )