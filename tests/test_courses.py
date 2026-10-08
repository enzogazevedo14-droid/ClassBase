import sqlite3
import tempfile
import unittest
from pathlib import Path

from database import CourseRepository, StudentRepository
from database.connection import DEFAULT_COURSES, connect


class CourseRepositoryTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "courses.db"
        self.repo = CourseRepository(self.db_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_default_courses_are_created(self):
        names = [course["nome"] for course in self.repo.list_courses()]
        for expected in DEFAULT_COURSES:
            self.assertIn(expected, names)

    def test_create_update_deactivate_and_activate_course(self):
        course_id = self.repo.create_course("Logística")
        self.assertEqual(self.repo.get_course(course_id)["nome"], "Logística")

        self.assertTrue(self.repo.update_course(course_id, "Logística Integrada"))
        self.assertEqual(
            self.repo.get_course(course_id)["nome"],
            "Logística Integrada",
        )

        self.assertTrue(self.repo.set_course_active(course_id, False))
        self.assertNotIn(
            course_id,
            [course["id"] for course in self.repo.list_courses()],
        )

        self.assertTrue(self.repo.set_course_active(course_id, True))
        self.assertIn(
            course_id,
            [course["id"] for course in self.repo.list_courses()],
        )

    def test_duplicate_course_name_is_rejected_case_insensitively(self):
        with self.assertRaisesRegex(ValueError, "Já existe"):
            self.repo.create_course("administração")

    def test_course_linked_to_student_cannot_be_deleted(self):
        student_repo = StudentRepository(self.db_path)
        course = next(
            c
            for c in self.repo.list_courses()
            if c["nome"] == "Desenvolvimento de Sistemas"
        )
        student_repo.create_student("100", "Ana", course["nome"])

        self.assertEqual(self.repo.count_students(course["id"]), 1)
        with self.assertRaisesRegex(ValueError, "vinculado"):
            self.repo.delete_course(course["id"])

    def test_unused_course_can_be_deleted(self):
        course_id = self.repo.create_course("Curso temporário")
        self.assertTrue(self.repo.delete_course(course_id))
        self.assertIsNone(self.repo.get_course(course_id))


class DatabaseMigrationTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "legacy.db"

    def tearDown(self):
        self.temp_dir.cleanup()

    def _create_v1_database(self):
        connection = sqlite3.connect(self.db_path)
        try:
            connection.execute(
                """
                CREATE TABLE alunos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    rm TEXT NOT NULL UNIQUE,
                    nome TEXT NOT NULL,
                    curso TEXT NOT NULL
                )
                """
            )
            connection.execute(
                """
                CREATE TABLE usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario TEXT NOT NULL UNIQUE,
                    salt BLOB NOT NULL,
                    senha_hash BLOB NOT NULL
                )
                """
            )
            connection.execute(
                """
                INSERT INTO alunos (rm, nome, curso)
                VALUES (?, ?, ?)
                """,
                ("900001", "Aluno legado", "Curso legado"),
            )
            connection.commit()
        finally:
            connection.close()

    def test_v1_student_data_is_preserved_in_v2_relationship(self):
        self._create_v1_database()

        student_repo = StudentRepository(self.db_path)
        course_repo = CourseRepository(self.db_path)

        students = student_repo.list_students()
        self.assertEqual(len(students), 1)
        self.assertEqual(students[0]["rm"], "900001")
        self.assertEqual(students[0]["curso"], "Curso legado")

        courses = course_repo.list_courses(include_inactive=True)
        self.assertIn("Curso legado", [course["nome"] for course in courses])

        with connect(self.db_path) as connection:
            columns = {
                row["name"]
                for row in connection.execute("PRAGMA table_info(alunos)")
            }
            version = connection.execute("PRAGMA user_version").fetchone()[0]

        self.assertIn("curso_id", columns)
        self.assertNotIn("curso", columns)
        self.assertEqual(version, 2)

    def test_migration_keeps_autoincrement_sequence_working(self):
        self._create_v1_database()
        student_repo = StudentRepository(self.db_path)
        course_repo = CourseRepository(self.db_path)
        course_repo.create_course("Novo curso")

        new_id = student_repo.create_student(
            "900002",
            "Novo aluno",
            "Novo curso",
        )

        self.assertGreater(new_id, 1)
        self.assertEqual(student_repo.get_student(new_id)["rm"], "900002")

    def test_migration_is_idempotent(self):
        self._create_v1_database()

        first = StudentRepository(self.db_path)
        second = StudentRepository(self.db_path)

        self.assertEqual(first.count_students(), 1)
        self.assertEqual(second.count_students(), 1)
        self.assertEqual(second.list_students()[0]["curso"], "Curso legado")


if __name__ == "__main__":
    unittest.main()
