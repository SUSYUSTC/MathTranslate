import os

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.factory import Factory
from kivy.uix.popup import Popup


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
    cwdir = ObjectProperty(None)


class EngineDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
    # cwdir = ObjectProperty(None)


class LanguageDialog(FloatLayout):
    language = ObjectProperty(None)
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class TranslationDialog(FloatLayout):
    file = ObjectProperty(None)
    cwdir = ObjectProperty(None)
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class WaitingDialog(FloatLayout):
    pass


class DownloadDialog(BoxLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

    def download(self):
        os.system(f'pip install --upgrade mathtranslate')
        self.success_load()

    def success_load(self):
        content = SuccessDialog(cancel=self.success_dismiss_popup)
        self.success_popup = Popup(title="Upload the MathTranslate", content=content, size_hint=(.4, .5))
        self.success_popup.open()

    def success_dismiss_popup(self):
        self.success_popup.dismiss()


class SuccessDialog(BoxLayout):
    cancel = ObjectProperty(None)


class DownloadDialogEncapsulation:
    def download_load(self):
        content = DownloadDialog(load=self.down_load, cancel=self.download_dismiss_popup)
        self.down_popup = Popup(title="Upload the MathTranslate", content=content, size_hint=(.4, .5))
        self.down_popup.open()

    def down_load(self):
        self.down_popup()

    def download_dismiss_popup(self):
        self.down_popup.dismiss()


Factory.register("SuccessDialog", cls=SuccessDialog)
Factory.register("DownloadDialog", cls=DownloadDialog)
Factory.register("WaitingDialog", cls=WaitingDialog)
Factory.register("TranslationDialog", cls=TranslationDialog)
Factory.register("LanguageDialog", cls=LanguageDialog)
Factory.register("EngineDialog", cls=EngineDialog)
Factory.register("LoadDialog", cls=LoadDialog)
