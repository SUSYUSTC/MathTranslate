__version__ = "2.3.6"
__author__ = "MathTranslate developers"

import os
ROOT = os.path.dirname(os.path.abspath(__file__))
from . import cache
from . import config
from . import translate
from . import tencentcloud
from . import encoding
from . import process_latex
from . import process_text
from . import update
from . import translate_tex
from . import translate_arxiv
from .translate_tex import main as tex_main
from .translate_arxiv import main as arxiv_main
