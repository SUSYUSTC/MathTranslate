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
    id = ObjectProperty(None)
    key = ObjectProperty(None)


class TranslationDialog(FloatLayout):
    cancel = ObjectProperty(None)


class LanguageDialog(FloatLayout):
    language = ObjectProperty(None)
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
    lang_from_show = ObjectProperty(None)
    lang_to_show = ObjectProperty(None)
    lang_list = ObjectProperty(None)


class SavePathDialog(FloatLayout):
    file = ObjectProperty(None)
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
    dirname = ObjectProperty(None)
    default_filename = ObjectProperty(None)

    def action_choose_file(self, selection):
        if selection:
            selected = selection[0]
            if os.path.isdir(selected):
                return os.path.join(selected, self.default_filename)
            else:
                return selected


Factory.register("LoadDialog", cls=LoadDialog)
Factory.register("SavePathDialog", cls=SavePathDialog)
Factory.register("LanguageDialog", cls=LanguageDialog)
Factory.register("EngineDialog", cls=EngineDialog)

'''
class DownloadDialog(BoxLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class DownloadDialogEncapsulation:
    def __init__(self):
        pass

    def download_load(self):
        content = DownloadDialog(load=self.download, cancel=self.download_dismiss_popup)
        self.down_popup = Popup(title="Update the MathTranslate", content=content, size_hint=(.4, .5))
        self.down_popup.open()

    def download_dismiss_popup(self):
        self.down_popup.dismiss()

    def download(self):
        os.system('pip install --upgrade mathtranslate')
        self.success_load()
        self.down_popup.dismiss()

    def success_load(self):
        content = SuccessDialog(cancel=self.success_dismiss_popup)
        self.success_popup = Popup(title="Success", content=content, size_hint=(.4, .5))
        self.success_popup.open()

    def success_dismiss_popup(self):
        self.success_popup.dismiss()


Factory.register("DownloadDialog", cls=DownloadDialog)
'''
