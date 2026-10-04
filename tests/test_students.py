import tempfile
import unittest
from pathlib import Path

from database import StudentRepository


class StudentRepositoryTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test.db"
        self.repo = StudentRepository(self.db_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_create_and_get_student(self):
        student_id = self.repo.create_student("123", "Ana Souza", "DS")
        student = self.repo.get_student(student_id)

        self.assertEqual(student["rm"], "123")
        self.assertEqual(student["nome"], "Ana Souza")
        self.assertEqual(student["curso"], "DS")

    def test_rm_must_be_unique(self):
        self.repo.create_student("123", "Ana", "DS")

        with self.assertRaisesRegex(ValueError, "Já existe"):
            self.repo.create_student("123", "Bruno", "Administração")

    def test_required_fields_are_validated(self):
        with self.assertRaisesRegex(ValueError, "RM é obrigatório"):
            self.repo.create_student("   ", "Ana", "DS")

        with self.assertRaisesRegex(ValueError, "Nome é obrigatório"):
            self.repo.create_student("123", "", "DS")

        with self.assertRaisesRegex(ValueError, "Curso é obrigatório"):
            self.repo.create_student("123", "Ana", "   ")

    def test_values_are_trimmed(self):
        student_id = self.repo.create_student(
            " 123 ", " Ana Souza ", " Desenvolvimento de Sistemas "
        )
        student = self.repo.get_student(student_id)

        self.assertEqual(student["rm"], "123")
        self.assertEqual(student["nome"], "Ana Souza")
        self.assertEqual(student["curso"], "Desenvolvimento de Sistemas")

    def test_list_students_is_ordered_by_name(self):
        self.repo.create_student("2", "Carlos", "DS")
        self.repo.create_student("1", "Ana", "DS")

        students = self.repo.list_students()

        self.assertEqual([s["nome"] for s in students], ["Ana", "Carlos"])

    def test_search_finds_rm_name_and_course(self):
        self.repo.create_student("100", "Ana Souza", "Desenvolvimento de Sistemas")
        self.repo.create_student("200", "Bruno Lima", "Administração")

        self.assertEqual(len(self.repo.list_students("100")), 1)
        self.assertEqual(len(self.repo.list_students("ana")), 1)
        self.assertEqual(len(self.repo.list_students("Admin")), 1)

    def test_update_student(self):
        student_id = self.repo.create_student("123", "Ana", "DS")

        updated = self.repo.update_student(
            student_id, "124", "Ana Souza", "Administração"
        )
        student = self.repo.get_student(student_id)

        self.assertTrue(updated)
        self.assertEqual(student["rm"], "124")
        self.assertEqual(student["nome"], "Ana Souza")
        self.assertEqual(student["curso"], "Administração")

    def test_update_rejects_duplicate_rm(self):
        first_id = self.repo.create_student("100", "Ana", "DS")
        self.repo.create_student("200", "Bruno", "DS")

        with self.assertRaisesRegex(ValueError, "Já existe"):
            self.repo.update_student(first_id, "200", "Ana", "DS")

    def test_delete_student(self):
        student_id = self.repo.create_student("123", "Ana", "DS")

        self.assertTrue(self.repo.delete_student(student_id))
        self.assertIsNone(self.repo.get_student(student_id))
        self.assertFalse(self.repo.delete_student(student_id))

    def test_count_students(self):
        self.assertEqual(self.repo.count_students(), 0)
        self.repo.create_student("1", "Ana", "DS")
        self.repo.create_student("2", "Bruno", "DS")
        self.assertEqual(self.repo.count_students(), 2)

    def test_data_persists_between_repository_instances(self):
        self.repo.create_student("123", "Ana", "DS")

        reopened_repo = StudentRepository(self.db_path)

        self.assertEqual(reopened_repo.count_students(), 1)
        self.assertEqual(reopened_repo.list_students()[0]["rm"], "123")


if __name__ == "__main__":
    unittest.main()
