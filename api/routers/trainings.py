from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.dependencies import get_session
from api.schemas import TrainingCreate, TrainingOut, TrainerCreate
from repositories_sa.training_repository import TrainingRepositorySA
from repositories_sa.trainer_repository import TrainerRepositorySA
from fitness_club.training import Training
from fitness_club.trainer import Trainer

router = APIRouter(prefix="/trainings", tags=["trainings"])


@router.post("/trainers", response_model=dict, status_code=201)
def create_trainer(payload: TrainerCreate, session: Session = Depends(get_session)):
    trainer = Trainer(payload.name, payload.specialization)
    TrainerRepositorySA(session).save(trainer)
    session.commit()
    return {"id": trainer.id, "name": trainer.name}


@router.post("", response_model=TrainingOut, status_code=201)
def create_training(payload: TrainingCreate, session: Session = Depends(get_session)):
    trainer = TrainerRepositorySA(session).get_by_id(payload.trainer_id)
    if trainer is None:
        raise HTTPException(status_code=404, detail="Тренер не найден")

    training = Training(payload.name, trainer, payload.start_time, payload.duration_minutes, payload.capacity)
    TrainingRepositorySA(session).save(training)
    session.commit()
    return training


@router.get("/{training_id}", response_model=TrainingOut)
def get_training(training_id: int, session: Session = Depends(get_session)):
    training = TrainingRepositorySA(session).get_by_id(training_id)
    if training is None:
        raise HTTPException(status_code=404, detail="Тренировка не найдена")
    return training


@router.get("", response_model=list[TrainingOut])
def list_by_trainer(trainer_id: int, session: Session = Depends(get_session)):
    return TrainingRepositorySA(session).filter_by_trainer(trainer_id)