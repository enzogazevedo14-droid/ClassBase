from pathlib import Path

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder

from database import (
    AuthRepository,
    CourseRepository,
    HistoryRepository,
    StudentRepository,
)
from screens import (
    ClassBaseScreenManager,
    CourseScreen,
    EditStudentScreen,
    HistoryScreen,
    HomeScreen,
    LoginScreen,
    RegisterStudentScreen,
    StudentDetailScreen,
    StudentListScreen,
)


BASE_DIR = Path(__file__).resolve().parent
KV_DIR = BASE_DIR / "kv"
KV_FILES = (
    "theme.kv",
    "login.kv",
    "home.kv",
    "cadastro.kv",
    "alunos.kv",
    "detalhes.kv",
    "editar.kv",
    "cursos.kv",
    "historico.kv",
)
_kv_loaded = False


def load_kv_files():
    global _kv_loaded
    if _kv_loaded:
        return

    for filename in KV_FILES:
        Builder.load_file(str(KV_DIR / filename))
    _kv_loaded = True


class ClassBaseApp(App):
    def __init__(self, db_path=None, **kwargs):
        super().__init__(**kwargs)
        self.db_path = Path(db_path) if db_path else None

    def build(self):
        self.title = "ClassBase"
        Window.softinput_mode = "resize"
        load_kv_files()

        database_path = self.db_path or Path(self.user_data_dir) / "classbase.db"
        manager = ClassBaseScreenManager()
        manager.repository = StudentRepository(database_path)
        manager.course_repository = CourseRepository(database_path)
        manager.history_repository = HistoryRepository(database_path)
        manager.auth_repository = AuthRepository(database_path)
        manager.auth_repository.ensure_default_user()
        manager.add_widget(LoginScreen(name="login"))
        manager.add_widget(HomeScreen(name="home"))
        manager.add_widget(RegisterStudentScreen(name="cadastro"))
        manager.add_widget(StudentListScreen(name="alunos"))
        manager.add_widget(StudentDetailScreen(name="detalhes"))
        manager.add_widget(EditStudentScreen(name="editar"))
        manager.add_widget(CourseScreen(name="cursos"))
        manager.add_widget(HistoryScreen(name="historico"))
        return manager


if __name__ == "__main__":
    ClassBaseApp().run()
