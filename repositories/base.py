from abc import ABC, abstractmethod


class BaseRepository(ABC):


    table_name: str = None

    def __init__(self, connection):
        self._connection = connection

    @abstractmethod
    def _to_row(self, obj) -> dict:
        ...

    @abstractmethod
    def _from_row(self, row: dict):
        ...

    def save(self, obj):
        if obj.id is None:
            return self._insert(obj)
        return self._update(obj)

    def _insert(self, obj):
        data = self._to_row(obj)
        columns = list(data.keys())
        placeholders = ", ".join(["%s"] * len(columns))
        query = f"INSERT INTO {self.table_name} ({', '.join(columns)}) VALUES ({placeholders}) RETURNING id"
        with self._connection.cursor() as cur:
            cur.execute(query, list(data.values()))
            obj.id = cur.fetchone()[0]
        self._connection.commit()
        return obj.id

    def _update(self, obj):
        data = self._to_row(obj)
        set_clause = ", ".join(f"{col} = %s" for col in data.keys())
        query = f"UPDATE {self.table_name} SET {set_clause} WHERE id = %s"
        with self._connection.cursor() as cur:
            cur.execute(query, [*data.values(), obj.id])
        self._connection.commit()
        return obj.id

    def delete(self, obj):
        with self._connection.cursor() as cur:
            cur.execute(f"DELETE FROM {self.table_name} WHERE id = %s", (obj.id,))
        self._connection.commit()
        obj.id = None

    def get_by_id(self, obj_id):
        with self._connection.cursor() as cur:
            cur.execute(f"SELECT * FROM {self.table_name} WHERE id = %s", (obj_id,))
            row = cur.fetchone()
            if row is None:
                return None
            columns = [desc[0] for desc in cur.description]
        return self._from_row(dict(zip(columns, row)))

    def list(self):
        with self._connection.cursor() as cur:
            cur.execute(f"SELECT id FROM {self.table_name}")
            ids = [r[0] for r in cur.fetchall()]
        return [self.get_by_id(i) for i in ids]