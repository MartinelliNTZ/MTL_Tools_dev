# -*- coding: utf-8 -*-
from .Strings_pt_BR import Strings_pt_BR

from qgis.PyQt.QtCore import QCoreApplication


class Strings_en(Strings_pt_BR):
    """Strings for English (en)"""

    # General
    APP_NAME = "Cadmus"

    # About
    ABOUT_CADMUS = "About Cadmus"
    VERSION = "Version"
    UPDATED_ON = "Last updated"
    CREATED_ON = "Created on"
    CREATOR = "Author"
    LOCATION = "Location"

    # Buttons
    CLOSE = "Close"
    SAVE = "Save"
    LOAD_FILES = "Load Files"
    EXPORT = "Export"
    CANCEL = "Cancel"
    EXECUTE = "Run"
    COPIED = "Copied"

    # Common labels
    OPTIONS = "Options"
    SAVING = "Saving"
    STYLES = "Styles"
    WARNING = "Warning"
    ERROR = "Error"
    ADVANCED_PARAMETERS = "Advanced Parameters"
    APP_PREFERENCES = "Application Preferences"
    OPEN_PREFERENCES_FOLDER = "Open Preferences Folder"
    FILE_TYPES = "File Types"
    ROOT_FOLDER = "Root folder:"
    OUTPUT_FOLDER = "Output folder:"
    INPUT_LINE_LAYER = "Line Layer (INPUT):"
    SOURCE_LAYER = "Source Layer:"
    TARGET_LAYER = "Target Layer:"
    IMPLEMENT_SIZE = "Implement width (meters):"
    VECTOR_CALCULATION_METHOD = "Vector Calculation Method"
    VECTOR_FIELDS_PRECISION = "Vector field precision (decimal places):"
    ASYNC_THRESHOLD = "Async threshold (feature count):"
    CALCULATION_METHOD_LABEL = "Vector calculation method:"
    SEARCH_TEXT = "Text to search:"
    REPLACE_WITH_NEW_TEXT = "Replace with:"
    SOURCE_LAYER_ATTRIBUTES = "Source layer attributes"
    EXPORT_OPTIONS = "Export Options"
    MAX_WIDTH_PNG = "Max PNG width (px):"
    USE_PROJECT_FOLDER = "Use project folder"
    EXPORT_PDF = "Export as PDF"
    EXPORT_PNG = "Export as PNG"
    MERGE_PDFS_FINAL = "Merge PDFs into final file"
    MERGE_PNGS_FINAL = "Convert PNGs into PDF"
    REPLACE_EXISTING_FILES = "Overwrite existing files"
    WGS84_EPSG4326 = "WGS 84 (EPSG:4326)"
    UTM_SIRGAS_2000 = "UTM SIRGAS 2000"
    ALTIMETRY_OPENTOPO = "Elevation (OpenTopoData)"
    APPROX_ALTITUDE_METERS = "Approx. elevation (m)"
    LATITUDE_DECIMAL = "Latitude (Decimal)"
    LONGITUDE_DECIMAL = "Longitude (Decimal)"
    LATITUDE_DMS = "Latitude (DMS)"
    LONGITUDE_DMS = "Longitude (DMS)"
    EASTING_X = "Easting (X)"
    NORTHING_Y = "Northing (Y)"
    ADDRESS_OSM = "Address (OSM):"
    COPY_WGS84_FULL = "Copy WGS84 (Full)"
    COPY_UTM_FULL = "Copy UTM (Full)"
    COPY_LOCATION_FULL = "Copy Location (Full)"
    POINT_COORDINATES = "Point Coordinates"
    ZONE = "Zone"
    HEMISPHERE = "Hemisphere"
    CITY = "City"
    INTERMEDIATE_REGION = "Intermediate Region"
    STATE = "State"
    REGION = "Region"
    COUNTRY = "Country"
    LOADING = "Loading..."
    LOADING_LOWER = "loading..."
    UNAVAILABLE = "Unavailable"

    # Common option labels
    CASE_SENSITIVE = "Case sensitive"
    FULL_LABEL_REPLACE = "Replace entire label when match is found"
    LOAD_ONLY_MISSING_FILES = "Load only files not already added to the project"
    PRESERVE_FOLDER_STRUCTURE = "Group layers based on folder/subfolder structure"
    DO_NOT_GROUP_LAST_FOLDER = "Do not group last folder level"
    CREATE_PROJECT_BACKUP_IF_SAVED = (
        "Create project backup before loading (if already saved)"
    )

    # Common messages
    SUCCESS_MESSAGE = "Processing completed successfully."
    ERROR_LAYER_NOT_FOUND = "Error: Layer not found."
    SELECT_VALID_FOLDER = "Please select a valid folder."
    SELECT_AT_LEAST_ONE_FILE_TYPE = "Select at least one file type."
    SELECT_AT_LEAST_ONE_EXPORT_FORMAT = "Select at least one format (PDF or PNG)"
    SELECT_VALID_LINE_LAYER = "Select a valid line layer."
    INVALID_SOURCE_LAYER = "Invalid source layer"
    INVALID_TARGET_LAYER = "Invalid target layer"
    INVALID_INPUT_LAYER = "Invalid input layer."
    FINAL_LAYER_NOT_FOUND = "Error: final layer not found in context."
    BUFFER_CANNOT_BE_ZERO = "Buffer cannot be zero"
    ASYNC_STARTED = "Background execution started. Check logs for progress."
    ASYNC_START_ERROR = "Error starting async execution:"
    ASYNC_FINISHED = "Async execution completed."
    ASYNC_EXECUTION_ERROR = "Error during async execution:"
    FILES_LOADED_PREFIX = "Loaded"
    FILES_SUFFIX = "files."
    SETTINGS_SAVED_TITLE = "Settings Saved"
    SETTINGS_SAVED_MESSAGE = "Settings saved successfully."
    PREFERENCES_FOLDER_NOT_FOUND = "Preferences folder not found:"
    ENTER_TEXT_TO_SEARCH = "Enter text to search."
    CONFIRM_REPLACEMENTS = "Confirm replacements"
    SEARCH_LABEL = "Search:"
    REPLACE_WITH_LABEL = "Replace with:"
    DESTRUCTIVE_OPERATION_WARNING = "Warning - destructive operation"
    LAYOUTS_ANALYZED = "Layouts analyzed:"
    CHANGES_APPLIED = "Replacements applied:"
    REPLACEMENT_COMPLETED_TITLE = "Replacement completed"
    PROJECT_BACKUP_INFO = "Backup: a copy of the project (.qgz) will be created in a backup folder next to the project file."
    LAYER_MUST_BE_EDITABLE = "Layer must be in edit mode"
    NO_ATTRIBUTE_SELECTED = "No attribute selected"
    ATTRIBUTES_COPIED_SUCCESS = "Attributes copied successfully (changes not saved)"
    REQUIRED_LIBRARY = "Required library"
    PYPDF2_REQUIRED_MESSAGE = "To merge PDFs, the PyPDF2 package is required.\n\nWould you like to install it now?"
    PILLOW_REQUIRED_MESSAGE = "To convert PNGs into PDF, the Pillow package is required.\n\nWould you like to install it now?"
    EXPORTING_LAYOUTS = "Exporting layouts..."
    FAILED_EXPORT_PDF = "Failed to export PDF:"
    FAILED_EXPORT_PNG = "Failed to export PNG:"
    ERROR_EXPORTING = "Error during export"
    FAILED_MERGE_PDFS = "Failed to merge PDFs:"
    FAILED_MERGE_PNGS = "Failed to merge PNGs:"
    ERRORS_FOUND = "Errors found:"
    LAYOUTS_EXPORTED_SUCCESS = "Layout(s) exported successfully!"
    PDFS_MERGED = "PDFs merged"
    PNGS_MERGED = "PNGs merged"
    EXPORT_LAYOUTS_COMPLETED = "Layout export completed"
    LOCATION_COPIED_TO_CLIPBOARD = "Location copied to clipboard"
    ADDRESS_COPIED_TO_CLIPBOARD = "Address copied to clipboard"

    # plugins/DroneCoordinates.py
    DRONE_COORDINATES_TITLE = "Drone Coordinates"
    DRONE_COORDINATES_TOOLTIP = (
        "Reads drone MRK files to generate photo points and flight path.\n"
        "Can match points with image metadata,\n"
        "save results to file, and apply QML styles\n"
        "to both points and generated track."
    )
    RECURSIVE_SEARCH = "Search subfolders"
    PHOTOS_METADATA = "Match with photo metadata"
    MRK_FOLDER = "MRK folder:"
    SAVE_POINTS_CHECKBOX = "Save MRK points to file?"
    SAVE_IN = "Save to:"
    SAVE_TRACK_CHECKBOX = "Save track to file?"
    APPLY_STYLE_POINTS = "Apply style (QML) to points?"
    QML_POINTS = "Points QML:"
    APPLY_STYLE_TRACK = "Apply style (QML) to track?"
    QML_TRACK = "QML:"

    # plugins/SettingsPlugin.py
    SETTINGS_TITLE = "Cadmus Settings"
    SETTINGS_TOOLTIP = (
        "Opens Cadmus global settings.\n"
        "Allows configuring the default vector calculation method,\n"
        "field precision, and feature threshold\n"
        "for asynchronous processing."
    )
    ELLIPSOIDAL = "Ellipsoidal"
    CARTESIAN = "Cartesian"
    BOTH = "Both"

    # plugins/ReplaceInLayouts.py
    REPLACE_IN_LAYOUTS_TITLE = "Replace Text in Layouts"
    REPLACE_IN_LAYOUTS_TOOLTIP = (
        "Searches for text in layout labels\n"
        "and replaces it with the provided value.\n"
        "Supports partial replacement or full label overwrite\n"
        "when a match is found."
    )
    REPLACE_IN_LAYOUTS_SWAP = "Swap"
    REPLACE_IN_LAYOUTS_RUN = "Run replacement"

    # plugins/LoadFolderLayers.py
    LOAD_FOLDER_LAYERS_TITLE = "Load Folder Layers"
    LOAD_FOLDER_LAYERS_TOOLTIP = (
        "Batch loads vector and raster files from a folder\n"
        "and its subfolders into the QGIS project.\n"
        "Supports file type filtering, duplicate avoidance,\n"
        "and layer grouping based on folder structure."
    )

    # plugins/GenerateTrailPlugin.py
    GENERATE_TRAIL_TITLE = "Generate Machine Trail"
    GENERATE_TRAIL_TOOLTIP = (
        "Generates the coverage area of an implement from a line layer.\n"
        "Converts the given width to the layer unit,\n"
        "applies a buffer using half of the value,\n"
        "and creates a new layer with the resulting trail."
    )

    # plugins/CopyAttributesPlugin.py
    COPY_ATTRIBUTES_TITLE = "Copy Vector Attributes"
    COPY_ATTRIBUTES_TOOLTIP = (
        "Copies the field structure from a source vector layer\n"
        "to a target vector layer.\n"
        "Allows selecting which attributes to create and handling\n"
        "name conflicts when fields already exist."
    )

    # plugins/ExportAllLayouts.py
    EXPORT_ALL_LAYOUTS_TITLE = "Export All Layouts"
    EXPORT_ALL_LAYOUTS_TOOLTIP = (
        "Exports all project layouts to PDF, PNG, or both.\n"
        "Can merge generated PDFs into a single file,\n"
        "convert PNGs into PDF, and control file overwrite\n"
        "in the output folder."
    )

    # plugins/VectorMultipartPlugin.py
    CONVERTER_MULTIPART_TITLE = "Convert Multipart"
    CONVERTER_MULTIPART_TOOLTIP = (
        "Processes multipart features in the active layer\n"
        "and splits them into single-part features.\n"
        "Can operate on selected features only\n"
        "or the entire layer, preserving attributes."
    )

    # plugins/CoordClickTool.py
    COORD_CLICK_TOOL_TITLE = "Capture Coordinates"
    COORD_CLICK_TOOL_TOOLTIP = (
        "Click on the map to retrieve point coordinates.\n"
        "Opens a dialog with WGS84, UTM, approximate elevation,\n"
        "and estimated address, along with copy options\n"
        "to the clipboard."
    )

    # core/ToolRegistry.py
    RESTART_QGIS_TITLE = "Save, Close and Reopen Project"
    RESTART_QGIS_TOOLTIP = (
        "Saves the current project, closes QGIS, and reopens it.\n"
        "Useful for recovering sessions after crashes\n"
        "or visual glitches without losing work."
    )
    LOGCAT_TITLE = "Log Viewer"
    LOGCAT_TOOLTIP = (
        "Opens the plugin log viewer.\n"
        "Allows inspecting messages, errors, and internal events\n"
        "recorded by Cadmus."
    )
    ABOUT_DIALOG_TOOLTIP = (
        f"Opens the {ABOUT_CADMUS} window of {APP_NAME}.\n"
        "Displays general information about the plugin,\n"
        "such as version, author, and project context."
    )
    VECTOR_FIELDS_TITLE = "Calculate Vector Fields"
    VECTOR_FIELDS_TOOLTIP = (
        "Automatically calculates vector fields such as area,\n"
        "length, or X/Y coordinates in the active layer.\n"
        "Useful for generating technical attributes\n"
        "without manual field editing."
    )
