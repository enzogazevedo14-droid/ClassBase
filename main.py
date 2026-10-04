from pathlib import Path

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

from screens import (
    EditStudentScreen,
    HomeScreen,
    LoginScreen,
    RegisterStudentScreen,
    StudentListScreen,
)


BASE_DIR = Path(__file__).resolve().parent
KV_DIR = BASE_DIR / "kv"
KV_FILES = ("login.kv", "home.kv", "cadastro.kv", "alunos.kv", "editar.kv")
_kv_loaded = False


def load_kv_files():
    global _kv_loaded
    if _kv_loaded:
        return

    for filename in KV_FILES:
        Builder.load_file(str(KV_DIR / filename))
    _kv_loaded = True


class ClassBaseApp(App):
    def build(self):
        self.title = "ClassBase"
        load_kv_files()

        manager = ScreenManager()
        manager.add_widget(LoginScreen(name="login"))
        manager.add_widget(HomeScreen(name="home"))
        manager.add_widget(RegisterStudentScreen(name="cadastro"))
        manager.add_widget(StudentListScreen(name="alunos"))
        manager.add_widget(EditStudentScreen(name="editar"))
        return manager


if __name__ == "__main__":
    ClassBaseApp().run()
