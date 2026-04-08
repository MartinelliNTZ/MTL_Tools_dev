# -*- coding: utf-8 -*-
from dataclasses import dataclass


@dataclass
class Field:
    normalized: str
    core: str
    label: str
    attribute: str
    description: str
    level: int
