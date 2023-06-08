import os
import re
import threading
import mathtranslate
from mathtranslate.config import config
from Translate import translate_texfile
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from Dialog import LoadDialog, SavePathDialog, TranslationDialog


class IndexPage(FloatLayout):

    def __init__(self, **kwargs):
        self.file_path = None
        self.output_path = None
        #self.dde = DownloadDialogEncapsulation()
        latest_version = mathtranslate.update.get_latest_version()
        self.current_version = mathtranslate.__version__
        self.updated = self.current_version == latest_version
        self.config = config
        super().__init__(**kwargs)

    def dismiss_popup(self):
        self._popup.dismiss()

    @staticmethod
    def go_to_preference_page(*args):
        App.get_running_app().screen_manager.current = "Preferences_page"
        App.get_running_app().screen_manager.transition.direction = 'left'

    @staticmethod
    def go_to_arxiv_page(*args):
        App.get_running_app().screen_manager.current = "Arxiv_page"
        App.get_running_app().screen_manager.transition.direction = 'left'

    def open_dialog_select_texfile(self):
        cwdir = self.config.default_loading_dir
        content = LoadDialog(load=self.select_texfile, cancel=self.dismiss_popup, cwdir=cwdir)
        self._popup = Popup(title="Load Latex File", content=content, size_hint=(.9, .9))
        self._popup.open()

    def select_texfile(self, path, filename):
        self.file_path = filename
        basename = os.path.basename(filename)
        dirname = os.path.dirname(filename)
        self.ids.loaded_filename.text = f'Loaded file: {basename}'
        self.config.set_variable_4ui(self.config.default_loading_dir_path, dirname)
        self.config.load()
        self.dismiss_popup()

    def open_dialog_select_savepath(self):
        if self.file_path is None:
            return
        dirname = os.path.dirname(self.file_path)
        filename = os.path.join(dirname, 'translate.tex')
        content = SavePathDialog(load=self.select_savepath, cancel=self.dismiss_popup, file=filename, dirname=dirname, default_filename='translate.tex')
        self._popup = Popup(title="Output File Path Setting", content=content, size_hint=(.9, .9))
        self._popup.open()

    def select_savepath(self, output_path):
        self.dismiss_popup()
        self.output_path = output_path
        self.translate()
        # popup_wait.dismiss()

    def translate(self):
        #self.dismiss_popup()
        #if not self.updated:
        #    self.dde.download_load()
        #    self.updated = True
        #else:
        thread = threading.Thread(target=translate_texfile, args=(self.file_path, self.output_path))
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
