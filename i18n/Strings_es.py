# -*- coding: utf-8 -*-
from .Strings_pt_BR import Strings_pt_BR


class Strings_es(Strings_pt_BR):
    """ "Strings for Spanish (es)"""

    # General
    APP_NAME = "Cadmus"

    # About
    ABOUT_CADMUS = "Acerca de Cadmus"
    VERSION = "Versión"
    UPDATED_ON = "Actualizado el"
    CREATED_ON = "Creado el"
    CREATOR = "Creador"
    LOCATION = "Ubicación"

    # Buttons
    CLOSE = "Cerrar"
    SAVE = "Guardar"
    EXPORT = "Exportar"
    CANCEL = "Cancelar"
    EXECUTE = "Ejecutar"
    COPIED = "Copiado"

    # Common labels
    OPTIONS = "Opciones"
    SAVING = "Guardado"
    STYLES = "Estilos"
    WARNING = "Aviso"
    ERROR = "Error"
    ADVANCED_PARAMETERS = "Parámetros Avanzados"
    APP_PREFERENCES = "Preferencias de la Aplicación"
    OPEN_PREFERENCES_FOLDER = "Abrir Carpeta de Preferencias"
    FILE_TYPES = "Tipos de Archivo"
    ROOT_FOLDER = "Carpeta raíz:"
    OUTPUT_FOLDER = "Carpeta de salida:"
    INPUT_LINE_LAYER = "Capa de Líneas (ENTRADA):"
    SOURCE_LAYER = "Capa de Origen:"
    TARGET_LAYER = "Capa de Destino:"
    IMPLEMENT_SIZE = "Tamaño del implemento: (siempre en metros)"
    VECTOR_CALCULATION_METHOD = "Método de Cálculo Vectorial"
    VECTOR_FIELDS_PRECISION = "Precisión de campos vectoriales (decimales):"
    ASYNC_THRESHOLD = "Umbral asíncrono (nº de entidades):"
    CALCULATION_METHOD_LABEL = "Método de cálculo vectorial:"
    SEARCH_TEXT = "Texto a buscar:"
    REPLACE_WITH_NEW_TEXT = "Texto de reemplazo (nuevo):"
    SOURCE_LAYER_ATTRIBUTES = "Atributos de la capa de origen"
    EXPORT_OPTIONS = "Opciones de Exportación"
    MAX_WIDTH_PNG = "Ancho máximo para PNG (px):"
    USE_PROJECT_FOLDER = "Usar carpeta del proyecto"
    EXPORT_PDF = "Exportar PDF"
    EXPORT_PNG = "Exportar PNG"
    MERGE_PDFS_FINAL = "Unir PDFs en PDF final"
    MERGE_PNGS_FINAL = "Unir PNGs en PDF final"
    REPLACE_EXISTING_FILES = "Reemplazar archivos existentes"
    WGS84_EPSG4326 = "WGS 84 (EPSG:4326)"
    UTM_SIRGAS_2000 = "UTM SIRGAS 2000"
    ALTIMETRY_OPENTOPO = "Altimetría (OpenTopoData)"
    APPROX_ALTITUDE_METERS = "Altitud aproximada (m)"
    LATITUDE_DECIMAL = "Latitud (Decimal)"
    LONGITUDE_DECIMAL = "Longitud (Decimal)"
    LATITUDE_DMS = "Latitud (DMS)"
    LONGITUDE_DMS = "Longitud (DMS)"
    EASTING_X = "Este (X)"
    NORTHING_Y = "Norte (Y)"
    ADDRESS_OSM = "Dirección (OSM):"
    COPY_WGS84_FULL = "Copiar WGS 84 (Completo)"
    COPY_UTM_FULL = "Copiar UTM (Completo)"
    COPY_LOCATION_FULL = "Copiar Ubicación (Completa)"
    POINT_COORDINATES = "Coordenadas del Punto"
    ZONE = "Zona"
    HEMISPHERE = "Hemisferio"
    CITY = "Municipio"
    INTERMEDIATE_REGION = "Región Intermedia"
    STATE = "Estado"
    REGION = "Región"
    COUNTRY = "País"
    LOADING = "Cargando..."
    LOADING_LOWER = "cargando..."
    UNAVAILABLE = "No disponible"

    # Common option labels
    CASE_SENSITIVE = "Distinguir mayúsculas/minúsculas"
    FULL_LABEL_REPLACE = "Reemplazar la etiqueta completa cuando se encuentre el texto"
    LOAD_ONLY_MISSING_FILES = "Cargar solo archivos que aún no están en el proyecto"
    PRESERVE_FOLDER_STRUCTURE = (
        "Crear grupos según la estructura de carpetas/subcarpetas"
    )
    DO_NOT_GROUP_LAST_FOLDER = "No agrupar la última carpeta"
    CREATE_PROJECT_BACKUP_IF_SAVED = (
        "Crear copia de seguridad del proyecto antes de cargar (solo si ya está guardado)"
    )

    # Common messages
    SUCCESS_MESSAGE = "Procesamiento completado con éxito."
    ERROR_LAYER_NOT_FOUND = "Error: Capa no encontrada."
    SELECT_VALID_FOLDER = "Seleccione una carpeta válida."
    SELECT_AT_LEAST_ONE_FILE_TYPE = "Seleccione al menos un tipo de archivo."
    SELECT_AT_LEAST_ONE_EXPORT_FORMAT = (
        "Seleccione al menos un formato (PDF o PNG)"
    )
    SELECT_VALID_LINE_LAYER = "Seleccione una capa de líneas válida."
    INVALID_SOURCE_LAYER = "Capa de origen inválida"
    INVALID_TARGET_LAYER = "Capa de destino inválida"
    INVALID_INPUT_LAYER = "Capa de entrada inválida."
    FINAL_LAYER_NOT_FOUND = "Error: capa final no encontrada en el contexto."
    BUFFER_CANNOT_BE_ZERO = "El buffer no puede ser 0"
    ASYNC_STARTED = "La ejecución en segundo plano ha comenzado. Revise el registro para ver el progreso."
    ASYNC_START_ERROR = "Error al iniciar la ejecución asíncrona:"
    ASYNC_FINISHED = "La ejecución asíncrona se completó."
    ASYNC_EXECUTION_ERROR = "Error en la ejecución asíncrona:"
    FILES_LOADED_PREFIX = "Se cargaron"
    FILES_SUFFIX = "archivos."
    SETTINGS_SAVED_TITLE = "Configuración Guardada"
    SETTINGS_SAVED_MESSAGE = "La configuración se guardó correctamente."
    PREFERENCES_FOLDER_NOT_FOUND = "Carpeta de preferencias no encontrada:"
    ENTER_TEXT_TO_SEARCH = "Ingrese el texto a buscar."
    CONFIRM_REPLACEMENTS = "Confirmar reemplazos"
    SEARCH_LABEL = "Buscar:"
    REPLACE_WITH_LABEL = "Reemplazar por:"
    DESTRUCTIVE_OPERATION_WARNING = "Atención - operación destructiva"
    LAYOUTS_ANALYZED = "Diseños analizados:"
    CHANGES_APPLIED = "Reemplazos aplicados:"
    REPLACEMENT_COMPLETED_TITLE = "Reemplazo completado"
    PROJECT_BACKUP_INFO = (
        "Copia de seguridad: se creará una copia del proyecto (.qgz) en la carpeta backup junto al archivo del proyecto."
    )
    LAYER_MUST_BE_EDITABLE = "La capa debe estar en modo de edición"
    NO_ATTRIBUTE_SELECTED = "Ningún atributo seleccionado"
    ATTRIBUTES_COPIED_SUCCESS = (
        "Atributos copiados correctamente (cambios no guardados)"
    )
    REQUIRED_LIBRARY = "Biblioteca necesaria"
    PYPDF2_REQUIRED_MESSAGE = (
        "Para unir PDFs es necesario instalar el paquete PyPDF2.\n\n¿Desea instalarlo ahora?"
    )
    PILLOW_REQUIRED_MESSAGE = (
        "Para unir PNGs en PDF es necesario instalar el paquete Pillow.\n\n¿Desea instalarlo ahora?"
    )
    EXPORTING_LAYOUTS = "Exportando diseños..."
    FAILED_EXPORT_PDF = "Error al exportar PDF:"
    FAILED_EXPORT_PNG = "Error al exportar PNG:"
    ERROR_EXPORTING = "Error exportando"
    FAILED_MERGE_PDFS = "Error al unir PDFs:"
    FAILED_MERGE_PNGS = "Error al unir PNGs:"
    ERRORS_FOUND = "Errores encontrados:"
    LAYOUTS_EXPORTED_SUCCESS = "diseño(s) exportado(s) con éxito"
    PDFS_MERGED = "PDFs unidos"
    PNGS_MERGED = "PNGs unidos"
    EXPORT_LAYOUTS_COMPLETED = "Exportación de Diseños Completada"
    LOCATION_COPIED_TO_CLIPBOARD = "Ubicación copiada al portapapeles"
    ADDRESS_COPIED_TO_CLIPBOARD = "Dirección copiada al portapapeles"

    # plugins/DroneCoordinates.py
    DRONE_COORDINATES_TITLE = "Coordenadas del Dron"
    RECURSIVE_SEARCH = "Buscar subcarpetas"
    PHOTOS_METADATA = "Cruzar con metadatos de fotos"
    MRK_FOLDER = "Carpeta MRK:"
    SAVE_POINTS_CHECKBOX = "¿Guardar puntos MRK en archivo?"
    SAVE_IN = "Guardar en:"
    SAVE_TRACK_CHECKBOX = "¿Guardar la trayectoria en archivo?"
    APPLY_STYLE_POINTS = "¿Aplicar estilo (QML) a los puntos?"
    QML_POINTS = "QML de puntos:"
    APPLY_STYLE_TRACK = "¿Aplicar estilo (QML) a la trayectoria?"
    QML_TRACK = "QML:"

    # plugins/SettingsPlugin.py
    SETTINGS_TITLE = "Configuración de Cadmus"
    SETTINGS_CALCULATION_METHOD_ELLIPSOIDAL = "Elipsoidal"
    SETTINGS_CALCULATION_METHOD_CARTESIAN = "Cartesiana"
    SETTINGS_CALCULATION_METHOD_BOTH = "Ambos"

    # plugins/ReplaceInLayouts.py
    REPLACE_IN_LAYOUTS_TITLE = "Reemplazar Texto en Diseños"
    REPLACE_IN_LAYOUTS_SWAP = "Intercambiar"
    REPLACE_IN_LAYOUTS_RUN = "Ejecutar reemplazo"

    # plugins/LoadFolderLayers.py
    LOAD_FOLDER_LAYERS_TITLE = "Cargar Archivos de Carpeta"
    LOAD_FOLDER_LAYERS_RUN = "Cargar Archivos"

    # plugins/GenerateTrailPlugin.py
    GENERATE_TRAIL_TITLE = "Generar Rastro de Máquinas"

    # plugins/CopyAttributesPlugin.py
    COPY_ATTRIBUTES_TITLE = "Copiar Atributos de Vector"

    # plugins/ExportAllLayouts.py
    EXPORT_ALL_LAYOUTS_TITLE = "Exportar Todos los Diseños"
