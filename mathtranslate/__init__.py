__version__ = "2.1.12"
__author__ = "MathTranslate developers"

import os
ROOT = os.path.dirname(os.path.abspath(__file__))
from . import config
from . import translate
from . import tencentcloud
from . import encoding
from . import process_latex
from . import process_text
from . import translate_tex
from . import update
