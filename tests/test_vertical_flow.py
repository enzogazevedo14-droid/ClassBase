import tempfile
import unittest
from pathlib import Path

from main import ClassBaseApp


class VerticalFlowTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        db_path = Path(self.temp_dir.name) / "integration.db"
        self.app = ClassBaseApp(db_path=db_path)
        self.manager = self.app.build()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_registration_reaches_sqlite_and_list(self):
        screen = self.manager.get_screen("cadastro")
        screen.ids.rm_input.text = " 12345 "
        screen.ids.name_input.text = " Ana Souza "
        screen.ids.course_input.text = "Desenvolvimento de Sistemas"

        self.assertTrue(screen.register_student())
        self.assertEqual(self.manager.repository.count_students(), 1)
        self.assertEqual(screen.ids.feedback.text, "Aluno cadastrado com sucesso.")

        list_screen = self.manager.get_screen("alunos")
        students = list_screen.refresh_students()

        self.assertEqual(len(students), 1)
        self.assertEqual(students[0]["rm"], "12345")
        self.assertEqual(students[0]["nome"], "Ana Souza")

    def test_duplicate_rm_is_reported_in_ui(self):
        screen = self.manager.get_screen("cadastro")

        screen.ids.rm_input.text = "123"
        screen.ids.name_input.text = "Ana"
        screen.ids.course_input.text = "Administração"
        self.assertTrue(screen.register_student())

        screen.ids.rm_input.text = "123"
        screen.ids.name_input.text = "Bruno"
        screen.ids.course_input.text = "Recursos Humanos"

        self.assertFalse(screen.register_student())
        self.assertIn("Já existe", screen.ids.feedback.text)
        self.assertEqual(self.manager.repository.count_students(), 1)

    def test_search_and_home_counter_use_repository(self):
        repo = self.manager.repository
        repo.create_student("100", "Ana Souza", "Desenvolvimento de Sistemas")
        repo.create_student("200", "Bruno Lima", "Administração")

        list_screen = self.manager.get_screen("alunos")
        results = list_screen.refresh_students("Bruno")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["rm"], "200")

        home = self.manager.get_screen("home")
        home.on_pre_enter()
        self.assertEqual(home.ids.student_count.text, "2")


if __name__ == "__main__":
    unittest.main()
