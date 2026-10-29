import tempfile
import unittest
from pathlib import Path

from main import ClassBaseApp


class NavigationTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.app = ClassBaseApp(db_path=Path(self.temp_dir.name) / "navigation.db")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_app_contains_planned_screens(self):
        manager = self.app.build()
        self.assertEqual(
            manager.screen_names,
            [
                "login",
                "home",
                "cadastro",
                "alunos",
                "detalhes",
                "editar",
                "cursos",
                "historico",
                "configurar",
                "alterar_senha",
            ],
        )
        self.assertEqual(manager.current, "configurar")

    def test_navigation_targets_exist(self):
        manager = self.app.build()
        for screen_name in (
            "home",
            "cadastro",
            "alunos",
            "detalhes",
            "editar",
            "cursos",
            "historico",
            "login",
        ):
            manager.current = screen_name
            self.assertEqual(manager.current, screen_name)


if __name__ == "__main__":
    unittest.main()
