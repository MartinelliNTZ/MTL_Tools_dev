import os
import json
from qgis.PyQt.QtCore import QStandardPaths

PREF_FOLDER = os.path.join(
    QStandardPaths.writableLocation(QStandardPaths.AppDataLocation),
    "MTLTools"
)

PREF_FILE = os.path.join(PREF_FOLDER, "mtl_prefs.json")

def _ensure_pref_folder():
    os.makedirs(PREF_FOLDER, exist_ok=True)
    if not os.path.exists(PREF_FILE):
        with open(PREF_FILE, "w", encoding="utf-8") as f:
            f.write("{}")

def load_prefs():
    """Carrega todo o JSON de preferências."""
    _ensure_pref_folder()
    try:
        with open(PREF_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_prefs(data):
    """Salva o JSON inteiro de preferências."""
    _ensure_pref_folder()
    with open(PREF_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def load_tool_prefs(tool_key):
    """Carrega apenas as prefs da ferramenta específica."""
    prefs = load_prefs()
    return prefs.get(tool_key, {})

def save_tool_prefs(tool_key, values: dict):
    """Salva prefs de uma ferramenta específica."""
    prefs = load_prefs()
    prefs[tool_key] = values
    save_prefs(prefs)
