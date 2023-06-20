import os
import re
import threading
from Translate import translate_arxiv
from mathtranslate.config import config
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from Dialog import SavePathDialog, TranslationDialog


class ArxivPage(BoxLayout):
    def __init__(self, **kwargs):
        self.output_path = None
        self.number = ''
        self.config = config
        super().__init__(**kwargs)

    def back_index(*args):
        App.get_running_app().screen_manager.current = "Index_page"
        App.get_running_app().screen_manager.transition.direction = 'right'

    def dismiss_popup(self):
        self._popup.dismiss()

    def open_dialog_select_savepath(self):
        if self.number == '':
            return
        default_filename = 'arxiv.zip'
        filename = os.path.join(self.config.default_saving_dir, default_filename)
        print(self.config.default_saving_dir)
        content = SavePathDialog(load=self.select_savepath, cancel=self.dismiss_popup, file=filename, dirname=self.config.default_saving_dir, default_filename=default_filename)
        self._popup = Popup(title="Output File Path Setting", content=content, size_hint=(.9, .9))
        self._popup.open()

    def select_savepath(self, output_path):
        self.dismiss_popup()
        self.output_path = output_path
        dirname = os.path.dirname(output_path)
        self.config.set_variable_4ui(self.config.default_saving_dir_path, dirname)
        self.config.load()
        self.ids.prompt.text = f'The Number of Arxiv is: {self.ids.set_number.text}\n Output File Path: {output_path}'

    def set_number(self):
        self.number = self.ids.set_number.text
        if self.output_path is None:
            self.ids.prompt.text = f'The Arxiv number is: {self.number}\n Output File not specified'
        else:
            self.ids.prompt.text = f'The Arxiv number is: {self.number}\n Output File Path: {self.output_path}'

    def translate(self):
        # do not translate if arxiv number or output path not specified
        if (self.number == '') or (self.output_path is None):
            return
        thread = threading.Thread(target=translate_arxiv, args=(self.number, self.output_path))
        thread.start()

        content = TranslationDialog(cancel=self.dismiss_popup)
        self._popup = Popup(title="Translation output", content=content, size_hint=(.9, .9))
        self._popup.open()

        def update_progress(dt):
            # replace \r to original
            text = open(self.config.log_file, 'rb').read().decode('utf-8')
            text = text.replace('\r\n', '\n')
            normal_text = re.sub('.*\r', '', text)
            content.ids.translation_output.text = normal_text

        Clock.schedule_interval(update_progress, 0.1)

        def check_finish(dt):
            if not thread.is_alive():
                content.ids.translation_button_close.disabled = False
                content.ids.translation_button_close.text = 'Close'

        Clock.schedule_interval(check_finish, 0.1)
