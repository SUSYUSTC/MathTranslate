import os
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.factory import Factory


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
            
class ThreadsDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
    threads = ObjectProperty(None)
    checkbox_update = ObjectProperty(None)
    textinput_update = ObjectProperty(None)
        

Factory.register("LoadDialog", cls=LoadDialog)
Factory.register("SavePathDialog", cls=SavePathDialog)
Factory.register("LanguageDialog", cls=LanguageDialog)
Factory.register("EngineDialog", cls=EngineDialog)
Factory.register("ThreadsDialog", cls=ThreadsDialog)
