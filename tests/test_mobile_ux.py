import tempfile
import unittest
from pathlib import Path

from kivy.core.window import Window

from main import ClassBaseApp
from screens.cadastro import ERROR_COLOR, SUCCESS_COLOR


class MobileUxTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        db_path = Path(self.temp_dir.name) / "mobile-ux.db"
        self.app = ClassBaseApp(db_path=db_path)
        self.manager = self.app.build()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_keyboard_uses_resize_mode(self):
        self.assertEqual(Window.softinput_mode, "resize")

    def test_registration_success_uses_success_color(self):
        screen = self.manager.get_screen("cadastro")
        screen.ids.rm_input.text = "100"
        screen.ids.name_input.text = "Ana"
        screen.ids.course_input.text = "Administração"

        self.assertTrue(screen.register_student())
        self.assertEqual(tuple(screen.ids.feedback.color), SUCCESS_COLOR)

    def test_registration_error_uses_error_color(self):
        screen = self.manager.get_screen("cadastro")
        screen.ids.rm_input.text = ""
        screen.ids.name_input.text = "Ana"
        screen.ids.course_input.text = "Administração"

        self.assertFalse(screen.register_student())
        self.assertEqual(tuple(screen.ids.feedback.color), ERROR_COLOR)


if __name__ == "__main__":
    unittest.main()
