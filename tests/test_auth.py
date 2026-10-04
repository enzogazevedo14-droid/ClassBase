import sqlite3
import tempfile
import unittest
from pathlib import Path

from database import AuthRepository


class AuthRepositoryTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "auth.db"
        self.repo = AuthRepository(self.db_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_create_and_authenticate_user(self):
        self.repo.create_user("admin", "senha123")

        self.assertTrue(self.repo.authenticate("admin", "senha123"))
        self.assertFalse(self.repo.authenticate("admin", "errada"))
        self.assertFalse(self.repo.authenticate("inexistente", "senha123"))

    def test_password_is_not_stored_as_plain_text(self):
        self.repo.create_user("admin", "senha123")

        connection = sqlite3.connect(self.db_path)
        row = connection.execute(
            "SELECT salt, senha_hash FROM usuarios WHERE usuario = ?",
            ("admin",),
        ).fetchone()
        connection.close()

        self.assertIsInstance(row[0], bytes)
        self.assertIsInstance(row[1], bytes)
        self.assertNotEqual(row[1], b"senha123")
        self.assertNotIn(b"senha123", row[1])

    def test_duplicate_user_is_rejected(self):
        self.repo.create_user("admin", "senha123")

        with self.assertRaisesRegex(ValueError, "já existe"):
            self.repo.create_user("admin", "outra")

    def test_default_user_is_created_once(self):
        self.assertTrue(self.repo.ensure_default_user())
        self.assertFalse(self.repo.ensure_default_user())
        self.assertEqual(self.repo.count_users(), 1)
        self.assertTrue(self.repo.authenticate("admin", "classbase123"))


if __name__ == "__main__":
    unittest.main()
