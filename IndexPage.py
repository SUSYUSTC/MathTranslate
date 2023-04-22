import importlib
import os

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup

from Dialog import LoadDialog, TranslationDialog, DownloadDialog, DownloadDialogEncapsulation, SuccessDialog


class IndexPage(FloatLayout):

    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)
        self.config = config
        self.dde = DownloadDialogEncapsulation()
        self.config.updated = False
        try:
            importlib.import_module('mathtranslate')
            self.config.updated = True
        except ImportError:
            self.config.updated = False
        if self.config.updated:
            import mathtranslate
            latest = mathtranslate.update.get_latest_version()
            self.config.updated = mathtranslate.__version__ == latest

    @staticmethod
    def page_preferences(*args):
        App.get_running_app().screen_manager.current = "Preferences_page"
        App.get_running_app().screen_manager.transition.direction = 'left'

    def show_load(self):
        # 绑定加载和取消的方法
        # content = LoadDialog(load=self._load,cancel=self.dismiss_popup,cwdir=os.getcwd())
        content = LoadDialog(load=self._load, cancel=self.dismiss_popup, cwdir="./")
        self._popup = Popup(title="Load Latex File", content=content, size_hint=(.9, .9))
        self._popup.open()

    def _load(self, path, filename):
        self.dismiss_popup()
        self.config.file_path = filename

    def dismiss_popup(self):
        self._popup.dismiss()

    def translate_load(self):
        content = TranslationDialog(load=self.trans_load, cancel=self.dismiss_popup, cwdir='./',
                                    file=self.config.file_path)
        self._popup = Popup(title="Output File Path Setting", content=content, size_hint=(.9, .9))
        self._popup.open()

    def trans_load(self, output_path):
        self.config.output_path = output_path
        self.translate()
        self.dismiss_popup()
        # popup_wait.dismiss()

    def translate(self):
        if not self.config.updated:
            self.dde.download_load()

        else:
            from Translate import translate
            translate(self.config)
            self.success_load()

    def success_load(self):
        content = SuccessDialog(cancel=self.success_dismiss_popup)
        self.success_popup = Popup(title="Upload the MathTranslate", content=content, size_hint=(.4, .5))
        self.success_popup.open()

    def success_dismiss_popup(self):
        self.success_popup.dismiss()
