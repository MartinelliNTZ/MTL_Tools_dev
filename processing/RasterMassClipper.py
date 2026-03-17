# -*- coding: utf-8 -*-
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

from PyQt5.QtGui import QIcon

from .BaseProcessingAlgorithm import BaseProcessingAlgorithm
from qgis.core import (
    QgsProcessingAlgorithm,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterFolderDestination,
    QgsProcessingParameterBoolean,
    QgsProcessing,
    QgsVectorLayer,
    QgsCoordinateTransform,
    QgsProject,
)

import processing
from ..utils.Preferences import load_tool_prefs, save_tool_prefs
from ..utils.ToolKeys import ToolKey
from ..core.config.LogUtils import LogUtils


class RasterMassClipper(BaseProcessingAlgorithm):

    TOOL_KEY = ToolKey.RASTER_MASS_CLIPPER
    INPUT_MASK = "INPUT_MASK"
    INPUT_RASTERS = "INPUT_RASTERS"
    OUTPUT_FOLDER = "OUTPUT_FOLDER"
    PER_FEATURE = "PER_FEATURE"
    BUFFER_FIX = "BUFFER_FIX"
    logger = LogUtils(tool=TOOL_KEY, class_name="RasterMassClipper", level="DEBUG")
    prefs = load_tool_prefs(TOOL_KEY)

    def name(self):
        return "raster_mass_clipper"

    def displayName(self):
        return "Recorte Massivo de Rasters"

    def createInstance(self):
        return RasterMassClipper()

    # ---------------- INIT ----------------

    def initAlgorithm(self, config=None):
        self.logger.debug("Inicializando algoritmo RasterMassClipper…")

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT_MASK,
                "Camada máscara (polígono)",
                [QgsProcessing.TypeVectorPolygon],
            )
        )

        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUT_RASTERS,
                "Rasters",
                QgsProcessing.TypeRaster,
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.PER_FEATURE,
                "Recortar por cada polígono",
                defaultValue=self.prefs.get("per_feature", False)
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.BUFFER_FIX,
                "Aplicar buffer de correção (pixel * 1.1)",
                defaultValue=self.prefs.get("buffer_fix", True)
            )
        )

        self.addParameter(
            QgsProcessingParameterFolderDestination(
                self.OUTPUT_FOLDER,
                "Pasta de saída",
                defaultValue=self.prefs.get("last_output_folder", ""),
            )
        )

    # ---------------- PROCESS ----------------

    def processAlgorithm(self, params, context, feedback):        

        mask_layer = self.parameterAsVectorLayer(params, self.INPUT_MASK, context)
        rasters = self.parameterAsLayerList(params, self.INPUT_RASTERS, context)
        out_folder = self.parameterAsString(params, self.OUTPUT_FOLDER, context)

        per_feature = self.parameterAsBool(params, self.PER_FEATURE, context)
        buffer_fix = self.parameterAsBool(params, self.BUFFER_FIX, context)
        self.logger.debug(f"Parâmetros: {per_feature}, Buffer fix: {buffer_fix}, Output folder: {out_folder}, Rasters: {[r.name() for r in rasters]}")

        os.makedirs(out_folder, exist_ok=True)

        tasks = []

        with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:

            if per_feature:

                for feat in mask_layer.getFeatures():

                    for ras in rasters:

                        tasks.append(
                            executor.submit(
                                self.clip_raster_feature,
                                ras,
                                feat.geometry(),
                                feat.id(),
                                mask_layer,
                                out_folder,
                                buffer_fix,
                                context,
                            )
                        )

            else:

                for ras in rasters:

                    tasks.append(
                        executor.submit(
                            self.clip_raster_layer,
                            ras,
                            mask_layer,
                            out_folder,
                            buffer_fix,
                            context,
                        )
                    )

            for future in as_completed(tasks):

                if feedback.isCanceled():
                    break

                try:
                    future.result()
                except Exception as e:
                    feedback.pushInfo(str(e))
                    self.logger.error(f"Erro ao processar tarefa: {e}")

        prefs = load_tool_prefs(self.TOOL_KEY)
        prefs["last_output_folder"] = out_folder
        prefs['per_feature'] = per_feature
        prefs['buffer_fix'] = buffer_fix
        save_tool_prefs(self.TOOL_KEY, prefs)

        clickable = f'<a href="file:///{out_folder}">{out_folder}</a>'
        feedback.pushInfo(f"Arquivos salvos em: {clickable}")    

        return {self.OUTPUT_FOLDER: out_folder}
    


    # ---------------- CLIP LAYER ----------------

    def clip_raster_layer(self, raster, mask_layer, out_folder, buffer_fix, context):

        raster_path = raster.source()
        base = os.path.splitext(os.path.basename(raster_path))[0]

        mask = self.prepare_mask(mask_layer, raster)

        if buffer_fix:

            pixel = abs(raster.rasterUnitsPerPixelX())
            buffer_dist = pixel * 1.1

            self.logger.debug(
                f"Aplicando buffer {buffer_dist} na layer inteira"
            )

            buffered = QgsVectorLayer(
                f"Polygon?crs={raster.crs().authid()}",
                "mask_buffer",
                "memory",
            )

            prov = buffered.dataProvider()

            feats = []

            for f in mask.getFeatures():

                g = f.geometry().buffer(buffer_dist, 5)

                nf = f
                nf.setGeometry(g)

                feats.append(nf)

            prov.addFeatures(feats)
            buffered.updateExtents()

            mask = buffered

        out_path = os.path.join(out_folder, f"{base}_clip.tif")

        processing.run(
            "gdal:cliprasterbymasklayer",
            {
                "INPUT": raster_path,
                "MASK": mask,
                "CROP_TO_CUTLINE": True,
                "KEEP_RESOLUTION": True,
                "OUTPUT": out_path,
            },
            context=context,
        )
    # ---------------- CLIP FEATURE ----------------

    def clip_raster_feature(
        self, raster, geom, feat_id, mask_layer, out_folder, buffer_fix, context
    ):

        raster_path = raster.source()
        base = os.path.splitext(os.path.basename(raster_path))[0]

        geom = self.reproject_geom(geom, mask_layer.crs(), raster.crs())

        if buffer_fix:

            pixel = abs(raster.rasterUnitsPerPixelX())
            buffer_dist = pixel * 1.1

            geom = geom.buffer(buffer_dist, 5)

            self.logger.debug(
                f"Buffer feature {feat_id}: {buffer_dist}"
            )

        mem_layer = QgsVectorLayer(
            f"Polygon?crs={raster.crs().authid()}",
            "mask",
            "memory",
        )

        prov = mem_layer.dataProvider()

        feat = self.geom_to_feature(geom)
        prov.addFeature(feat)

        mem_layer.updateExtents()

        out_path = os.path.join(out_folder, f"{base}_feat_{feat_id}.tif")

        processing.run(
            "gdal:cliprasterbymasklayer",
            {
                "INPUT": raster_path,
                "MASK": mem_layer,
                "CROP_TO_CUTLINE": True,
                "KEEP_RESOLUTION": True,
                "OUTPUT": out_path,
            },
            context=context,
        )

    # ---------------- HELPERS ----------------

    def reproject_geom(self, geom, src_crs, dst_crs):

        if src_crs == dst_crs:
            return geom

        transform = QgsCoordinateTransform(
            src_crs,
            dst_crs,
            QgsProject.instance(),
        )

        g = geom.clone()
        g.transform(transform)

        return g

    def geom_to_feature(self, geom):

        from qgis.core import QgsFeature

        f = QgsFeature()
        f.setGeometry(geom)
        return f

    def prepare_mask(self, layer, raster):

        crs = raster.crs()

        if layer.crs() == crs:
            return layer

        self.logger.debug(
            f"Reprojetando máscara {layer.crs().authid()} -> {crs.authid()}"
        )

        params = {
            "INPUT": layer,
            "TARGET_CRS": crs,
            "OUTPUT": "memory:",
        }

        result = processing.run(
            "native:reprojectlayer",
            params
        )

        return result["OUTPUT"]

    # ---------------- UI ----------------

    def icon(self):
        return super().icon("raster_mass_clipper.ico")

    def group(self):
        return self.GROUP_RASTER.name

    def groupId(self):
        return self.GROUP_RASTER.id