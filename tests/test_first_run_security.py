"""Autenticação de primeira execução e troca obrigatória da senha de demonstração.

Não necessita Kivy ou instalação de SDK Android.
"""
import ast
import sqlite3
import tempfile
import unittest
from pathlib import Path

from database import AuthRepository, CourseRepository, StudentRepository


ROOT = Path(__file__).resolve().parents[1]


class FirstRunSecurityTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db_path = Path(self.tmp.name) / "secure.db"
        self.auth = AuthRepository(self.db_path)

    def tearDown(self):
        self.tmp.cleanup()

    def test_empty_database_has_no_known_login(self):
        self.assertEqual(self.auth.count_users(), 0)
        self.assertFalse(self.auth.authenticate("admin", "classbase123"))

    def test_owner_created_only_once_with_private_password(self):
        self.assertTrue(self.auth.initialize_owner("responsavel", "Minha Frase Segura 2026"))
        self.assertEqual(self.auth.count_users(), 1)
        self.assertTrue(self.auth.authenticate("responsavel", "Minha Frase Segura 2026"))
        self.assertFalse(self.auth.authenticate("admin", "classbase123"))
        with self.assertRaisesRegex(ValueError, "já foi concluída"):
            self.auth.initialize_owner("invasor", "Outra Frase Segura 2026")
        self.assertFalse(self.auth.authenticate("invasor", "Outra Frase Segura 2026"))

    def test_short_known_or_space_padded_password_is_rejected(self):
        for password in ("curta", "classbase123", "espacos no inicio ", "A" * 129):
            with self.subTest(password=password[:20]):
                with self.assertRaises(ValueError):
                    self.auth.initialize_owner("admin", password)
                self.assertEqual(self.auth.count_users(), 0)

    def test_invalid_username_does_not_create_owner(self):
        with self.assertRaises(ValueError):
            self.auth.initialize_owner("", "Minha Frase Segura 2026")
        with self.assertRaises(ValueError):
            self.auth.initialize_owner("x" * 65, "Minha Frase Segura 2026")
        self.assertEqual(self.auth.count_users(), 0)

    def test_owner_password_is_salted_and_not_plain_text(self):
        self.auth.initialize_owner("dono", "Uma senha bastante segura 2026")
        with sqlite3.connect(self.db_path) as db:
            row = db.execute(
                "SELECT salt, senha_hash FROM usuarios WHERE usuario = 'dono'"
            ).fetchone()
        self.assertEqual(len(row[0]), 16)
        self.assertEqual(len(row[1]), 32)
        self.assertNotEqual(row[1], b"Uma senha bastante segura 2026")

    def test_legacy_demo_user_must_change_password(self):
        self.auth.create_user("admin", "classbase123")
        self.assertTrue(self.auth.requires_demo_password_change("admin"))
        self.assertTrue(
            self.auth.change_password("admin", "classbase123", "Nova Senha Segura 2026!")
        )
        self.assertFalse(self.auth.requires_demo_password_change("admin"))
        self.assertFalse(self.auth.authenticate("admin", "classbase123"))
        self.assertTrue(self.auth.authenticate("admin", "Nova Senha Segura 2026!"))

    def test_wrong_old_password_does_not_change_hash(self):
        self.auth.create_user("admin", "classbase123")
        with sqlite3.connect(self.db_path) as db:
            before = db.execute("SELECT salt, senha_hash FROM usuarios").fetchone()
        self.assertFalse(
            self.auth.change_password("admin", "senha-invalida", "Nova Senha Segura 2026!")
        )
        with sqlite3.connect(self.db_path) as db:
            after = db.execute("SELECT salt, senha_hash FROM usuarios").fetchone()
        self.assertEqual(before, after)
        self.assertTrue(self.auth.requires_demo_password_change("admin"))

    def test_new_password_requires_policy_on_rotation(self):
        self.auth.create_user("admin", "classbase123")
        for password in ("poucos", "classbase123", "admin"):
            with self.subTest(password=password):
                with self.assertRaises(ValueError):
                    self.auth.change_password("admin", "classbase123", password)
        self.assertTrue(self.auth.authenticate("admin", "classbase123"))

    def test_custom_legacy_user_is_not_forced_to_change(self):
        self.auth.create_user("admin", "senha-personalizada-antiga")
        self.assertFalse(self.auth.requires_demo_password_change("admin"))

    def test_rotation_keeps_students_courses_and_history(self):
        self.auth.create_user("admin", "classbase123")
        courses = CourseRepository(self.db_path)
        students = StudentRepository(self.db_path)
        course_id = courses.create_course("Curso de Teste Seguranca")
        student_id = students.create_student(
            "990999", "Aluno Preservado", "Curso de Teste Seguranca"
        )
        before = students.get_student(student_id)
        self.assertTrue(
            self.auth.change_password("admin", "classbase123", "Nova Senha Segura 2026!")
        )
        after = StudentRepository(self.db_path).get_student(student_id)
        self.assertEqual(before, after)
        self.assertIsNotNone(CourseRepository(self.db_path).get_course(course_id))
        with sqlite3.connect(self.db_path) as db:
            self.assertEqual(db.execute("PRAGMA integrity_check").fetchone()[0], "ok")
            self.assertEqual(db.execute("PRAGMA foreign_key_check").fetchall(), [])


class AuthUIWiringContractTests(unittest.TestCase):
    def test_main_does_not_seed_default_user(self):
        text = (ROOT / "main.py").read_text(encoding="utf-8")
        self.assertNotIn("ensure_default_user", text)
        self.assertIn('manager.auth_repository.count_users() == 0', text)
        self.assertIn('InitialSetupScreen(name="configurar")', text)
        self.assertIn('ChangeDemoPasswordScreen(name="alterar_senha")', text)
        self.assertIn('"configuracao_inicial.kv"', text)
        self.assertIn('"alterar_senha.kv"', text)

    def test_login_requires_demo_password_upgrade_before_home(self):
        text = (ROOT / "screens" / "login.py").read_text(encoding="utf-8")
        tree = ast.parse(text)
        self.assertIn("requires_demo_password_change(username)", text)
        self.assertIn('self.manager.current = "alterar_senha"', text)
        self.assertIn('self.manager.current = "home"', text)
        self.assertIsNotNone(tree)

    def test_secure_setup_and_upgrade_have_masked_fields(self):
        setup = (ROOT / "kv" / "configuracao_inicial.kv").read_text(encoding="utf-8")
        change = (ROOT / "kv" / "alterar_senha.kv").read_text(encoding="utf-8")
        self.assertGreaterEqual(setup.count("password: True"), 2)
        self.assertGreaterEqual(change.count("password: True"), 3)
        self.assertIn("root.configure_account()", setup)
        self.assertIn("root.update_password()", change)


if __name__ == "__main__":
    unittest.main()
