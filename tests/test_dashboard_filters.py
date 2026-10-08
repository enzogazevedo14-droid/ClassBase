import tempfile
import time
import unittest
from pathlib import Path

from database import CourseRepository, StudentRepository
from main import ClassBaseApp


class RepositoryFilterTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "filters.db"
        self.students = StudentRepository(self.db_path)
        self.courses = CourseRepository(self.db_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_filter_students_by_course(self):
        self.students.create_student("100", "Ana", "Desenvolvimento de Sistemas")
        self.students.create_student("200", "Bruno", "Administração")

        results = self.students.list_students(course="Administração")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["nome"], "Bruno")

    def test_search_and_course_filter_can_be_combined(self):
        self.students.create_student("100", "Ana Silva", "Desenvolvimento de Sistemas")
        self.students.create_student("101", "Ana Lima", "Administração")
        self.students.create_student("102", "Bruno", "Administração")

        results = self.students.list_students(
            search="Ana",
            course="Administração",
        )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["rm"], "101")

    def test_order_students_by_rm(self):
        self.students.create_student("20", "Ana", "Desenvolvimento de Sistemas")
        self.students.create_student("10", "Carlos", "Desenvolvimento de Sistemas")

        results = self.students.list_students(order_by="rm")

        self.assertEqual([student["rm"] for student in results], ["10", "20"])

    def test_order_students_by_recent_creation(self):
        first_id = self.students.create_student(
            "1",
            "Primeiro",
            "Desenvolvimento de Sistemas",
        )
        time.sleep(0.002)
        second_id = self.students.create_student(
            "2",
            "Segundo",
            "Desenvolvimento de Sistemas",
        )

        results = self.students.list_students(order_by="recentes")

        self.assertEqual(results[0]["id"], second_id)
        self.assertEqual(results[1]["id"], first_id)

    def test_invalid_order_falls_back_to_name(self):
        self.students.create_student("2", "Carlos", "Desenvolvimento de Sistemas")
        self.students.create_student("1", "Ana", "Desenvolvimento de Sistemas")

        results = self.students.list_students(order_by="qualquer")

        self.assertEqual([student["nome"] for student in results], ["Ana", "Carlos"])

    def test_course_counts_use_group_by(self):
        self.students.create_student("1", "Ana", "Administração")
        self.students.create_student("2", "Bruno", "Administração")
        self.students.create_student("3", "Carlos", "Desenvolvimento de Sistemas")

        counts = {
            course["nome"]: course["total"]
            for course in self.courses.list_student_counts()
        }

        self.assertEqual(counts["Administração"], 2)
        self.assertEqual(counts["Desenvolvimento de Sistemas"], 1)
        self.assertEqual(counts["Recursos Humanos"], 0)


class DashboardAndFilterUiTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        db_path = Path(self.temp_dir.name) / "filters-ui.db"
        self.app = ClassBaseApp(db_path=db_path)
        self.manager = self.app.build()
        self.repo = self.manager.repository

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_home_shows_distribution_by_course(self):
        self.repo.create_student("1", "Ana", "Administração")
        self.repo.create_student("2", "Bruno", "Administração")
        self.repo.create_student("3", "Carlos", "Desenvolvimento de Sistemas")

        home = self.manager.get_screen("home")
        home.on_pre_enter()

        self.assertEqual(home.ids.student_count.text, "3")
        self.assertIn("Administração: 2", home.ids.course_summary.text)
        self.assertIn(
            "Desenvolvimento de Sistemas: 1",
            home.ids.course_summary.text,
        )

    def test_list_screen_filters_course_and_updates_result_count(self):
        self.repo.create_student("1", "Ana", "Administração")
        self.repo.create_student("2", "Bruno", "Desenvolvimento de Sistemas")

        screen = self.manager.get_screen("alunos")
        screen.refresh_filters()
        screen.ids.course_filter.text = "Administração"
        results = screen.refresh_students()

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["nome"], "Ana")
        self.assertEqual(screen.ids.result_count.text, "1 aluno encontrado")

    def test_list_screen_orders_by_rm(self):
        self.repo.create_student("20", "Ana", "Administração")
        self.repo.create_student("10", "Bruno", "Administração")

        screen = self.manager.get_screen("alunos")
        screen.refresh_filters()
        screen.ids.order_filter.text = "RM"
        results = screen.refresh_students()

        self.assertEqual([student["rm"] for student in results], ["10", "20"])


if __name__ == "__main__":
    unittest.main()
