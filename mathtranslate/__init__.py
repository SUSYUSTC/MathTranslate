__version__ = "2.1.9"
__author__ = "Jiace Sun"

import os
ROOT = os.path.dirname(os.path.abspath(__file__))
from . import config
from . import translate
from . import tencent
from . import encoding
from . import process_latex
from . import process_text
from . import translate_tex
from . import update
