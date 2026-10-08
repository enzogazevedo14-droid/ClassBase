import tempfile
import unittest
from pathlib import Path

from main import ClassBaseApp


class CourseUiTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        db_path = Path(self.temp_dir.name) / "course-ui.db"
        self.app = ClassBaseApp(db_path=db_path)
        self.manager = self.app.build()
        self.screen = self.manager.get_screen("cursos")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_course_screen_creates_course_and_refreshes_student_spinner(self):
        self.screen.ids.course_name_input.text = "Logística"

        self.assertTrue(self.screen.create_course())
        self.assertIn("Logística", self.manager.get_screen("cadastro").ids.course_input.values)
        self.assertEqual(self.screen.ids.feedback.text, "Curso cadastrado com sucesso.")

    def test_duplicate_course_is_reported_in_ui(self):
        self.screen.ids.course_name_input.text = "Administração"

        self.assertFalse(self.screen.create_course())
        self.assertIn("Já existe", self.screen.ids.feedback.text)

    def test_inactive_course_is_removed_from_registration_choices(self):
        course_id = self.manager.course_repository.create_course("Mecatrônica")
        self.screen.refresh_courses()

        self.assertTrue(self.screen.toggle_course(course_id, True))
        registration = self.manager.get_screen("cadastro")

        self.assertNotIn("Mecatrônica", registration.ids.course_input.values)

    def test_unused_course_can_be_deleted_from_screen(self):
        course_id = self.manager.course_repository.create_course("Temporário")
        self.screen.refresh_courses()

        self.assertTrue(self.screen.delete_course(course_id))
        self.assertIsNone(self.manager.course_repository.get_course(course_id))

    def test_linked_course_delete_is_blocked_in_screen(self):
        course = next(
            course
            for course in self.manager.course_repository.list_courses()
            if course["nome"] == "Administração"
        )
        self.manager.repository.create_student("500", "Aluno", "Administração")

        self.assertFalse(self.screen.delete_course(course["id"]))
        self.assertIn("vinculado", self.screen.ids.feedback.text)


if __name__ == "__main__":
    unittest.main()
