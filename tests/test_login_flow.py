import tempfile
import unittest
from pathlib import Path

from main import ClassBaseApp


class LoginFlowTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        db_path = Path(self.temp_dir.name) / "login-flow.db"
        self.app = ClassBaseApp(db_path=db_path)
        self.manager = self.app.build()
        self.screen = self.manager.get_screen("login")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_default_login_opens_home(self):
        self.screen.ids.username_input.text = "admin"
        self.screen.ids.password_input.text = "classbase123"

        self.assertTrue(self.screen.login())
        self.assertEqual(self.manager.current, "home")
        self.assertEqual(self.screen.ids.password_input.text, "")

    def test_invalid_login_stays_on_login(self):
        self.screen.ids.username_input.text = "admin"
        self.screen.ids.password_input.text = "incorreta"

        self.assertFalse(self.screen.login())
        self.assertEqual(self.manager.current, "login")
        self.assertEqual(
            self.screen.ids.feedback.text,
            "Usuário ou senha inválidos.",
        )

    def test_logout_clears_login_fields(self):
        self.screen.ids.username_input.text = "admin"
        self.screen.ids.password_input.text = "classbase123"
        self.screen.ids.feedback.text = "mensagem"

        self.assertTrue(self.screen.login())
        home = self.manager.get_screen("home")
        self.assertTrue(home.logout())

        self.assertEqual(self.manager.current, "login")
        self.assertEqual(self.screen.ids.username_input.text, "")
        self.assertEqual(self.screen.ids.password_input.text, "")
        self.assertEqual(self.screen.ids.feedback.text, "")


if __name__ == "__main__":
    unittest.main()
