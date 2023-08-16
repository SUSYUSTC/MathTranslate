from mathtranslate.config import config
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

from Dialog import LanguageDialog, EngineDialog, ThreadsDialog


language_dict = {'Afrikaans': 'af',
                 'Irish': 'ga',
                 'Albanian': 'sq',
                 'Italian': 'it',
                 'Arabic': 'ar',
                 'Japanese': 'ja',
                 'Azerbaijani': 'az',
                 'Kannada': 'kn',
                 'Basque': 'eu',
                 'Korean': 'ko',
                 'Bengali': 'bn',
                 'Latin': 'la',
                 'Belarusian': 'be',
                 'Latvian': 'lv',
                 'Bulgarian': 'bg',
                 'Lithuanian': 'lt',
                 'Catalan': 'ca',
                 'Macedonian': 'mk',
                 'Chinese Simplified': 'zh-CN',
                 'Malay': 'ms',
                 'Chinese Traditional': 'zh-TW',
                 'Maltese': 'mt',
                 'Croatian': 'hr',
                 'Norwegian': 'no',
                 'Czech': 'cs',
                 'Persian': 'fa',
                 'Danish': 'da',
                 'Polish': 'pl',
                 'Dutch': 'nl',
                 'Portuguese': 'pt',
                 'English': 'en',
                 'Romanian': 'ro',
                 'Esperanto': 'eo',
                 'Russian': 'ru',
                 'Estonian': 'et',
                 'Serbian': 'sr',
                 'Filipino': 'tl',
                 'Slovak': 'sk',
                 'Finnish': 'fi',
                 'Slovenian': 'sl',
                 'French': 'fr',
                 'Spanish': 'es',
                 'Galician': 'gl',
                 'Swahili': 'sw',
                 'Georgian': 'ka',
                 'Swedish': 'sv',
                 'German': 'de',
                 'Tamil': 'ta',
                 'Greek': 'el',
                 'Telugu': 'te',
                 'Gujarati': 'gu',
                 'Thai': 'th',
                 'Haitian Creole': 'ht',
                 'Turkish': 'tr',
                 'Hebrew': 'iw',
                 'Ukrainian': 'uk',
                 'Hindi': 'hi',
                 'Urdu': 'ur',
                 'Hungarian': 'hu',
                 'Vietnamese': 'vi',
                 'Icelandic': 'is',
                 'Welsh': 'cy',
                 'Indonesian': 'id',
                 'Yiddish': 'yi'}
language_dict_inverse = {language_dict[k]: k for k in language_dict}


class PreferencesPage(BoxLayout):

    def __init__(self, **kwargs):
        #Clock.schedule_interval(self.update_language_format, 1)
        self.config = config
        super().__init__(**kwargs)
        self.ids.language_setting.text = self.config.default_language_from + "=>" + self.config.default_language_to

    def back_index(*args):
        App.get_running_app().screen_manager.current = "Index_page"
        App.get_running_app().screen_manager.transition.direction = 'right'

    def engine_show_load(self, text):
        self.config.set_variable_4ui(self.config.default_engine_path, text)
        self.config.load()
        if text == 'tencent':
            id = self.config.tencent_secret_id
            key = self.config.tencent_secret_key
            if id is None:
                id = ''
            if key is None:
                key = ''
            content = EngineDialog(load=self.engine_load, cancel=self.dismiss_popup, id=id, key=key)
            self._popup = Popup(title="Engine API Setting", content=content, size_hint=(.9, .9))
            self._popup.open()
            self.ids.EditThreadsButton.disabled = True
        else:
            self.ids.EditThreadsButton.disabled = False

    def language_show_load(self):
        lang_from_show = language_dict_inverse[self.config.default_language_from]
        lang_to_show = language_dict_inverse[self.config.default_language_to]
        lang_list = list(language_dict.keys())
        lang_list.sort()
        content = LanguageDialog(load=self.language_load, cancel=self.dismiss_popup, lang_from_show=lang_from_show, lang_to_show=lang_to_show, lang_list=lang_list)
        self._popup = Popup(title="Translation Language Setting", content=content, size_hint=(.9, .9))
        self._popup.open()

    def engine_load(self, id, key):
        self.config.set_variable_4ui(self.config.tencent_secret_id_path, id)
        self.config.set_variable_4ui(self.config.tencent_secret_key_path, key)
        self.config.load()
        self.dismiss_popup()

    def language_load(self, lang_from_show, lang_to_show):
        language_from = language_dict[lang_from_show]
        language_to = language_dict[lang_to_show]
        self.config.set_variable_4ui(self.config.default_language_from_path, language_from)
        self.config.set_variable_4ui(self.config.default_language_to_path, language_to)
        self.config.load()
        self.dismiss_popup()
        self.ids.language_setting.text = self.config.default_language_from + "=>" + self.config.default_language_to

    def dismiss_popup(self):
        self._popup.dismiss()

    def threads_show_load(self, text):
        self.config.set_variable_4ui(self.config.default_threads_path, text)
        self.config.load()
        self.threads = self.config.default_threads
        content = ThreadsDialog(load=self.threads_load, cancel=self.dismiss_popup, checkbox_update=self.checkbox_update, textinput_update=self.textinput_update, threads=self.config.default_threads)
        self._popup = Popup(title="Threads Setting", content=content, size_hint=(.9, .9))
        self._popup.open()

    def threads_load(self):
        self.config.set_variable_4ui(self.config.default_threads_path, self.threads)
        self.config.load()
        self.dismiss_popup()
        self.ids.EditThreadsButton.text = (str(self.config.default_threads) if self.config.default_threads != 0 else 'auto') + " Threads"

    def checkbox_update(self, checkbox_state, ThreadNumberInput):
        if checkbox_state:
            ThreadNumberInput.text = 'auto'
            ThreadNumberInput.readonly = True
            ThreadNumberInput.disabled = True
            self.threads = 0
        else:
            ThreadNumberInput.text = '1'
            ThreadNumberInput.disabled = False
            self.threads = 1

    def textinput_update(self, threads):
        self.threads = threads
