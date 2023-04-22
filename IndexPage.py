import os

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup

from Dialog import LoadDialog, TranslationDialog, DownloadDialog


class IndexPage(FloatLayout):

    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)
        self.config = config

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
        if self.config.engine == 'tencent':
            if self.config.language_from == 'zh-CN':
                self.config.language_from = 'zh'
            if self.config.language_to == 'zh-CN':
                self.config.anguage_to = 'zh'
        try:
            import mathtranslate
            latest = mathtranslate.update.get_latest_version()
            updated = mathtranslate.__version__ == latest


        except ImportError:
            updated = False

        if not updated:
            print('not updated')
            self.download_load()

        else:
            from Translate import translate
            translate(self.config)

    def download_load(self):
        print("11111")
        content = DownloadDialog(load=self.down_load, cancel=self.download_dismiss_popup)
        self.down_popup = Popup(title="Upload the MathTranslate", content=content, size_hint=(.4, .5))
        self.down_popup.open()

    def down_load(self):
        self.down_popup()

    def download_dismiss_popup(self):
        self.down_popup.dismiss()


