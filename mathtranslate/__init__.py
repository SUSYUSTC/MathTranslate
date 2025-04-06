import os
import os

def _read_file(filename):
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, filename), encoding="utf-8") as f:
        return f.read().strip()

__version__ = _read_file("version.txt")
__author__ = _read_file("author.txt")
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
