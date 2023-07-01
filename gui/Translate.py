from mathtranslate.config import config
from mathtranslate.translate_tex import main as main_texfile
from mathtranslate.translate_arxiv import main as main_arxiv
import sys
from PreferencesPage import PreferencesPage


class Redirect:
    def __init__(self, file_path):
        self.file_path = file_path

    def __enter__(self):
        self.f = open(self.file_path, 'w', encoding='utf-8')
        sys.stdout = self.f
        sys.stderr = self.f

    def __exit__(self, exc_type, exc_value, traceback):
        self.f.close()
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__


def translate_texfile(file_path, output_path):
    # redirect standard output to log file
        config.load()
        args = [file_path, "--threads", config.default_threads, '-o', output_path]
        try:
            main_texfile(args=args, require_updated=False)
            print()
            print('finished')
            print('file saved to', output_path)
        except BaseException:
            print('Translation failed')
            pass


def translate_arxiv(number, output_path):
    # redirect standard output to log file
    with Redirect(config.log_file):
        config.load()
        args = [number, '--threads', config.default_threads, '-o', output_path]
        try:
            main_arxiv(args=args, require_updated=False)
            print()
            print('finished')
            print('file saved to', output_path)
        except BaseException:
            print('Translation failed')
            pass
