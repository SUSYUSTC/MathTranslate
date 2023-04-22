from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

from Dialog import LanguageDialog, EngineDialog


class PreferencesPage(BoxLayout):

    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)
        self.config = config

    @staticmethod
    def back_index(*args):
        App.get_running_app().screen_manager.current = "Index_page"
        App.get_running_app().screen_manager.transition.direction = 'right'

    def engine_show_load(self, text):
        if text == 'Tencent':
            content = EngineDialog(load=self.engine_load, cancel=self.dismiss_popup)
            self._popup = Popup(title="Engine API Setting", content=content, size_hint=(.9, .9))
            self._popup.open()
            self.config.engine = 'tencent'

    def language_show_load(self):
        content = LanguageDialog(load=self.language_load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Translation Language Setting", content=content, size_hint=(.9, .9))
        self._popup.open()

    def engine_load(self, id, key):
        print(id, key)
        self.config.tencent_secret_id = id
        self.config.tencent_secret_key = key
        print(self.config.tencent_secret_id, self.config.tencent_secret_key)
        self.dismiss_popup()

    def language_load(self, language_from, language_to):
        print(language_from, language_to)
        # language_setting.text = language_from + ' to ' + language_to
        self.config.language_from = language_from
        self.config.language_to = language_to
        self.dismiss_popup()

    def dismiss_popup(self):
        self._popup.dismiss()
