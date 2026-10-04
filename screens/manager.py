from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager


class ClassBaseScreenManager(ScreenManager):
    repository = ObjectProperty(None, allownone=True)
