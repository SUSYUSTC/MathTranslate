from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup

from mathtranslate.config import default_engine, default_language_to, default_language_from
from mathtranslate.encoding import get_file_encoding
from mathtranslate.translate import TextTranslator, LatexTranslator

from Dialog import LoadDialog, TranslationDialog


class IndexPage(FloatLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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
        options.file = filename

    def dismiss_popup(self):
        self._popup.dismiss()

    def translate_load(self):
        print(options.file)
        content = TranslationDialog(load=self.trans_load, cancel=self.dismiss_popup, file=options.file)
        self._popup = Popup(title="Output File Path Setting", content=content, size_hint=(.9, .9))
        self._popup.open()

    def trans_load(self, output_path):
        print(output_path)
        options.o = output_path
        self.translate()
        self.dismiss_popup()
        # popup_wait.dismiss()

    def translate(self):
        if options.engine == 'tencent':
            if options.language_from == 'zh-CN':
                options.language_from = 'zh'
            if options.language_to == 'zh-CN':
                options.language_to = 'zh'
        text_translator = TextTranslator(options.engine, options.language_to, options.language_from)
        latex_translator = LatexTranslator(text_translator, options.debug)

        input_encoding = get_file_encoding(options.file)
        text_original = open(options.file, encoding=input_encoding).read()
        text_final = latex_translator.translate_full_latex(text_original)
        with open(options.o, "w", encoding='utf-8') as file:
            print(text_final, file=file)
