# -*- coding: utf-8 -*-
from ..i18n.TranslationManager import STR

class StringManager:
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
            "pt_BR": "BR Português"
        }
