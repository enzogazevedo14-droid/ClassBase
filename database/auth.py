import hashlib
import hmac
import secrets
import sqlite3

from .connection import DEFAULT_DB_PATH, connect, initialize_database


PBKDF2_ITERATIONS = 200_000


class AuthRepository:
    def __init__(self, db_path=DEFAULT_DB_PATH):
        self.db_path = db_path
        initialize_database(self.db_path)

    @staticmethod
    def _clean(value, field_name):
        value = str(value).strip()
        if not value:
            raise ValueError(f"{field_name} é obrigatório.")
        return value

    @staticmethod
    def _hash_password(password, salt):
        return hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            PBKDF2_ITERATIONS,
        )

    def create_user(self, username, password):
        username = self._clean(username, "Usuário")
        password = self._clean(password, "Senha")
        salt = secrets.token_bytes(16)
        password_hash = self._hash_password(password, salt)

        try:
            with connect(self.db_path) as connection:
                cursor = connection.execute(
                    """
                    INSERT INTO usuarios (usuario, salt, senha_hash)
                    VALUES (?, ?, ?)
                    """,
                    (username, salt, password_hash),
                )
                return cursor.lastrowid
        except sqlite3.IntegrityError as exc:
            raise ValueError("Este usuário já existe.") from exc

    def authenticate(self, username, password):
        username = str(username).strip()
        password = str(password)

        if not username or not password:
            return False

        with connect(self.db_path) as connection:
            row = connection.execute(
                """
                SELECT salt, senha_hash
                FROM usuarios
                WHERE usuario = ?
                """,
                (username,),
            ).fetchone()

        if row is None:
            return False

        candidate_hash = self._hash_password(password, row["salt"])
        return hmac.compare_digest(candidate_hash, row["senha_hash"])

    def count_users(self):
        with connect(self.db_path) as connection:
            row = connection.execute(
                "SELECT COUNT(*) AS total FROM usuarios"
            ).fetchone()
        return row["total"]

    def ensure_default_user(self, username="admin", password="classbase123"):
        if self.count_users() == 0:
            self.create_user(username, password)
            return True
        return False
