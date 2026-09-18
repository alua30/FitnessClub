from fitness_club.training import Training
from db.sa_models import TrainingORM
from repositories_sa.trainer_repository import TrainerRepositorySA


class TrainingRepositorySA:
    def __init__(self, session):
        self._session = session
        self._trainer_repo = TrainerRepositorySA(session)

    def _to_domain(self, orm_obj):
        trainer = self._trainer_repo.get_by_id(orm_obj.trainer_id)
        training = Training(orm_obj.name, trainer, orm_obj.start_time, orm_obj.duration_minutes, orm_obj.capacity)
        training.id = orm_obj.id
        return training

    def save(self, training):
        if training.trainer.id is None:
            self._trainer_repo.save(training.trainer)

        if training.id is None:
            orm_obj = TrainingORM(
                name=training.name, trainer_id=training.trainer.id, start_time=training.start_time,
                duration_minutes=training.duration_minutes, capacity=training.capacity,
            )
            self._session.add(orm_obj)
            self._session.flush()
            training.id = orm_obj.id
        else:
            orm_obj = self._session.get(TrainingORM, training.id)
            orm_obj.name = training.name
            orm_obj.capacity = training.capacity
        return training.id

    def get_by_id(self, training_id):
        orm_obj = self._session.get(TrainingORM, training_id)
        return self._to_domain(orm_obj) if orm_obj else None

    def filter_by_trainer(self, trainer_id):
        orm_objs = self._session.query(TrainingORM).filter_by(trainer_id=trainer_id).all()
        return [self._to_domain(o) for o in orm_objs]