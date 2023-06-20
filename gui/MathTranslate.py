from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from IndexPage import IndexPage
from PreferencesPage import PreferencesPage
from ArxivPage import ArxivPage
from FilePage import FilePage
import sys
from kivy.resources import resource_add_path
import win32timezone


class MathTranslate(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        self.title = "MathTranslate App"

        self.load_kv("guipage/page.kv")
        self.load_kv("guipage/preferencespage.kv")
        self.load_kv("guipage/dialog.kv")
        self.load_kv("guipage/file.kv")

        self.screen_manager = ScreenManager()
        pages = {"Index_page": IndexPage(), "Preferences_page": PreferencesPage(), "Arxiv_page": ArxivPage(),
                 "File_page": FilePage()}

        for item, page in pages.items():
            self.default_page = page
            # add page
            screen = Screen(name=item)
            screen.add_widget(self.default_page)
            # add page from screen manager
            self.screen_manager.add_widget(screen)
        return self.screen_manager


if __name__ == "__main__":
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(sys._MEIPASS)
    sys.setrecursionlimit(50000)
    MathTranslate().run()
