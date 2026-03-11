# -*- coding: utf-8 -*-

"""
MTL Tools - Public API

Centraliza os imports públicos do plugin.
Evita imports profundos espalhados pelo projeto e melhora autocomplete.
"""

# =========================================================
# UTILS
# =========================================================

from .utils.ToolKeys import ToolKey
from .utils.QgisMessageUtil import QgisMessageUtil
from .utils.DependenciesManager import DependenciesManager
from .utils.ExplorerUtils import ExplorerUtils
from .utils.FormatUtils import FormatUtils
from .utils.LayoutsUtils import LayoutsUtils
from .utils.PDFUtils import PDFUtils
from .utils.Preferences import load_tool_prefs, save_tool_prefs
from .utils.ProjectUtils import ProjectUtils
from .utils.StringUtils import StringUtils


# =========================================================
# UTILS - MRK
# =========================================================

from .utils.mrk.MrkParser import MrkParser
from .utils.mrk.PhotoMetadata import PhotoMetadata


# =========================================================
# UTILS - RASTER
# =========================================================

from .utils.raster.RasterLayerMetrics import RasterLayerMetrics
from .utils.raster.RasterLayerProcessing import RasterLayerProcessing
from .utils.raster.RasterLayerProjection import RasterLayerProjection
from .utils.raster.RasterLayerRendering import RasterLayerRendering
from .utils.raster.RasterLayerSource import RasterLayerSource
from .utils.raster.RasterVectorBridge import RasterVectorBridge


# =========================================================
# UTILS - VECTOR
# =========================================================

from .utils.vector.VectorLayerAttributes import VectorLayerAttributes
from .utils.vector.VectorLayerGeometry import VectorLayerGeometry
from .utils.vector.VectorLayerMetrics import VectorLayerMetrics
from .utils.vector.VectorLayerProjection import VectorLayerProjection
from .utils.vector.VectorLayerSource import VectorLayerSource


# =========================================================
# CORE CONFIG
# =========================================================

from .core.config.LogCleanupUtils import LogCleanupUtils
from .core.config.LogUtils import LogUtils


# =========================================================
# CORE ENGINE TASKS
# =========================================================

from .core.engine_tasks.AsyncPipelineEngine import AsyncPipelineEngine
from .core.engine_tasks.BaseStep import BaseStep
from .core.engine_tasks.BufferStep import BufferStep
from .core.engine_tasks.ExecutionContext import ExecutionContext
from .core.engine_tasks.ExplodeStep import ExplodeStep
from .core.engine_tasks.LineFieldsStep import LineFieldsStep
from .core.engine_tasks.LoadFilesStep import LoadFilesStep
from .core.engine_tasks.MrkParseStep import MrkParseStep
from .core.engine_tasks.PhotoMetadataStep import PhotoMetadataStep
from .core.engine_tasks.PointFieldsStep import PointFieldsStep
from .core.engine_tasks.PolygonFieldsStep import PolygonFieldsStep
from .core.engine_tasks.SaveVectorStep import SaveVectorStep


# =========================================================
# PROCESSING PROVIDER
# =========================================================

from .processing.provider import MTLProvider


# =========================================================
# PROCESSING ALGORITHMS
# =========================================================

from .processing.attribute_statistics import AttributeStatisticsAlgorithm
from .processing.difference_fields_algorithm import DifferenceFieldsAlgorithm
from .processing.elevation_analisys import ElevationAnalisys
from .processing.implement_trail import ImplementTrail
from .processing.my_algorithm import MTLExampleAlgorithm
from .processing.raster_mass_sampler import RasterMassSampler


# =========================================================
# PUBLIC EXPORTS
# =========================================================

__all__ = [

    # utils
    "ToolKey",
    "QgisMessageUtil",
    "DependenciesManager",
    "ExplorerUtils",
    "FormatUtils",
    "LayoutsUtils",
    "PDFUtils",
    "Preferences",
    "ProjectUtils",
    "StringUtils",

    # utils.mrk
    "MrkParser",
    "PhotoMetadata",

    # utils.raster
    "RasterLayerMetrics",
    "RasterLayerProcessing",
    "RasterLayerProjection",
    "RasterLayerRendering",
    "RasterLayerSource",
    "RasterVectorBridge",

    # utils.vector
    "VectorLayerAttributes",
    "VectorLayerGeometry",
    "VectorLayerMetrics",
    "VectorLayerProjection",
    "VectorLayerSource",

    # core.config
    "LogCleanupUtils",
    "LogUtils",

    # core.engine_tasks
    "AsyncPipelineEngine",
    "BaseStep",
    "BufferStep",
    "ExecutionContext",
    "ExplodeStep",
    "LineFieldsStep",
    "LoadFilesStep",
    "MrkParseStep",
    "PhotoMetadataStep",
    "PointFieldsStep",
    "PolygonFieldsStep",
    "SaveVectorStep",

    # processing
    "MTLProvider",
    "AttributeStatisticsAlgorithm",
    "DifferenceFieldsAlgorithm",
    "ElevationAnalisys",
    "ImplementTrail",
    "MyAlgorithm",
    "RasterMassSampler",
]