# -*- coding: utf-8 -*-
from dataclasses import dataclass


@dataclass
class Field:
    """Representa a definicao de um metacampo catalogado no sistema."""
    normalized: str
    core: str
    label: str
    attribute: str
    description: str
    level: int
