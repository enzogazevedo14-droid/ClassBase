import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView

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

    def test_main_content_screens_are_scrollable_when_needed(self):
        for screen_name in ("home", "cadastro", "editar", "detalhes"):
            screen = self.manager.get_screen(screen_name)
            self.assertIsInstance(
                screen.children[0],
                ScrollView,
                msg=f"{screen_name} deve permitir rolagem em telas menores.",
            )

    def test_course_edit_popup_uses_fixed_mobile_safe_height(self):
        screen = self.manager.get_screen("cursos")
        course = self.manager.course_repository.list_courses()[0]

        with patch.object(Popup, "open", autospec=True) as open_mock:
            self.assertTrue(screen.open_edit(course["id"]))

        popup = open_mock.call_args.args[0]
        self.assertIsNone(popup.size_hint_y)
        self.assertGreaterEqual(popup.height, dp(250))

    def test_long_history_description_has_extra_vertical_space(self):
        student_id = self.manager.repository.create_student(
            "900001",
            "Aluno com Nome Muito Longo para Teste de Interface",
            "Desenvolvimento de Sistemas",
        )
        self.manager.repository.update_student(
            student_id,
            "900002",
            "Aluno com Nome Ainda Mais Longo para Teste de Interface",
            "Administração",
        )

        screen = self.manager.get_screen("historico")
        events = screen.refresh_history()

        self.assertGreaterEqual(len(events), 2)
        first_card = screen.ids.history_list.children[-1]
        self.assertGreaterEqual(first_card.height, dp(140))

        description_labels = [
            child
            for child in first_card.children
            if getattr(child, "text", "") == events[0]["descricao"]
        ]
        self.assertEqual(len(description_labels), 1)
        self.assertGreaterEqual(description_labels[0].height, dp(72))


if __name__ == "__main__":
    unittest.main()
