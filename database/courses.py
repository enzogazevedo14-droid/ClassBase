import sqlite3

from .connection import DEFAULT_DB_PATH, connect, initialize_database
from .history import record_history


class CourseRepository:
    def __init__(self, db_path=DEFAULT_DB_PATH):
        self.db_path = db_path
        initialize_database(self.db_path)

    @staticmethod
    def _clean_name(name):
        name = str(name).strip()
        if not name:
            raise ValueError("Nome do curso é obrigatório.")
        return name

    def create_course(self, name):
        name = self._clean_name(name)
        try:
            with connect(self.db_path) as connection:
                cursor = connection.execute(
                    "INSERT INTO cursos (nome, ativo) VALUES (?, 1)",
                    (name,),
                )
                course_id = cursor.lastrowid
                record_history(
                    connection,
                    "curso",
                    course_id,
                    "criado",
                    f"Curso {name} cadastrado.",
                )
                return course_id
        except sqlite3.IntegrityError as exc:
            raise ValueError("Já existe um curso com este nome.") from exc

    def get_course(self, course_id):
        with connect(self.db_path) as connection:
            row = connection.execute(
                "SELECT id, nome, ativo FROM cursos WHERE id = ?",
                (course_id,),
            ).fetchone()
        return dict(row) if row else None

    def list_courses(self, include_inactive=False):
        with connect(self.db_path) as connection:
            if include_inactive:
                rows = connection.execute(
                    """
                    SELECT id, nome, ativo
                    FROM cursos
                    ORDER BY ativo DESC, nome COLLATE NOCASE, id
                    """
                ).fetchall()
            else:
                rows = connection.execute(
                    """
                    SELECT id, nome, ativo
                    FROM cursos
                    WHERE ativo = 1
                    ORDER BY nome COLLATE NOCASE, id
                    """
                ).fetchall()
        return [dict(row) for row in rows]

    def list_student_counts(self, include_inactive=True):
        condition = "" if include_inactive else "WHERE c.ativo = 1"

        with connect(self.db_path) as connection:
            rows = connection.execute(
                f"""
                SELECT
                    c.id,
                    c.nome,
                    c.ativo,
                    COUNT(a.id) AS total
                FROM cursos AS c
                LEFT JOIN alunos AS a ON a.curso_id = c.id
                {condition}
                GROUP BY c.id, c.nome, c.ativo
                ORDER BY total DESC, c.nome COLLATE NOCASE, c.id
                """
            ).fetchall()

        return [dict(row) for row in rows]

    def update_course(self, course_id, name):
        name = self._clean_name(name)
        try:
            with connect(self.db_path) as connection:
                current = connection.execute(
                    "SELECT nome FROM cursos WHERE id = ?",
                    (course_id,),
                ).fetchone()

                if current is None:
                    return False

                if current["nome"] == name:
                    return True

                cursor = connection.execute(
                    "UPDATE cursos SET nome = ? WHERE id = ?",
                    (name, course_id),
                )

                if cursor.rowcount == 1:
                    description = (
                        f"Curso renomeado: {current['nome']} → {name}."
                    )
                    record_history(
                        connection,
                        "curso",
                        course_id,
                        "atualizado",
                        description,
                    )
                    return True

                return False
        except sqlite3.IntegrityError as exc:
            raise ValueError("Já existe um curso com este nome.") from exc

    def set_course_active(self, course_id, active):
        active = bool(active)

        with connect(self.db_path) as connection:
            current = connection.execute(
                "SELECT nome, ativo FROM cursos WHERE id = ?",
                (course_id,),
            ).fetchone()

            if current is None:
                return False

            desired = 1 if active else 0
            if current["ativo"] == desired:
                return True

            cursor = connection.execute(
                "UPDATE cursos SET ativo = ? WHERE id = ?",
                (desired, course_id),
            )

            if cursor.rowcount == 1:
                action = "ativado" if active else "desativado"
                record_history(
                    connection,
                    "curso",
                    course_id,
                    action,
                    f"Curso {current['nome']} {action}.",
                )
                return True

            return False

    def count_students(self, course_id):
        with connect(self.db_path) as connection:
            row = connection.execute(
                "SELECT COUNT(*) AS total FROM alunos WHERE curso_id = ?",
                (course_id,),
            ).fetchone()
        return row["total"]

    def delete_course(self, course_id):
        try:
            with connect(self.db_path) as connection:
                current = connection.execute(
                    "SELECT nome FROM cursos WHERE id = ?",
                    (course_id,),
                ).fetchone()

                if current is None:
                    return False

                cursor = connection.execute(
                    "DELETE FROM cursos WHERE id = ?",
                    (course_id,),
                )

                if cursor.rowcount == 1:
                    record_history(
                        connection,
                        "curso",
                        course_id,
                        "excluido",
                        f"Curso {current['nome']} excluído.",
                    )
                    return True

                return False
        except sqlite3.IntegrityError as exc:
            raise ValueError(
                "Não é possível excluir um curso vinculado a alunos."
            ) from exc
