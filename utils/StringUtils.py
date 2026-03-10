



class StringUtils:
    APP_NAME = "MTL Tools"
    #Filtros de arquivos
    FILTER_ALL = "All files (*.*)"
    FILTER_VECTOR = "Shapefile (*.shp);;GeoPackage (*.gpkg);;GeoJSON (*.geojson *.json);;KML (*.kml);;CSV (*.csv)"
    FILTER_QGIS_STYLE = 'QML files (*.qml)'
    SHP_EXTENSIONS = [".shp", ".shx", ".dbf", ".prj", ".cpg", ".qix"]
    VECTOR_DRIVERS = {
        ".shp": "ESRI Shapefile",
        ".gpkg": "GPKG",
        ".geojson": "GeoJSON",
        ".json": "GeoJSON",
        ".kml": "KML",       
    }