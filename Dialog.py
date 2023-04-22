from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.factory import Factory


class LoadDialog(FloatLayout):
    '''
    弹窗的加载和取消属性定义
    '''
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
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class WaitingDialog(FloatLayout):
    pass

Factory.register("WaitingDialog", cls=WaitingDialog)
Factory.register("TranslationDialog", cls=TranslationDialog)
Factory.register("LanguageDialog", cls=LanguageDialog)
Factory.register("EngineDialog", cls=EngineDialog)
Factory.register("LoadDialog", cls=LoadDialog)
