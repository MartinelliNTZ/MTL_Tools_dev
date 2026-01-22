



class StringUtils:
    APP_NAME = "MTL Tools"
    FILTER_VECTOR = "Shapefile (*.shp);;GeoPackage (*.gpkg);;GeoJSON (*.geojson *.json);;KML (*.kml);;CSV (*.csv)"
    FILTER_QGIS_STYLE = 'QML files (*.qml)'
    VECTOR_DRIVERS = {
        ".shp": "ESRI Shapefile",
        ".gpkg": "GPKG",
        ".geojson": "GeoJSON",
        ".json": "GeoJSON",
        ".kml": "KML",       
    }