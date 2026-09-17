from datetime import date, datetime
import pytest

from db.connection import get_connection
from fitness_club.client import Client
from fitness_club.membership import TimeLimitedMembership
from fitness_club.trainer import Trainer
from fitness_club.training import Training
from fitness_club.booking import Booking
from repositories.client_repository import ClientRepository
from services.rebooking import reschedule_booking


@pytest.fixture
def connection():
    conn = get_connection()
    yield conn
    conn.close()


def _make_client(connection):
    client = Client("Тест Тестов", "0", "t@example.com")
    client.membership = TimeLimitedMembership("М", date(2026, 9, 1), date(2026, 9, 30))
    ClientRepository(connection).save(client)
    return client


def _make_training(connection, name="Т", capacity=5):
    trainer = Trainer("Тренер Т", "Спец")
    trainer.save(connection)
    training = Training(name, trainer, datetime(2026, 9, 16, 18, 0), 60, capacity)
    training.save(connection)
    return training


def test_filter_by_single_field(connection):
    training = _make_training(connection)
    result = Training.filter(connection, name=training.name)
    assert any(t.id == training.id for t in result)


def test_one_to_many_trainer_trainings(connection):
    trainer = Trainer("Уникальный Тренер", "Йога")
    trainer.save(connection)
    t1 = Training("A", trainer, datetime(2026, 9, 16, 18, 0), 60, 5)
    t1.save(connection)
    t2 = Training("B", trainer, datetime(2026, 9, 17, 18, 0), 60, 5)
    t2.save(connection)

    trainings = Training.filter(connection, trainer_id=trainer.id)
    assert len(trainings) == 2


def test_many_to_many_client_training_via_booking(connection):
    client = _make_client(connection)
    training = _make_training(connection)

    client.book(training, datetime.now(), connection)

    bookings = Booking.filter(connection, client_id=client.id)
    assert len(bookings) == 1
    assert bookings[0].training.id == training.id


def test_transaction_rollback_on_full_training(connection):
    client = _make_client(connection)
    training = _make_training(connection, capacity=1)
    other_client = _make_client(connection)

    booking = client.book(training, datetime.now(), connection)
    other_training = _make_training(connection, capacity=1)
    other_client.book(other_training, datetime.now(), connection)  # занято другое место

    full_training = _make_training(connection, capacity=1)
    other_client.book(full_training, datetime.now(), connection)  # заполнили capacity=1

    with pytest.raises(ValueError):
        reschedule_booking(booking, full_training, datetime.now(), connection)

    # старая запись должна остаться активной — транзакция откатилась
    restored = Booking.get(booking.id, connection)
    assert restored.is_active() is True