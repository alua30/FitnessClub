from db.connection import get_connection


class Model:

    table_name: str = None
    fields: list = []

    def __init__(self):
        self.id = None

    def to_row(self) -> dict:
        raise NotImplementedError

    @classmethod
    def from_row(cls, row: dict):
        raise NotImplementedError

    def save(self, connection=None):
        connection = connection or get_connection()
        data = self.to_row()
        if self.id is None:
            columns = list(data.keys())
            placeholders = ", ".join(["%s"] * len(columns))
            query = f"INSERT INTO {self.table_name} ({', '.join(columns)}) VALUES ({placeholders}) RETURNING id"
            with connection.cursor() as cur:
                cur.execute(query, list(data.values()))
                self.id = cur.fetchone()[0]
        else:
            set_clause = ", ".join(f"{col} = %s" for col in data.keys())
            query = f"UPDATE {self.table_name} SET {set_clause} WHERE id = %s"
            with connection.cursor() as cur:
                cur.execute(query, [*data.values(), self.id])
        connection.commit()
        return self.id

    def delete(self, connection=None):
        connection = connection or get_connection()
        with connection.cursor() as cur:
            cur.execute(f"DELETE FROM {self.table_name} WHERE id = %s", (self.id,))
        connection.commit()
        self.id = None

    @classmethod
    def get(cls, obj_id, connection=None):
        connection = connection or get_connection()
        with connection.cursor() as cur:
            cur.execute(f"SELECT * FROM {cls.table_name} WHERE id = %s", (obj_id,))
            row = cur.fetchone()
            if row is None:
                return None
            columns = [desc[0] for desc in cur.description]
        return cls.from_row(dict(zip(columns, row)))

    @classmethod
    def all(cls, connection=None):
        connection = connection or get_connection()
        with connection.cursor() as cur:
            cur.execute(f"SELECT id FROM {cls.table_name}")
            ids = [r[0] for r in cur.fetchall()]
        return [cls.get(i, connection) for i in ids]