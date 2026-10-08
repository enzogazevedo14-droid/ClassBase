import tempfile
import unittest
from pathlib import Path

from database import CourseRepository, HistoryRepository, StudentRepository
from main import ClassBaseApp


class HistoryRepositoryTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "history.db"
        self.students = StudentRepository(self.db_path)
        self.courses = CourseRepository(self.db_path)
        self.history = HistoryRepository(self.db_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_default_database_creation_does_not_create_history(self):
        self.assertEqual(self.history.count_events(), 0)

    def test_student_create_update_and_delete_are_recorded(self):
        student_id = self.students.create_student(
            "100",
            "Ana",
            "Desenvolvimento de Sistemas",
        )
        self.students.update_student(
            student_id,
            "101",
            "Ana Souza",
            "Administração",
        )
        self.students.delete_student(student_id)

        events = self.history.list_events(entity="aluno")

        self.assertEqual(len(events), 3)
        self.assertEqual(
            [event["acao"] for event in events],
            ["excluido", "atualizado", "criado"],
        )
        self.assertEqual(events[0]["registro_id"], student_id)
        self.assertIn("Ana Souza", events[0]["descricao"])
        self.assertIn("RM: 100 → 101", events[1]["descricao"])
        self.assertIn(
            "Curso: Desenvolvimento de Sistemas → Administração",
            events[1]["descricao"],
        )

    def test_student_history_remains_after_student_is_deleted(self):
        student_id = self.students.create_student(
            "200",
            "Aluno Histórico",
            "Administração",
        )
        self.students.delete_student(student_id)

        self.assertIsNone(self.students.get_student(student_id))
        events = self.history.list_events(entity="aluno")

        self.assertEqual(len(events), 2)
        self.assertTrue(
            all(event["registro_id"] == student_id for event in events)
        )

    def test_failed_student_operation_does_not_create_history(self):
        self.students.create_student(
            "300",
            "Primeiro",
            "Desenvolvimento de Sistemas",
        )
        before = self.history.count_events()

        with self.assertRaises(ValueError):
            self.students.create_student(
                "300",
                "Duplicado",
                "Administração",
            )

        self.assertEqual(self.history.count_events(), before)

    def test_course_lifecycle_is_recorded(self):
        course_id = self.courses.create_course("Logística")
        self.courses.update_course(course_id, "Logística Integrada")
        self.courses.set_course_active(course_id, False)
        self.courses.set_course_active(course_id, True)
        self.courses.delete_course(course_id)

        events = self.history.list_events(entity="curso")

        self.assertEqual(
            [event["acao"] for event in events],
            ["excluido", "ativado", "desativado", "atualizado", "criado"],
        )
        self.assertTrue(
            all(event["registro_id"] == course_id for event in events)
        )

    def test_entity_filter_separates_student_and_course_events(self):
        self.courses.create_course("Mecatrônica")
        self.students.create_student(
            "400",
            "Aluno",
            "Administração",
        )

        student_events = self.history.list_events(entity="aluno")
        course_events = self.history.list_events(entity="curso")

        self.assertEqual(len(student_events), 1)
        self.assertEqual(len(course_events), 1)
        self.assertEqual(student_events[0]["entidade"], "aluno")
        self.assertEqual(course_events[0]["entidade"], "curso")

    def test_history_limit_is_bounded_and_newest_first(self):
        for index in range(5):
            self.courses.create_course(f"Curso {index}")

        events = self.history.list_events(limit=3)

        self.assertEqual(len(events), 3)
        self.assertGreater(events[0]["id"], events[1]["id"])
        self.assertGreater(events[1]["id"], events[2]["id"])


class HistoryUiTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        db_path = Path(self.temp_dir.name) / "history-ui.db"
        self.app = ClassBaseApp(db_path=db_path)
        self.manager = self.app.build()
        self.history_screen = self.manager.get_screen("historico")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_history_screen_shows_empty_state(self):
        events = self.history_screen.refresh_history()

        self.assertEqual(events, [])
        self.assertEqual(
            self.history_screen.ids.history_count.text,
            "0 ações registradas",
        )

    def test_history_screen_lists_and_filters_events(self):
        self.manager.course_repository.create_course("Logística")
        self.manager.repository.create_student(
            "500",
            "Aluno",
            "Administração",
        )

        events = self.history_screen.refresh_history()
        self.assertEqual(len(events), 2)
        self.assertEqual(
            self.history_screen.ids.history_count.text,
            "2 ações registradas",
        )

        self.history_screen.ids.entity_filter.text = "Alunos"
        student_events = self.history_screen.refresh_history()

        self.assertEqual(len(student_events), 1)
        self.assertEqual(student_events[0]["entidade"], "aluno")
        self.assertEqual(
            self.history_screen.ids.history_count.text,
            "1 ação registrada",
        )


if __name__ == "__main__":
    unittest.main()
