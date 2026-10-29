import hashlib
import hmac
import secrets
import sqlite3

from .connection import DEFAULT_DB_PATH, connect, initialize_database


PBKDF2_ITERATIONS = 200_000
MIN_PASSWORD_LENGTH = 12
MAX_PASSWORD_LENGTH = 128
DEMO_USERNAME = "admin"
DEMO_PASSWORD = "classbase123"


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

    @classmethod
    def _validate_new_password(cls, username, password):
        if not isinstance(password, str):
            raise ValueError("Senha inválida.")
        if len(password) < MIN_PASSWORD_LENGTH:
            raise ValueError("A senha deve ter pelo menos 12 caracteres.")
        if len(password) > MAX_PASSWORD_LENGTH:
            raise ValueError("A senha deve ter no máximo 128 caracteres.")
        if password != password.strip() or "\n" in password or "\r" in password:
            raise ValueError("A senha não pode começar ou terminar com espaços.")
        if password.casefold() in {DEMO_PASSWORD, username.casefold()}:
            raise ValueError("Escolha uma senha diferente da senha de teste e do usuário.")
        return password

    def create_user(self, username, password):
        """API legada para testes e migração; novas contas usam initialize_owner."""
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

    def initialize_owner(self, username, password):
        """Cria a conta inicial uma única vez, em transação atômica."""
        username = self._clean(username, "Usuário")
        if len(username) > 64:
            raise ValueError("O usuário deve ter no máximo 64 caracteres.")
        password = self._validate_new_password(username, password)
        salt = secrets.token_bytes(16)
        password_hash = self._hash_password(password, salt)

        with connect(self.db_path) as connection:
            connection.execute("BEGIN IMMEDIATE")
            if connection.execute(
                "SELECT 1 FROM usuarios LIMIT 1"
            ).fetchone() is not None:
                raise ValueError("A configuração inicial já foi concluída.")
            connection.execute(
                """
                INSERT INTO usuarios (usuario, salt, senha_hash)
                VALUES (?, ?, ?)
                """,
                (username, salt, password_hash),
            )
        return True

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

    def requires_demo_password_change(self, username):
        """Identifica contas legadas ainda protegidas por senha pública de demonstração."""
        return (
            str(username).strip() == DEMO_USERNAME
            and self.authenticate(DEMO_USERNAME, DEMO_PASSWORD)
        )

    def change_password(self, username, current_password, new_password):
        """Substitui o hash de forma atômica, sem alterar outros dados SQLite."""
        username = self._clean(username, "Usuário")
        new_password = self._validate_new_password(username, new_password)
        if not current_password or current_password == new_password:
            raise ValueError("Informe uma senha atual e uma nova senha diferente.")

        with connect(self.db_path) as connection:
            connection.execute("BEGIN IMMEDIATE")
            row = connection.execute(
                "SELECT id, salt, senha_hash FROM usuarios WHERE usuario = ?",
                (username,),
            ).fetchone()
            if row is None:
                return False

            candidate = self._hash_password(str(current_password), row["salt"])
            if not hmac.compare_digest(candidate, row["senha_hash"]):
                return False

            new_salt = secrets.token_bytes(16)
            new_hash = self._hash_password(new_password, new_salt)
            connection.execute(
                "UPDATE usuarios SET salt = ?, senha_hash = ? WHERE id = ?",
                (new_salt, new_hash, row["id"]),
            )
        return True

    def count_users(self):
        with connect(self.db_path) as connection:
            row = connection.execute("SELECT COUNT(*) AS total FROM usuarios").fetchone()
        return row["total"]
