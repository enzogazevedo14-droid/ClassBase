import unittest

from main import ClassBaseApp


class NavigationTests(unittest.TestCase):
    def test_app_contains_planned_screens(self):
        app = ClassBaseApp()
        manager = app.build()

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
            ],
        )
        self.assertEqual(manager.current, "login")

    def test_navigation_targets_exist(self):
        app = ClassBaseApp()
        manager = app.build()

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
