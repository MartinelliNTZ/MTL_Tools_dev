# -*- coding: utf-8 -*-
import os
import itertools
import processing
from ..core.config.LogUtils import LogUtils

from qgis.core import (
    QgsRasterLayer,
    QgsApplication,
    QgsTask,
    QgsMessageLog,
    Qgis
)

from qgis.analysis import (
    QgsRasterCalculator,
    QgsRasterCalculatorEntry
)
INPUT_FOLDER = r"D:\TTG\FAZ_MATRIZ_BERRANTE\SEPARADOS"
OUTPUT_FOLDER = f"{INPUT_FOLDER}\DIFERENCAS"

class RasterDiffTask(QgsTask):

    def __init__(self):
        super().__init__("Raster Pairwise Difference", QgsTask.CanCancel)
        self.total_pairs = 0
        self.processed = 0


    def log(self, msg):
        QgsMessageLog.logMessage(msg, "RasterDiff", Qgis.Info)
        print(msg)

    def get_rasters(self):

        rasters = []

        for f in os.listdir(INPUT_FOLDER):

            if f.lower().endswith((".tif",".tiff",".vrt",".img")):
                path = os.path.join(INPUT_FOLDER, f)
                rl = QgsRasterLayer(path, f)

                if rl.isValid():
                    rasters.append(rl)
                else:
                    self.log(f"Raster inválido ignorado: {f}")

        return rasters

    def overlap(self, r1, r2):

        e1 = r1.extent()
        e2 = r2.extent()

        inter = e1.intersect(e2)

        return not inter.isEmpty()

    def get_nodata(self, raster):

        dp = raster.dataProvider()
        nd = dp.sourceNoDataValue(1)

        if nd is None:
            nd = -9999

        return nd

    def run(self):

        if not os.path.exists(OUTPUT_FOLDER):
            os.makedirs(OUTPUT_FOLDER)

        rasters = self.get_rasters()

        if len(rasters) < 2:
            self.log("Menos de dois rasters.")
            return False

        pairs = list(itertools.combinations(rasters, 2))
        self.total_pairs = len(pairs)

        self.log(f"{len(rasters)} rasters encontrados")
        self.log(f"{self.total_pairs} combinações")

        for r1, r2 in pairs:

            if self.isCanceled():
                return False

            name1 = r1.name()
            name2 = r2.name()

            self.log(f"Processando {name1} - {name2}")

            if not self.overlap(r1, r2):
                self.log("Sem sobreposição. Pulando.")
                continue

            nd1 = self.get_nodata(r1)
            nd2 = self.get_nodata(r2)

            entry1 = QgsRasterCalculatorEntry()
            entry1.ref = "A@1"
            entry1.raster = r1
            entry1.bandNumber = 1

            entry2 = QgsRasterCalculatorEntry()
            entry2.ref = "B@1"
            entry2.raster = r2
            entry2.bandNumber = 1

            formula = f"""
            (
            ("A@1" != {nd1}) AND
            ("B@1" != {nd2})
            )
            *
            ("A@1" - "B@1")
            +
            (
            ("A@1" = {nd1}) OR
            ("B@1" = {nd2})
            )
            *
            {nd1}
            """

            out_name = f"DIF_{name1}_{name2}.tif".replace("@","").replace(" ","_")
            out_path = os.path.join(OUTPUT_FOLDER, out_name)

            calc = QgsRasterCalculator(
                formula,
                out_path,
                "GTiff",
                r1.extent(),
                r1.width(),
                r1.height(),
                [entry1, entry2]
            )

            result = calc.processCalculation()

            if result != 0:
                self.log("Erro no cálculo")
                continue

            self.log(f"Raster diferença criado: {out_name}")

            stats = processing.run(
                "native:rasterlayerstatistics",
                {
                    "INPUT": out_path,
                    "BAND": 1,
                    "OUTPUT_HTML_FILE": os.path.join(
                        OUTPUT_FOLDER,
                        out_name.replace(".tif","_stats.html")
                    )
                }
            )

            self.log(
                f"Stats → MIN {stats['MIN']} | MAX {stats['MAX']} | MEAN {stats['MEAN']} | STD {stats['STD_DEV']}"
            )

            self.processed += 1
            progress = (self.processed / self.total_pairs) * 100
            self.setProgress(progress)

        return True

    def finished(self, result):

        if result:
            self.log("Processamento finalizado")
        else:
            self.log("Processamento cancelado")


task = RasterDiffTask()
QgsApplication.taskManager().addTask(task)