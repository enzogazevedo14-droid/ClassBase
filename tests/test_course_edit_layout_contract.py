"""Static regression contract for Android course editing.

Does not import Kivy. Physical Android usability still requires manual QA.
"""
import ast
import unittest
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1] / "screens" / "cursos.py"


class CourseEditLayoutContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        text = SOURCE.read_text(encoding="utf-8")
        cls.source_text = text
        cls.tree = ast.parse(text)
        cls.open_edit = next(
            node for node in ast.walk(cls.tree)
            if isinstance(node, ast.FunctionDef) and node.name == "open_edit"
        )

    def test_actions_appear_above_text_input(self):
        source = ast.unparse(self.open_edit)
        self.assertLess(
            source.index("content.add_widget(actions)"),
            source.index("content.add_widget(name_input)"),
        )

    def test_keyboard_done_can_save(self):
        source = ast.unparse(self.open_edit)
        self.assertIn("name_input.bind(on_text_validate=save_course)", source)
        self.assertIn("save_button.bind(on_release=save_course)", source)

    def test_double_submission_guard_and_validation(self):
        source = ast.unparse(self.open_edit)
        self.assertIn("nonlocal saved", source)
        self.assertIn("if saved:\n", source)
        self.assertIn("saved = True", source)
        self.assertIn("except ValueError as exc:", source)


if __name__ == "__main__":
    unittest.main()
