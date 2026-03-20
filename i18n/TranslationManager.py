# -*- coding: utf-8 -*-
from qgis.core import QgsApplication
from .Strings_pt_BR import Strings_pt_BR
# futuramente:
from .Strings_en import Strings_en
from .Strings_es import Strings_es

class TranslationManager:
    INGLES = "en"
    PORTUGUES_BR = "pt_BR"
    PORTUGES_PT = "pt_PT"
    ESPANHOL = "es"
    
    
    def __init__(self):
        self.locale = QgsApplication.locale()  # ex: 'pt_BR'
        self.lang = self.locale[:2]

        if self.locale == self.INGLES:
            self.STR = Strings_en()
            
        elif self.locale == self.ESPANHOL:
            self.STR = Strings_es()  # fallback
        else:
            self.STR = Strings_pt_BR()  
TM = TranslationManager()
STR = TM.STR
LOCALE = TM.locale
"""Locale: TranslationManager.INGLES,TranslationManager.PORTUGUES_BR,TranslationManager.ESPANHOL"""




#"Locale: pt_BR, Locale Name: pt_BR, Language: pt"
#"Locale: en, Locale Name: pt_BR, Language: en"
#"Locale: es, Locale Name: pt_BR, Language: es"
#"Locale: pt_PT, Locale Name: pt_BR, Language: pt"