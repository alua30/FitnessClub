from fitness_club.trainer import Trainer
from db.sa_models import TrainerORM


class TrainerRepositorySA:
    def __init__(self, session):
        self._session = session

    def _to_domain(self, orm_obj):
        trainer = Trainer(orm_obj.name, orm_obj.specialization)
        trainer.id = orm_obj.id
        return trainer

    def save(self, trainer):
        if trainer.id is None:
            orm_obj = TrainerORM(name=trainer.name, specialization=trainer.specialization)
            self._session.add(orm_obj)
            self._session.flush()  # чтобы получить id до commit
            trainer.id = orm_obj.id
        else:
            orm_obj = self._session.get(TrainerORM, trainer.id)
            orm_obj.name = trainer.name
            orm_obj.specialization = trainer.specialization
        return trainer.id

    def get_by_id(self, trainer_id):
        orm_obj = self._session.get(TrainerORM, trainer_id)
        return self._to_domain(orm_obj) if orm_obj else None