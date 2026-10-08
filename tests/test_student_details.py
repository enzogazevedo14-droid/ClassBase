import tempfile
import unittest
from pathlib import Path

from main import ClassBaseApp


class StudentDetailTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        db_path = Path(self.temp_dir.name) / "details.db"
        self.app = ClassBaseApp(db_path=db_path)
        self.manager = self.app.build()
        self.repo = self.manager.repository

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_list_opens_student_details(self):
        student_id = self.repo.create_student(
            "700",
            "Aluno Detalhe",
            "Desenvolvimento de Sistemas",
        )

        list_screen = self.manager.get_screen("alunos")
        self.assertTrue(list_screen.open_detail(student_id))

        detail = self.manager.get_screen("detalhes")
        self.assertEqual(self.manager.current, "detalhes")
        self.assertEqual(detail.ids.name_value.text, "Aluno Detalhe")
        self.assertEqual(detail.ids.rm_value.text, "700")
        self.assertEqual(
            detail.ids.course_value.text,
            "Desenvolvimento de Sistemas",
        )
        self.assertNotEqual(detail.ids.created_value.text, "-")
        self.assertNotEqual(detail.ids.updated_value.text, "-")

    def test_detail_screen_can_open_edit_for_same_student(self):
        student_id = self.repo.create_student(
            "701",
            "Aluno Editável",
            "Administração",
        )
        detail = self.manager.get_screen("detalhes")
        self.assertTrue(detail.load_student(student_id))

        self.assertTrue(detail.edit_student())
        edit = self.manager.get_screen("editar")

        self.assertEqual(self.manager.current, "editar")
        self.assertEqual(edit.student_id, student_id)
        self.assertEqual(edit.ids.rm_input.text, "701")
        self.assertEqual(edit.ids.name_input.text, "Aluno Editável")

    def test_missing_student_does_not_open_details(self):
        list_screen = self.manager.get_screen("alunos")

        self.assertFalse(list_screen.open_detail(99999))
        self.assertNotEqual(self.manager.current, "detalhes")


if __name__ == "__main__":
    unittest.main()
