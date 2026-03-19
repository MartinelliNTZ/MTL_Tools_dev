# -*- coding: utf-8 -*-
import os


class InstructionsManager:
    """
    Gerenciador central de arquivos de instruções (.md)
    """

    BASE_PATH = os.path.dirname(__file__)

    # padrão
    STANDARD = os.path.join(BASE_PATH, "standard.md")

    # ferramentas
    COORD_CLICK = os.path.join(BASE_PATH, "coord_click_help.md")
    COPY_ATTRIBUTES = os.path.join(BASE_PATH, "copy_attributes_help.md")
    DRONE_COORDINATES = os.path.join(BASE_PATH, "drone_coordinates_help.md")
    EXPORT_ALL_LAYOUTS = os.path.join(BASE_PATH, "export_all_layouts_help.MD")
    GENERATE_TRAIL = os.path.join(BASE_PATH, "generate_trail_help.MD")
    LOAD_FOLDER = os.path.join(BASE_PATH, "load_folder_layers.MD")
    REPLACE_LAYOUTS = os.path.join(BASE_PATH, "replace_in_layouts_help.MD")
    RESTART_QGIS = os.path.join(BASE_PATH, "restart_qgis_help.md")
    SETTINGS = os.path.join(BASE_PATH, "settings_help.md")
    SETTINGS_OLD = os.path.join(BASE_PATH, "settings_help_old.md")
    VECTOR_FIELDS = os.path.join(BASE_PATH, "vector_fields_help.md")
    VECTOR_MULTIPART = os.path.join(BASE_PATH, "vector_multipart_help.md")
