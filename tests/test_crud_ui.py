import tempfile
import unittest
from pathlib import Path

from main import ClassBaseApp


class CrudUiTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        db_path = Path(self.temp_dir.name) / "crud-ui.db"
        self.app = ClassBaseApp(db_path=db_path)
        self.manager = self.app.build()
        self.repo = self.manager.repository

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_edit_flow_updates_student(self):
        student_id = self.repo.create_student(
            "100", "Ana Souza", "Desenvolvimento de Sistemas"
        )

        list_screen = self.manager.get_screen("alunos")
        self.assertTrue(list_screen.open_edit(student_id))

        edit_screen = self.manager.get_screen("editar")
        self.assertEqual(self.manager.current, "editar")
        self.assertEqual(edit_screen.ids.rm_input.text, "100")

        edit_screen.ids.rm_input.text = "101"
        edit_screen.ids.name_input.text = "Ana Lima"
        edit_screen.ids.course_input.text = "Administração"

        self.assertTrue(edit_screen.save_student())

        student = self.repo.get_student(student_id)
        self.assertEqual(student["rm"], "101")
        self.assertEqual(student["nome"], "Ana Lima")
        self.assertEqual(student["curso"], "Administração")
        self.assertEqual(self.manager.current, "alunos")

    def test_edit_flow_reports_duplicate_rm(self):
        first_id = self.repo.create_student("100", "Ana", "Administração")
        self.repo.create_student("200", "Bruno", "Recursos Humanos")

        list_screen = self.manager.get_screen("alunos")
        list_screen.open_edit(first_id)
        edit_screen = self.manager.get_screen("editar")
        edit_screen.ids.rm_input.text = "200"

        self.assertFalse(edit_screen.save_student())
        self.assertIn("Já existe", edit_screen.ids.feedback.text)
        self.assertEqual(self.manager.current, "editar")

    def test_delete_flow_removes_student(self):
        student_id = self.repo.create_student("100", "Ana", "Administração")
        list_screen = self.manager.get_screen("alunos")

        self.assertTrue(list_screen.delete_student(student_id))
        self.assertEqual(self.repo.count_students(), 0)
        self.assertFalse(list_screen.delete_student(student_id))


if __name__ == "__main__":
    unittest.main()
