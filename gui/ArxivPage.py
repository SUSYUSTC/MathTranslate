import importlib
import os
import re
import sys

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from mathtranslate.translate_arxiv import translate_arxiv_4ui

from Dialog import LoadDialog, SavePathDialog, TranslationDialog

from mathtranslate.translate_tex import main

from Translate import translate_4arxiv


class ArxivPage(BoxLayout):
    def __init__(self, **kwargs):
        self.output_path = None
        self.number = None
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

    def back_index(*args):
        App.get_running_app().screen_manager.current = "Index_page"
        App.get_running_app().screen_manager.transition.direction = 'right'

    def dismiss_popup(self):
        self._popup.dismiss()

    def arxiv_load(self):
        # dirname = os.path.dirname(self.file_path)
        filename = os.path.join(self.config.default_loading_dir_path, 'translate.tex')
        content = SavePathDialog(load=self.arx_load, cancel=self.dismiss_popup, file=filename, dirname=self.config.default_loading_dir_path)
        self._popup = Popup(title="Output File Path Setting", content=content, size_hint=(.9, .9))
        self._popup.open()

    def arx_load(self, output_path):
        self.dismiss_popup()
        self.output_path = output_path
        if self.ids.number_input.text == '':
            self.ids.prompt.text = f'Output File Path: {output_path}'
        else:
            self.ids.prompt.text = f'The Number of Arxiv is: {self.ids.number_input.text}\n Output File Path: {output_path}'

    @staticmethod
    def get_translate_output(selection):
        if selection:
            selected = selection[0]
            if os.path.isdir(selected):
                return os.path.join(selected, 'translate.tex')
            else:
                return selected

    def number_input(self):
        self.number = self.ids.number_input.text
        if self.output_path == '':
            self.ids.prompt.text = f'The Number of Arxiv is: {self.ids.number_input.text}'
        else:
            self.ids.prompt.text = f'The Number of Arxiv is: {self.ids.number_input.text}\n Output File Path: {self.output_path}'


    def translate(self):
        # self.dismiss_popup()
        if not self.updated:
            self.dde.download_load()
            self.updated = True
        else:
            from Translate import translate
            import threading
            download_path = self.number.replace('/', '-')
            thread = threading.Thread(target=translate_4arxiv, args=(self.number, download_path,self.output_path,self.config))
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

        print(download_path)


