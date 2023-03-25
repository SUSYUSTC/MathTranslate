__version__ = "2.0.0"
__author__ = "Jiace Sun"

import os
ROOT = os.path.dirname(os.path.abspath(__file__))
from . import config
from . import translate
from . import tencent
from . import fix_encoding
from . import process_latex
from . import process_text
from . import translate_tex
