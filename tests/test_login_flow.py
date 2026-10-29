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

    def _create_owner(self):
        setup = self.manager.get_screen("configurar")
        setup.ids.setup_username.text = "responsavel"
        setup.ids.setup_password.text = "Minha Senha Segura 2026!"
        setup.ids.setup_confirm.text = "Minha Senha Segura 2026!"
        self.assertTrue(setup.configure_account())
        self.assertEqual(self.manager.current, "login")

    def _login_owner(self):
        self.screen.ids.username_input.text = "responsavel"
        self.screen.ids.password_input.text = "Minha Senha Segura 2026!"
        self.assertTrue(self.screen.login())
        self.assertEqual(self.manager.current, "home")

    def test_first_run_requires_owner_setup(self):
        self.assertEqual(self.manager.current, "configurar")
        self.assertEqual(self.manager.auth_repository.count_users(), 0)
        self._create_owner()
        self._login_owner()
        self.assertEqual(self.screen.ids.password_input.text, "")

    def test_invalid_login_stays_on_login(self):
        self._create_owner()
        self.screen.ids.username_input.text = "responsavel"
        self.screen.ids.password_input.text = "incorreta"

        self.assertFalse(self.screen.login())
        self.assertEqual(self.manager.current, "login")
        self.assertEqual(
            self.screen.ids.feedback.text,
            "Usuário ou senha inválidos.",
        )

    def test_logout_clears_login_fields(self):
        self._create_owner()
        self._login_owner()
        self.screen.ids.feedback.text = "mensagem"
        home = self.manager.get_screen("home")
        self.assertTrue(home.logout())

        self.assertEqual(self.manager.current, "login")
        self.assertEqual(self.screen.ids.username_input.text, "")
        self.assertEqual(self.screen.ids.password_input.text, "")
        self.assertEqual(self.screen.ids.feedback.text, "")

    def test_demo_account_must_rotate_before_home(self):
        self.manager.auth_repository.create_user("admin", "classbase123")
        self.manager.current = "login"
        self.screen.ids.username_input.text = "admin"
        self.screen.ids.password_input.text = "classbase123"

        self.assertTrue(self.screen.login())
        self.assertEqual(self.manager.current, "alterar_senha")

        change = self.manager.get_screen("alterar_senha")
        change.ids.current_password.text = "classbase123"
        change.ids.new_password.text = "Senha Substituida 2026!"
        change.ids.confirm_password.text = "Senha Substituida 2026!"
        self.assertTrue(change.update_password())
        self.assertEqual(self.manager.current, "login")

        self.screen.ids.username_input.text = "admin"
        self.screen.ids.password_input.text = "Senha Substituida 2026!"
        self.assertTrue(self.screen.login())
        self.assertEqual(self.manager.current, "home")


if __name__ == "__main__":
    unittest.main()
