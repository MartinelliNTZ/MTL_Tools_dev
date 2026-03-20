# -*- coding: utf-8 -*-
from qgis.core import QgsApplication
from .Strings_pt_BR import Strings_pt_BR
# futuramente:
from .Strings_en import Strings_en

class TranslationManager:
    def __init__(self):
        self.locale = QgsApplication.locale()  # ex: 'pt_BR'
        self.lang = self.locale[:2]

        if self.locale == "pt_BR":
            self.STR = Strings_pt_BR()
        else:
            self.STR = Strings_en()  # fallback
TM = TranslationManager()
STR = TM.STR
#"Locale: pt_BR, Locale Name: pt_BR, Language: pt"
#"Locale: en, Locale Name: pt_BR, Language: en"
#"Locale: es, Locale Name: pt_BR, Language: es", "data"
#"Locale: pt_PT, Locale Name: pt_BR, Language: pt"