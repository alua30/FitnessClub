from fitness_club.training import Training
from repositories.trainer_repository import TrainerRepository
from repositories.base import Repository


class TrainingRepository(Repository):
    def __init__(self, connection):
        self._connection = connection
        self._trainer_repository = TrainerRepository(connection)

    def save(self, training):
        if training.trainer.id is None:
            self._trainer_repository.save(training.trainer)

        with self._connection.cursor() as cur:
            cur.execute(
                """INSERT INTO trainings (name, trainer_id, start_time, duration_minutes, capacity)
                   VALUES (%s, %s, %s, %s, %s) RETURNING id""",
                (training.name, training.trainer.id, training.start_time,
                 training.duration_minutes, training.capacity),
            )
            training.id = cur.fetchone()[0]
        self._connection.commit()
        return training.id

    def get_by_id(self, training_id):
        with self._connection.cursor() as cur:
            cur.execute(
                """SELECT name, trainer_id, start_time, duration_minutes, capacity
                   FROM trainings WHERE id = %s""",
                (training_id,),
            )
            row = cur.fetchone()
        if row is None:
            return None
        name, trainer_id, start_time, duration_minutes, capacity = row
        trainer = self._trainer_repository.get_by_id(trainer_id)
        training = Training(name, trainer, start_time, duration_minutes, capacity)
        training.id = training_id
        return training

    def list(self):
        with self._connection.cursor() as cur:
            cur.execute("SELECT id FROM trainings")
            ids = [r[0] for r in cur.fetchall()]
        return [self.get_by_id(i) for i in ids]