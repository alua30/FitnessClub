from fitness_club.training import Training
from repositories.trainer_repository import TrainerRepository
from repositories.base import BaseRepository


class TrainingRepository(BaseRepository):
    table_name = "trainings"

    def __init__(self, connection):
        super().__init__(connection)
        self._trainer_repository = TrainerRepository(connection)

    def save(self, training):
        if training.trainer.id is None:
            self._trainer_repository.save(training.trainer)
        return super().save(training)

    def _to_row(self, training):
        return {
            "name": training.name,
            "trainer_id": training.trainer.id,
            "start_time": training.start_time,
            "duration_minutes": training.duration_minutes,
            "capacity": training.capacity,
        }

    def _from_row(self, row):
        trainer = self._trainer_repository.get_by_id(row["trainer_id"])
        training = Training(row["name"], trainer, row["start_time"], row["duration_minutes"], row["capacity"])
        training.id = row["id"]
        return training