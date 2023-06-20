import mathtranslate
from mathtranslate.config import config
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout


class IndexPage(FloatLayout):

    def __init__(self, **kwargs):
        self.file_path = None
        self.output_path = None
        #self.dde = DownloadDialogEncapsulation()
        self.latest_version = mathtranslate.update.get_latest_version()
        self.current_version = mathtranslate.__version__
        self.updated = self.current_version == self.latest_version
        self.current_version_text = f'[b] Current: {self.current_version} [/b]'
        if self.updated:
            self.latest_version_text = '[b] Already latest [/b]'
        else:
            self.latest_version_text = f'[b] Latest: {self.latest_version} [/b]'
        self.config = config
        super().__init__(**kwargs)

    @staticmethod
    def go_to_preference_page(*args):
        App.get_running_app().screen_manager.current = "Preferences_page"
        App.get_running_app().screen_manager.transition.direction = 'left'

    @staticmethod
    def go_to_arxiv_page(*args):
        App.get_running_app().screen_manager.current = "Arxiv_page"
        App.get_running_app().screen_manager.transition.direction = 'left'

    @staticmethod
    def go_to_file_page(*args):
        App.get_running_app().screen_manager.current = "File_page"
        App.get_running_app().screen_manager.transition.direction = 'left'
