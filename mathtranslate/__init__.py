__version__ = "3.1.0"
__author__ = "MathTranslate developers"
import os
import shutil
import platform
import appdata

app_paths = appdata.AppDataPaths('mathtranslate')
app_dir = app_paths.app_data_path

"""
It appears that the `appdata` library might not follow the standard application data path conventions of macOS.
"""
# Check if the system is macOS
if platform.system() == 'Darwin':
    # Specify the new directory location for macOS
    mac_cache_path = os.path.expanduser("~/.cache/mathtranslate")
    
    # If the original directory exists
    if os.path.exists(app_dir):
        # Remove the target directory if it already exists
        if os.path.exists(mac_cache_path):
            shutil.rmtree(mac_cache_path)
        
        # Move the content of the original directory to the new location
        shutil.move(app_dir, mac_cache_path)
        
        # Update app_dir to point to the new location
        app_dir = mac_cache_path
    else:
        app_dir = mac_cache_path
else:
    app_dir = app_paths.app_data_path

# Ensure the directory is created
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
