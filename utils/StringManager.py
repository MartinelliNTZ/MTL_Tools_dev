# -*- coding: utf-8 -*-
from ..i18n.TranslationManager import STR


class StringManager:
    MENU_CATEGORIES = {
        "SYSTEM": STR.MENU_SYSTEM,
        "LAYOUTS": STR.MENU_LAYOUTS,
        "FOLDER": STR.MENU_FOLDER,
        "VECTOR": STR.MENU_VECTOR,
        "AGRICULTURE": STR.MENU_AGRICULTURE,
        "RASTER": STR.MENU_RASTER,
    }
    KML_FIELDS = [
        "descriptio",
        "timestamp",
        "begin",
        "end",
        "altitudeMo",
        "tessellate",
        "extrude",
        "visibility",
        "drawOrder",
        "icon",
    ]

    # Filtros de arquivos
    FILTER_ALL = "All files (*.*)"
    FILTER_VECTOR = "Shapefile (*.shp);;GeoPackage (*.gpkg);;GeoJSON (*.geojson *.json);;KML (*.kml);;CSV (*.csv)"
    FILTER_QGIS_STYLE = "QML files (*.qml)"
    SHP_EXTENSIONS = [".shp", ".shx", ".dbf", ".prj", ".cpg", ".qix"]
    VECTOR_DRIVERS = {
        ".shp": "ESRI Shapefile",
        ".gpkg": "GPKG",
        ".geojson": "GeoJSON",
        ".json": "GeoJSON",
        ".kml": "KML",
    }
    AVAILABLE_LANGUAGES = {
        "none": "🔧 " + STR.AUTO_DETECT,
        "es": "ES Español",
        "en": "EN English",
        "pt_BR": "BR Português",
        "de": "DE Deutsch",
    }
    VECTOR_EXTS = {
        ".shp",
        ".geojson",
        ".json",
        ".kml",
        ".kmz",
        ".gpx",
        ".csv",
        ".tab",
        ".las",
        ".laz",
        ".gpkg",
    }
    RASTER_EXTS = {".tif", ".tiff", ".ecw", ".jp2", ".asc"}
