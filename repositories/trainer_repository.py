from fitness_club.trainer import Trainer
from repositories.base import BaseRepository


class TrainerRepository(BaseRepository):
    table_name = "trainers"

    def _to_row(self, trainer):
        return {"name": trainer.name, "specialization": trainer.specialization}

    def _from_row(self, row):
        trainer = Trainer(row["name"], row["specialization"])
        trainer.id = row["id"]
        return trainer