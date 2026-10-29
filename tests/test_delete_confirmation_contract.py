"""Contratos estáticos de confirmação; não exige Kivy instalado."""
import ast
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class DeleteConfirmationContractTests(unittest.TestCase):
    def _check(self, file_name, deletion_method):
        source = (ROOT / "screens" / file_name).read_text(encoding="utf-8")
        module = ast.parse(source)
        self.assertIn("from kivy.uix.checkbox import CheckBox", source)

        request = next(
            node for node in ast.walk(module)
            if isinstance(node, ast.FunctionDef) and node.name == "request_delete"
        )
        confirm = next(
            node for node in ast.walk(request)
            if isinstance(node, ast.FunctionDef) and node.name == "confirm_delete"
        )
        self.assertIsInstance(confirm.body[0], ast.If)
        self.assertIsInstance(confirm.body[0].test, ast.UnaryOp)
        self.assertIsInstance(confirm.body[0].test.op, ast.Not)
        self.assertEqual(
            ast.unparse(confirm.body[0].test.operand),
            "confirm_checkbox.active",
        )

        self.assertIn('delete_button = Button(text="Excluir", disabled=True)', source)
        self.assertIn("confirm_checkbox.bind(", source)
        self.assertIn("active=lambda _, selected:", source)
        self.assertIn("delete_button.bind(on_release=confirm_delete)", source)

        direct_calls = [
            call for call in ast.walk(request)
            if isinstance(call, ast.Call)
            and isinstance(call.func, ast.Attribute)
            and call.func.attr == deletion_method
        ]
        self.assertEqual(len(direct_calls), 1)
        self.assertTrue(
            any(call is direct_calls[0] for call in ast.walk(confirm)),
            "Exclusão só pode ser invocada na segunda ação confirmada.",
        )

    def test_course_delete_requires_explicit_confirmation(self):
        self._check("cursos.py", "delete_course")

    def test_student_delete_requires_explicit_confirmation(self):
        self._check("alunos.py", "delete_student")


if __name__ == "__main__":
    unittest.main()
