from fitness_club.trainer import Trainer
from repositories.base import Repository


class TrainerRepository(Repository):
    def __init__(self, connection):
        self._connection = connection

    def save(self, trainer):
        with self._connection.cursor() as cur:
            cur.execute(
                "INSERT INTO trainers (name, specialization) VALUES (%s, %s) RETURNING id",
                (trainer.name, trainer.specialization),
            )
            trainer.id = cur.fetchone()[0]
        self._connection.commit()
        return trainer.id

    def get_by_id(self, trainer_id):
        with self._connection.cursor() as cur:
            cur.execute(
                "SELECT name, specialization FROM trainers WHERE id = %s",
                (trainer_id,),
            )
            row = cur.fetchone()
        if row is None:
            return None
        trainer = Trainer(row[0], row[1])
        trainer.id = trainer_id
        return trainer

    def list(self):
        with self._connection.cursor() as cur:
            cur.execute("SELECT id FROM trainers")
            ids = [r[0] for r in cur.fetchall()]
        return [self.get_by_id(i) for i in ids]