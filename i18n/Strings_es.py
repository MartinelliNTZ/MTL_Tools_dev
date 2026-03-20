# -*- coding: utf-8 -*-
from .Strings_pt_BR import Strings_pt_BR

class Strings_es(Strings_pt_BR):
    """ "Strings for Spanish (es)"""

    # General
    APP_NAME = "Cadmus"
    ABOUT_CADMUS = "Acerca de Cadmus"
    VERSION = "Version"
    UPDATED_ON = "Actualizado el"
    CREATED_ON = "Creado el"
    CREATOR = "Creador"
    LOCATION = "Ubicación"
    
    #botoes
    CLOSE = "Cerrar"
    
    #plugins/DroneCoordinates.py
    DRONE_COORDINATES_TITLE = "Coordenadas del Dron"
    RECURSIVE_SEARCH = "Buscar subcarpetas"
    PHOTOS_METADATA = "Cruzar con metadatos de fotos"
    MRK_FOLDER = "MRK:"
    OPTIONS = "Opciones"
    SAVING = "Guardado"
    STYLES = "Estilos"
    SAVE_POINTS_CHECKBOX = "¿Guardar puntos MRK en archivo?"
    SAVE_IN = "Guardar en:"
    SAVE_TRACK_CHECKBOX = "¿Guardar la trayectoria en archivo?"
    APPLY_STYLE_POINTS = "¿Aplicar estilo (QML) a los puntos?"
    QML_POINTS = "QML de puntos:"
    APPLY_STYLE_TRACK = "¿Aplicar estilo (QML) a la trayectoria?"
    QML_TRACK = "QML:"

    # Errores
    ERROR_LAYER_NOT_FOUND = "Error: Capa no encontrada."

    # Éxito
    SUCCESS_MESSAGE = "Procesamiento completado con éxito."