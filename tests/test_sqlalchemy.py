from datetime import date, datetime
import pytest

from db.sa_base import SessionLocal
from fitness_club.client import Client
from fitness_club.membership import TimeLimitedMembership
from fitness_club.trainer import Trainer
from fitness_club.training import Training
from repositories_sa.client_repository import ClientRepositorySA
from repositories_sa.training_repository import TrainingRepositorySA
from repositories_sa.booking_repository import BookingRepositorySA
from services.rebooking_sa import reschedule_booking


@pytest.fixture
def session():
    s = SessionLocal()
    yield s
    s.close()


def _make_client(session, client_repo):
    client = Client("Тест Тестов", "0", "t@example.com")
    client.membership = TimeLimitedMembership("М", date(2026, 9, 1), date(2026, 9, 30))
    client_repo.save(client)
    session.commit()
    return client


def _make_training(session, training_repo, name="Т", capacity=5):
    trainer = Trainer("Тренер Т", "Спец")
    training = Training(name, trainer, datetime(2026, 9, 16, 18, 0), 60, capacity)
    training_repo.save(training)
    session.commit()
    return training


def test_filter_by_trainer(session):
    training_repo = TrainingRepositorySA(session)
    training = _make_training(session, training_repo)

    result = training_repo.filter_by_trainer(training.trainer.id)
    assert any(t.id == training.id for t in result)


def test_many_to_many_client_training_via_booking(session):
    client_repo = ClientRepositorySA(session)
    training_repo = TrainingRepositorySA(session)
    booking_repo = BookingRepositorySA(session, client_repo, training_repo)

    client = _make_client(session, client_repo)
    training = _make_training(session, training_repo)

    booking = client.book(training, datetime.now())
    booking_repo.save(booking)
    session.commit()

    bookings = booking_repo.filter_by_client(client.id)
    assert len(bookings) == 1
    assert bookings[0].training.id == training.id


def test_transaction_rollback_on_full_training(session):
    client_repo = ClientRepositorySA(session)
    training_repo = TrainingRepositorySA(session)
    booking_repo = BookingRepositorySA(session, client_repo, training_repo)

    client = _make_client(session, client_repo)
    training = _make_training(session, training_repo, capacity=1)

    booking = client.book(training, datetime.now())
    booking_repo.save(booking)
    session.commit()

    other_client = _make_client(session, client_repo)
    full_training = _make_training(session, training_repo, capacity=1)
    other_booking = other_client.book(full_training, datetime.now())
    booking_repo.save(other_booking)
    session.commit()

    with pytest.raises(ValueError):
        reschedule_booking(booking, full_training, datetime.now(), session, booking_repo)

    restored = booking_repo.filter_by_client(client.id)[0]
    assert restored.is_active() is True