__version__ = "1.2.0"
__author__ = "Jiace Sun"

import os
ROOT = os.path.dirname(os.path.abspath(__file__))
from . import config
from . import tencent
from . import translation
from .translation import translate
