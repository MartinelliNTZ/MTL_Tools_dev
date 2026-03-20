from qgis.PyQt.QtCore import QCoreApplication

def get(string):
    return QCoreApplication.translate("StringsBR", string)

class StringsBR:
    """"Strings for Brazilian Portuguese (pt-BR)
    """
    # General
    APP_NAME = "Gerenciador de Senhas"
class StringsEN:
    """"Strings for English (en)
    """
    # General
    APP_NAME = "Password Manager"


