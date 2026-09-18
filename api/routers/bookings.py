from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from sqlalchemy.orm import Session

from api.dependencies import get_session
from api.schemas import BookingCreate, BookingOut
from repositories_sa.client_repository import ClientRepositorySA
from repositories_sa.training_repository import TrainingRepositorySA
from repositories_sa.booking_repository import BookingRepositorySA

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.post("", response_model=BookingOut, status_code=201)
def create_booking(payload: BookingCreate, session: Session = Depends(get_session)):
    client_repo = ClientRepositorySA(session)
    training_repo = TrainingRepositorySA(session)
    booking_repo = BookingRepositorySA(session, client_repo, training_repo)

    client = client_repo.get_by_id(payload.client_id)
    training = training_repo.get_by_id(payload.training_id)
    if client is None or training is None:
        raise HTTPException(status_code=404, detail="Клиент или тренировка не найдены")

    existing_bookings = booking_repo.filter_by_training(training.id)
    for b in existing_bookings:
        training._bookings.append(b)

    try:
        booking = client.book(training, datetime.now())
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

    booking_repo.save(booking)
    session.commit()
    return booking


@router.post("/{booking_id}/cancel", response_model=BookingOut)
def cancel_booking(booking_id: int, session: Session = Depends(get_session)):
    client_repo = ClientRepositorySA(session)
    training_repo = TrainingRepositorySA(session)
    booking_repo = BookingRepositorySA(session, client_repo, training_repo)

    booking = booking_repo.get_by_id(booking_id)
    if booking is None:
        raise HTTPException(status_code=404, detail="Запись не найдена")

    if not booking.is_active():
        raise HTTPException(status_code=409, detail="Запись уже отменена")

    booking._status = "cancelled"
    booking_repo.save(booking)
    session.commit()
    return booking