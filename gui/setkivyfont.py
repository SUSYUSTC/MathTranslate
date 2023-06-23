from kivy.properties import StringProperty
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooser
font = StringProperty('yahei.ttf')
Label.font_name = font
TextInput.font_name = font
Button.font_name = font
FileChooser.font_name = font
