from orm.model import Model
from fitness_club.training import Training
from db.connection import get_connection


class Booking(Model):
    table_name = "bookings"
    fields = ["client_id", "training_id", "created_at", "status"]

    def __init__(self, client, training, created_at):
        super().__init__()
        self.client = client
        self.training = training
        self.created_at = created_at
        self._status = "active"

    @property
    def status(self):
        return self._status

    def is_active(self):
        return self._status == "active"

    def cancel(self, connection=None, commit=True):
        self._status = "cancelled"
        if self.id is not None and connection is not None:
            self.save(connection, commit)

    def to_row(self):
        return {
            "client_id": self.client.id,
            "training_id": self.training.id,
            "created_at": self.created_at,
            "status": self._status,
        }

    @classmethod
    def from_row(cls, row):
        from repositories.client_repository import ClientRepository  # отложенный импорт — разрывает цикл

        connection = get_connection()
        training = Training.get(row["training_id"], connection)
        client = ClientRepository(connection).get_by_id(row["client_id"])
        obj = cls(client, training, row["created_at"])
        obj.id = row["id"]
        obj._status = row["status"]
        connection.close()
        return obj

    def __str__(self):
        return f"Запись: {self.client.name} → {self.training.name} [{self._status}]"