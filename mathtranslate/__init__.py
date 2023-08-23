__version__ = "3.1.1"
__author__ = "MathTranslate developers"
import os
import appdata
app_paths = appdata.AppDataPaths('mathtranslate')
app_dir = app_paths.app_data_path
os.makedirs(app_dir, exist_ok=True)

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
