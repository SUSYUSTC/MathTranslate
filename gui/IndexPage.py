import importlib
import os

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup

from Dialog import LoadDialog, SavePathDialog, DownloadDialog, DownloadDialogEncapsulation, SuccessDialog, WaitingDialog, TranslationDialog
import re


class IndexPage(FloatLayout):

    def __init__(self, **kwargs):
        self.file_path = None
        self.output_path = None
        self.dde = DownloadDialogEncapsulation()
        try:
            importlib.import_module('mathtranslate')
            self.updated = True
        except ImportError:
            self.updated = False
        if self.updated:
            import mathtranslate
            from mathtranslate.config import config
            latest = mathtranslate.update.get_latest_version()
            self.updated = mathtranslate.__version__ == latest
            self.config = config
        super().__init__(**kwargs)

    @staticmethod
    def page_preferences(*args):
        App.get_running_app().screen_manager.current = "Preferences_page"
        App.get_running_app().screen_manager.transition.direction = 'left'

    def show_load(self):
        # 绑定加载和取消的方法
        cwdir = self.config.default_loading_dir
        content = LoadDialog(load=self._load, cancel=self.dismiss_popup, cwdir=cwdir)
        self._popup = Popup(title="Load Latex File", content=content, size_hint=(.9, .9))
        self._popup.open()

    def _load(self, path, filename):
        self.file_path = filename
        basename = os.path.basename(filename)
        dirname = os.path.dirname(filename)
        self.ids.loaded_filename.text = f'Loaded file: {basename}'
        self.config.set_variable_4ui(self.config.default_loading_dir_path, dirname)
        self.config.load()
        self.dismiss_popup()

    def dismiss_popup(self):
        self._popup.dismiss()

    def translate_load(self):
        if self.file_path is None:
            return
        dirname = os.path.dirname(self.file_path)
        filename = os.path.join(dirname, 'translate.tex')
        content = SavePathDialog(load=self.trans_load, cancel=self.dismiss_popup, file=filename, dirname=dirname)
        self._popup = Popup(title="Output File Path Setting", content=content, size_hint=(.9, .9))
        self._popup.open()

    def trans_load(self, output_path):
        self.dismiss_popup()
        self.output_path = output_path
        self.translate()
        # popup_wait.dismiss()

    @staticmethod
    def get_translate_output(selection):
        if selection:
            selected = selection[0]
            if os.path.isdir(selected):
                return os.path.join(selected, 'translate.tex')
            else:
                return selected

    def translate(self):
        #self.dismiss_popup()
        if not self.updated:
            self.dde.download_load()
            self.updated = True
        else:
            from Translate import translate
            import threading

            thread = threading.Thread(target=translate, args=(self.file_path, self.output_path))
            thread.start()

            content = TranslationDialog(cancel=self.dismiss_popup)
            self._popup = Popup(title="Translation output", content=content, size_hint=(.9, .9))
            self._popup.open()

            def update_progress(dt):
                # replace \r to original
                text = open(self.config.log_file, 'rb').read().decode('utf-8')
                normal_text = re.sub('.*\r', '', text)
                content.ids.translation_output.text = normal_text

            Clock.schedule_interval(update_progress, 0.1)

            def check_finish(dt):
                if not thread.is_alive():
                    content.ids.translation_button_close.disabled = False
                    content.ids.translation_button_close.text = 'Close'

            Clock.schedule_interval(check_finish, 0.1)
'''
    def successful_translate(self):
        content = SuccessDialog(cancel=self.success_dismiss_popup)
        self.success_popup = Popup(title="Successfully translated", content=content, size_hint=(.4, .5))
        self.success_popup.open()

    def success_dismiss_popup(self):
        self.success_popup.dismiss()
'''
