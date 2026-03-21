# -*- coding: utf-8 -*-
from .Strings_pt_BR import Strings_pt_BR


class Strings_en(Strings_pt_BR):
    """ "Strings for English (en)"""

    # General
    APP_NAME = "Cadmus"

    # About
    ABOUT_CADMUS = "About Cadmus"
    VERSION = "Version"
    UPDATED_ON = "Updated on"
    CREATED_ON = "Created on"
    CREATOR = "Creator"
    LOCATION = "Location"

    # Buttons
    CLOSE = "Close"
    SAVE = "Save"
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
    IMPLEMENT_SIZE = "Implement size: (always in meters)"
    VECTOR_CALCULATION_METHOD = "Vector Calculation Method"
    VECTOR_FIELDS_PRECISION = "Vector field precision (decimal places):"
    ASYNC_THRESHOLD = "Async threshold (number of features):"
    CALCULATION_METHOD_LABEL = "Vector calculation method:"
    SEARCH_TEXT = "Text to search:"
    REPLACE_WITH_NEW_TEXT = "Replacement text (new):"
    SOURCE_LAYER_ATTRIBUTES = "Source layer attributes"
    EXPORT_OPTIONS = "Export Options"
    MAX_WIDTH_PNG = "Max Width for PNG (px):"
    USE_PROJECT_FOLDER = "Use project folder"
    EXPORT_PDF = "Export PDF"
    EXPORT_PNG = "Export PNG"
    MERGE_PDFS_FINAL = "Merge PDFs into final PDF"
    MERGE_PNGS_FINAL = "Merge PNGs into final PDF"
    REPLACE_EXISTING_FILES = "Replace existing files"
    WGS84_EPSG4326 = "WGS 84 (EPSG:4326)"
    UTM_SIRGAS_2000 = "UTM SIRGAS 2000"
    ALTIMETRY_OPENTOPO = "Altimetry (OpenTopoData)"
    APPROX_ALTITUDE_METERS = "Approximate altitude (m)"
    LATITUDE_DECIMAL = "Latitude (Decimal)"
    LONGITUDE_DECIMAL = "Longitude (Decimal)"
    LATITUDE_DMS = "Latitude (DMS)"
    LONGITUDE_DMS = "Longitude (DMS)"
    EASTING_X = "Easting (X)"
    NORTHING_Y = "Northing (Y)"
    ADDRESS_OSM = "Address (OSM):"
    COPY_WGS84_FULL = "Copy WGS 84 (Full)"
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
    FULL_LABEL_REPLACE = "Replace the entire label when the text is found"
    LOAD_ONLY_MISSING_FILES = "Load only files not yet loaded in the project"
    PRESERVE_FOLDER_STRUCTURE = "Create groups based on folder/subfolder structure"
    DO_NOT_GROUP_LAST_FOLDER = "Do not group the last folder"
    CREATE_PROJECT_BACKUP_IF_SAVED = (
        "Create a project backup before loading (only if already saved)"
    )

    # Common messages
    SUCCESS_MESSAGE = "Processing completed successfully."
    ERROR_LAYER_NOT_FOUND = "Error: Layer not found."
    SELECT_VALID_FOLDER = "Select a valid folder."
    SELECT_AT_LEAST_ONE_FILE_TYPE = "Select at least one file type."
    SELECT_AT_LEAST_ONE_EXPORT_FORMAT = "Select at least one format (PDF or PNG)"
    SELECT_VALID_LINE_LAYER = "Select a valid line layer."
    INVALID_SOURCE_LAYER = "Invalid source layer"
    INVALID_TARGET_LAYER = "Invalid target layer"
    INVALID_INPUT_LAYER = "Invalid input layer."
    FINAL_LAYER_NOT_FOUND = "Error: final layer not found in context."
    BUFFER_CANNOT_BE_ZERO = "Buffer cannot be 0"
    ASYNC_STARTED = "Background execution started. Check the log for progress."
    ASYNC_START_ERROR = "Error starting asynchronous execution:"
    ASYNC_FINISHED = "Asynchronous execution completed."
    ASYNC_EXECUTION_ERROR = "Error during asynchronous execution:"
    FILES_LOADED_PREFIX = "Loaded"
    FILES_SUFFIX = "files."
    SETTINGS_SAVED_TITLE = "Settings Saved"
    SETTINGS_SAVED_MESSAGE = "Settings were saved successfully."
    PREFERENCES_FOLDER_NOT_FOUND = "Preferences folder not found:"
    ENTER_TEXT_TO_SEARCH = "Enter the text to search."
    CONFIRM_REPLACEMENTS = "Confirm replacements"
    SEARCH_LABEL = "Search:"
    REPLACE_WITH_LABEL = "Replace with:"
    DESTRUCTIVE_OPERATION_WARNING = "Warning - destructive operation"
    LAYOUTS_ANALYZED = "Analyzed layouts:"
    CHANGES_APPLIED = "Applied replacements:"
    REPLACEMENT_COMPLETED_TITLE = "Replacement completed"
    PROJECT_BACKUP_INFO = (
        "Backup: a copy of the project (.qgz) will be created in the backup folder next to the project file."
    )
    LAYER_MUST_BE_EDITABLE = "The layer must be in editing mode"
    NO_ATTRIBUTE_SELECTED = "No attribute selected"
    ATTRIBUTES_COPIED_SUCCESS = (
        "Attributes copied successfully (changes not saved)"
    )
    REQUIRED_LIBRARY = "Required library"
    PYPDF2_REQUIRED_MESSAGE = (
        "To merge PDFs, the PyPDF2 package must be installed.\n\nDo you want to install it now?"
    )
    PILLOW_REQUIRED_MESSAGE = (
        "To merge PNGs into PDF, the Pillow package must be installed.\n\nDo you want to install it now?"
    )
    EXPORTING_LAYOUTS = "Exporting layouts..."
    FAILED_EXPORT_PDF = "Failed to export PDF:"
    FAILED_EXPORT_PNG = "Failed to export PNG:"
    ERROR_EXPORTING = "Error exporting"
    FAILED_MERGE_PDFS = "Failed to merge PDFs:"
    FAILED_MERGE_PNGS = "Failed to merge PNGs:"
    ERRORS_FOUND = "Errors found:"
    LAYOUTS_EXPORTED_SUCCESS = "layout(s) exported successfully!"
    PDFS_MERGED = "PDFs merged"
    PNGS_MERGED = "PNGs merged"
    EXPORT_LAYOUTS_COMPLETED = "Layout Export Completed"
    LOCATION_COPIED_TO_CLIPBOARD = "Location copied to clipboard"
    ADDRESS_COPIED_TO_CLIPBOARD = "Address copied to clipboard"

    # plugins/DroneCoordinates.py
    DRONE_COORDINATES_TITLE = "Drone Coordinates"
    RECURSIVE_SEARCH = "Search subfolders"
    PHOTOS_METADATA = "Cross with photo metadata"
    MRK_FOLDER = "MRK Folder:"
    SAVE_POINTS_CHECKBOX = "Save MRK points to file?"
    SAVE_IN = "Save in:"
    SAVE_TRACK_CHECKBOX = "Save track to file?"
    APPLY_STYLE_POINTS = "Apply style (QML) to points?"
    QML_POINTS = "QML points:"
    APPLY_STYLE_TRACK = "Apply style (QML) to track?"
    QML_TRACK = "QML:"

    # plugins/SettingsPlugin.py
    SETTINGS_TITLE = "Cadmus Settings"
    SETTINGS_CALCULATION_METHOD_ELLIPSOIDAL = "Ellipsoidal"
    SETTINGS_CALCULATION_METHOD_CARTESIAN = "Cartesian"
    SETTINGS_CALCULATION_METHOD_BOTH = "Both"

    # plugins/ReplaceInLayouts.py
    REPLACE_IN_LAYOUTS_TITLE = "Replace Text in Layouts"
    REPLACE_IN_LAYOUTS_SWAP = "Swap"
    REPLACE_IN_LAYOUTS_RUN = "Run replacement"

    # plugins/LoadFolderLayers.py
    LOAD_FOLDER_LAYERS_TITLE = "Load Folder Files"
    LOAD_FOLDER_LAYERS_RUN = "Load Files"

    # plugins/GenerateTrailPlugin.py
    GENERATE_TRAIL_TITLE = "Generate Machine Trail"

    # plugins/CopyAttributesPlugin.py
    COPY_ATTRIBUTES_TITLE = "Copy Vector Attributes"

    # plugins/ExportAllLayouts.py
    EXPORT_ALL_LAYOUTS_TITLE = "Export All Layouts"
