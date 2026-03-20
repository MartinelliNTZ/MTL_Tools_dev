from qgis.PyQt.QtCore import QCoreApplication

def get(string):
    return QCoreApplication.translate("StringsBR", string)

class StringsBR:
    """"Strings for Brazilian Portuguese (pt-BR)
    """
    # General
    APP_NAME = get("Gerenciador de Senhas")

