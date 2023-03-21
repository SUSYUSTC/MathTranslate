__version__ = "1.1.1"
__author__ = "Jiace Sun"

import os
ROOT = os.path.dirname(os.path.abspath(__file__))
from . import config
from .translate_tex import translate_tex
