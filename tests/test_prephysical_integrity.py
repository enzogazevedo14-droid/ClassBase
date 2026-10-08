import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from database import CourseRepository, HistoryRepository, StudentRepository
from database.connection import connect


class TransactionIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "integrity.db"
        self.students = StudentRepository(self.db_path)
        self.courses = CourseRepository(self.db_path)
        self.history = HistoryRepository(self.db_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_student_create_rolls_back_if_history_write_fails(self):
        with patch(
            "database.repository.record_history",
            side_effect=RuntimeError("history failure"),
        ):
            with self.assertRaisesRegex(RuntimeError, "history failure"):
                self.students.create_student(
                    "100",
                    "Ana",
                    "Desenvolvimento de Sistemas",
                )

        self.assertEqual(self.students.count_students(), 0)
        self.assertEqual(self.history.count_events(), 0)

    def test_student_update_rolls_back_if_history_write_fails(self):
        student_id = self.students.create_student(
            "100",
            "Ana",
            "Desenvolvimento de Sistemas",
        )
        before = self.students.get_student(student_id)
        before_history = self.history.count_events()

        with patch(
            "database.repository.record_history",
            side_effect=RuntimeError("history failure"),
        ):
            with self.assertRaisesRegex(RuntimeError, "history failure"):
                self.students.update_student(
                    student_id,
                    "101",
                    "Ana Souza",
                    "Administração",
                )

        after = self.students.get_student(student_id)
        self.assertEqual(after["rm"], before["rm"])
        self.assertEqual(after["nome"], before["nome"])
        self.assertEqual(after["curso"], before["curso"])
        self.assertEqual(after["updated_at"], before["updated_at"])
        self.assertEqual(self.history.count_events(), before_history)

    def test_student_delete_rolls_back_if_history_write_fails(self):
        student_id = self.students.create_student(
            "100",
            "Ana",
            "Desenvolvimento de Sistemas",
        )
        before_history = self.history.count_events()

        with patch(
            "database.repository.record_history",
            side_effect=RuntimeError("history failure"),
        ):
            with self.assertRaisesRegex(RuntimeError, "history failure"):
                self.students.delete_student(student_id)

        self.assertIsNotNone(self.students.get_student(student_id))
        self.assertEqual(self.history.count_events(), before_history)

    def test_course_create_rolls_back_if_history_write_fails(self):
        with patch(
            "database.courses.record_history",
            side_effect=RuntimeError("history failure"),
        ):
            with self.assertRaisesRegex(RuntimeError, "history failure"):
                self.courses.create_course("Curso com falha")

        names = [
            course["nome"]
            for course in self.courses.list_courses(include_inactive=True)
        ]
        self.assertNotIn("Curso com falha", names)

    def test_integrity_and_foreign_keys_remain_valid_after_crud(self):
        custom_id = self.courses.create_course("Logística")
        first_id = self.students.create_student("101", "Ana", "Logística")
        second_id = self.students.create_student(
            "102",
            "Bruno",
            "Desenvolvimento de Sistemas",
        )
        self.students.update_student(
            first_id,
            "101",
            "Ana Souza",
            "Administração",
        )
        self.students.delete_student(second_id)
        self.courses.delete_course(custom_id)

        with connect(self.db_path) as connection:
            integrity = connection.execute("PRAGMA integrity_check").fetchone()[0]
            foreign_key_errors = connection.execute(
                "PRAGMA foreign_key_check"
            ).fetchall()

        self.assertEqual(integrity, "ok")
        self.assertEqual(foreign_key_errors, [])

    def test_search_text_is_data_not_sql(self):
        self.students.create_student(
            "100",
            "Ana",
            "Desenvolvimento de Sistemas",
        )

        malicious = "' OR 1=1; DROP TABLE alunos; --"
        results = self.students.list_students(search=malicious)

        self.assertEqual(results, [])
        self.assertEqual(self.students.count_students(), 1)

        with connect(self.db_path) as connection:
            table = connection.execute(
                """
                SELECT name
                FROM sqlite_master
                WHERE type = 'table' AND name = 'alunos'
                """
            ).fetchone()

        self.assertIsNotNone(table)

    def test_unknown_order_value_cannot_be_used_as_sql(self):
        self.students.create_student(
            "2",
            "Carlos",
            "Desenvolvimento de Sistemas",
        )
        self.students.create_student(
            "1",
            "Ana",
            "Desenvolvimento de Sistemas",
        )

        results = self.students.list_students(
            order_by="nome; DROP TABLE alunos; --"
        )

        self.assertEqual([row["nome"] for row in results], ["Ana", "Carlos"])
        self.assertEqual(self.students.count_students(), 2)


class LegacyVolumeMigrationTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "legacy-volume.db"

    def tearDown(self):
        self.temp_dir.cleanup()

    def _create_large_v1_database(self, total=120):
        course_names = (
            "Desenvolvimento de Sistemas",
            "Administração",
            "Curso Antigo A",
            "Curso Antigo B",
        )
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
            rows = [
                (
                    f"{900000 + index}",
                    f"Aluno {index:03d}",
                    course_names[index % len(course_names)],
                )
                for index in range(1, total + 1)
            ]
            connection.executemany(
                """
                INSERT INTO alunos (rm, nome, curso)
                VALUES (?, ?, ?)
                """,
                rows,
            )
            connection.commit()
        finally:
            connection.close()

    def test_large_v1_migration_preserves_all_students_and_courses(self):
        self._create_large_v1_database(total=120)

        students = StudentRepository(self.db_path)
        courses = CourseRepository(self.db_path)
        history = HistoryRepository(self.db_path)

        all_students = students.list_students()
        all_course_names = {
            course["nome"]
            for course in courses.list_courses(include_inactive=True)
        }

        self.assertEqual(len(all_students), 120)
        self.assertEqual(students.count_students(), 120)
        self.assertIn("Curso Antigo A", all_course_names)
        self.assertIn("Curso Antigo B", all_course_names)
        self.assertEqual(history.count_events(), 0)
        self.assertTrue(all(row["created_at"] for row in all_students))
        self.assertTrue(all(row["updated_at"] for row in all_students))

        with connect(self.db_path) as connection:
            integrity = connection.execute("PRAGMA integrity_check").fetchone()[0]
            foreign_key_errors = connection.execute(
                "PRAGMA foreign_key_check"
            ).fetchall()
            version = connection.execute("PRAGMA user_version").fetchone()[0]

        self.assertEqual(integrity, "ok")
        self.assertEqual(foreign_key_errors, [])
        self.assertEqual(version, 4)

    def test_migrated_database_can_continue_crud_normally(self):
        self._create_large_v1_database(total=40)
        students = StudentRepository(self.db_path)
        courses = CourseRepository(self.db_path)

        new_course_id = courses.create_course("Curso Novo")
        new_student_id = students.create_student(
            "999999",
            "Aluno Novo",
            "Curso Novo",
        )
        students.update_student(
            new_student_id,
            "999998",
            "Aluno Novo Editado",
            "Administração",
        )
        self.assertTrue(students.delete_student(new_student_id))
        self.assertTrue(courses.delete_course(new_course_id))

        self.assertEqual(students.count_students(), 40)

        with connect(self.db_path) as connection:
            self.assertEqual(
                connection.execute("PRAGMA integrity_check").fetchone()[0],
                "ok",
            )
            self.assertEqual(
                connection.execute("PRAGMA foreign_key_check").fetchall(),
                [],
            )


if __name__ == "__main__":
    unittest.main()
