from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager

import sys

from Config import Config
from Dialog import EngineDialog, LanguageDialog
from IndexPage import IndexPage
from PreferencesPage import PreferencesPage


class MathTranslate(App):
    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)
        self.para_config = config

    def build(self):
        self.icon = "./static/icon.ico"
        self.title = "MathTranslate App"

        self.load_kv("guipage/index.kv")  # create a index.kv file
        self.load_kv("guipage/preferencespage.kv")  # create a image.kv file

        self.screen_manager = ScreenManager()
        pages = {"Index_page": IndexPage(self.para_config), "Preferences_page": PreferencesPage(self.para_config)}

        for item, page in pages.items():
            self.default_page = page
            # add page
            screen = Screen(name=item)
            screen.add_widget(self.default_page)
            # add page from screen manager
            self.screen_manager.add_widget(screen)
        return self.screen_manager


if __name__ == "__main__":
    sys.setrecursionlimit(3000)
    config = Config()
    MathTranslate(config).run()
