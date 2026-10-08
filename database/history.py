from .connection import DEFAULT_DB_PATH, connect, initialize_database, utc_now


def record_history(
    connection,
    entity,
    record_id,
    action,
    description,
    created_at=None,
):
    connection.execute(
        """
        INSERT INTO historico (
            entidade,
            registro_id,
            acao,
            descricao,
            created_at
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            str(entity),
            record_id,
            str(action),
            str(description),
            created_at or utc_now(),
        ),
    )


class HistoryRepository:
    def __init__(self, db_path=DEFAULT_DB_PATH):
        self.db_path = db_path
        initialize_database(self.db_path)

    def list_events(self, entity="", limit=100):
        entity = str(entity).strip()
        try:
            limit = max(1, min(int(limit), 500))
        except (TypeError, ValueError):
            limit = 100

        with connect(self.db_path) as connection:
            if entity:
                rows = connection.execute(
                    """
                    SELECT
                        id,
                        entidade,
                        registro_id,
                        acao,
                        descricao,
                        created_at
                    FROM historico
                    WHERE entidade = ?
                    ORDER BY id DESC
                    LIMIT ?
                    """,
                    (entity, limit),
                ).fetchall()
            else:
                rows = connection.execute(
                    """
                    SELECT
                        id,
                        entidade,
                        registro_id,
                        acao,
                        descricao,
                        created_at
                    FROM historico
                    ORDER BY id DESC
                    LIMIT ?
                    """,
                    (limit,),
                ).fetchall()

        return [dict(row) for row in rows]

    def count_events(self):
        with connect(self.db_path) as connection:
            row = connection.execute(
                "SELECT COUNT(*) AS total FROM historico"
            ).fetchone()
        return row["total"]
