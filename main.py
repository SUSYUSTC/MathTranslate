from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager


import sys

from Dialog import EngineDialog, LanguageDialog
from IndexPage import IndexPage


class PreferencesPage(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def back_index(*args):
        App.get_running_app().screen_manager.current = "Index_page"
        App.get_running_app().screen_manager.transition.direction = 'right'

    def engine_show_load(self, text):
        if text == 'Tencent':
            content = EngineDialog(load=self.engine_load, cancel=self.dismiss_popup)
            self._popup = Popup(title="Engine API Setting", content=content, size_hint=(.9, .9))
            self._popup.open()
            options.engine = 'tencent'

    def language_show_load(self):
        content = LanguageDialog(load=self.language_load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Translation Language Setting", content=content, size_hint=(.9, .9))
        self._popup.open()

    def engine_load(self, id, key):
        print(id, key)
        options.tencent_secret_id = id
        options.tencent_secret_key = key
        self.dismiss_popup()

    def language_load(self, language_from, language_to):
        print(language_from, language_to)
        # language_setting.text = language_from + ' to ' + language_to
        options.language_from = language_from
        options.language_to = language_to
        self.dismiss_popup()

    def dismiss_popup(self):
        self._popup.dismiss()


class LaneDetectApp(App):
    def build(self):
        self.icon = "./static/icon.ico"
        self.title = "MathTranslate App"

        self.load_kv("gui/guipage/index.kv")  # create a index.kv file
        self.load_kv("gui/guipage/preferencespage.kv")  # create a image.kv file

        self.screen_manager = ScreenManager()
        pages = {"Index_page": IndexPage(), "Preferences_page": PreferencesPage()}

        for item, page in pages.items():
            self.default_page = page
            # add page
            screen = Screen(name=item)
            screen.add_widget(self.default_page)
            # add page from screen manager
            self.screen_manager.add_widget(screen)
        return self.screen_manager


if __name__ == "__main__":
    import argparse
    sys.setrecursionlimit(3000)
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", nargs='?', type=str, help='input file')
    parser.add_argument("--o", type=str, help='output path')
    parser.add_argument("-engine", default=default_engine,
                        help=f'translation engine, avaiable options include google and tencent. default is {default_engine}')
    parser.add_argument("-language_from", default=default_language_from,
                        help=f'language from, default is {default_language_from}')
    parser.add_argument("-language_to", default=default_language_to,
                        help=f'language to, default is {default_language_to}')
    # parser.add_argument("--list", action='store_true', help='list codes for languages')
    parser.add_argument("--setkey", action='store_true', help='set id and key of tencent translator')
    # parser.add_argument("--setdefault", action='store_true', help='set default translation engine and languages')
    parser.add_argument("--debug", action='store_true')
    # parser.add_argument("--compile", action='store_true')
    options = parser.parse_args()
    LaneDetectApp().run()

