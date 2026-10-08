from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager


class ClassBaseScreenManager(ScreenManager):
    repository = ObjectProperty(None, allownone=True)
    auth_repository = ObjectProperty(None, allownone=True)
    course_repository = ObjectProperty(None, allownone=True)
    history_repository = ObjectProperty(None, allownone=True)
