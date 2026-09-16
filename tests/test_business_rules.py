from datetime import date, datetime
import pytest

from fitness_club.client import Client
from fitness_club.membership import TimeLimitedMembership, VisitLimitedMembership
from fitness_club.trainer import Trainer
from fitness_club.training import Training
from fitness_club.attendance import Attendance


@pytest.fixture
def trainer():
    return Trainer("Алексей Иванов", "Фитнес")


@pytest.fixture
def client_with_active_membership():
    client = Client("Алия Садыкова", "+7 700 111 22 33", "aliya@example.com")
    client.membership = TimeLimitedMembership("Месячный абонемент", date(2026, 9, 1), date(2026, 9, 30))
    return client


def test_client_without_membership_cannot_book(trainer):
    client = Client("Данияр Ахметов", "+7 701 444 55 66", "daniyar@example.com")
    training = Training("Йога", trainer, datetime(2026, 9, 17, 19, 0), 60, capacity=5)

    with pytest.raises(ValueError):
        client.book(training, datetime(2026, 9, 17, 9, 0))


def test_expired_membership_is_not_active():
    membership = TimeLimitedMembership("Истёкший", date(2025, 1, 1), date(2025, 12, 31))
    assert membership.is_active(date(2026, 9, 16)) is False


def test_booking_cannot_exceed_training_capacity(trainer):
    training = Training("Силовая", trainer, datetime(2026, 9, 16, 18, 0), 60, capacity=1)

    client_1 = Client("Клиент 1", "1", "1@example.com")
    client_1.membership = TimeLimitedMembership("М1", date(2026, 9, 1), date(2026, 9, 30))
    client_2 = Client("Клиент 2", "2", "2@example.com")
    client_2.membership = TimeLimitedMembership("М2", date(2026, 9, 1), date(2026, 9, 30))

    client_1.book(training, datetime(2026, 9, 16, 10, 0))

    with pytest.raises(ValueError):
        client_2.book(training, datetime(2026, 9, 16, 10, 5))


def test_client_cannot_have_two_active_bookings_for_same_training(trainer, client_with_active_membership):
    training = Training("Силовая", trainer, datetime(2026, 9, 16, 18, 0), 60, capacity=5)
    client_with_active_membership.book(training, datetime(2026, 9, 16, 10, 0))

    with pytest.raises(ValueError):
        client_with_active_membership.book(training, datetime(2026, 9, 16, 10, 5))


def test_cancelled_booking_is_not_active(trainer, client_with_active_membership):
    training = Training("Силовая", trainer, datetime(2026, 9, 16, 18, 0), 60, capacity=5)
    booking = client_with_active_membership.book(training, datetime(2026, 9, 16, 10, 0))

    client_with_active_membership.cancel_booking(booking)

    assert booking.is_active() is False


def test_cancelling_booking_frees_slot(trainer):
    training = Training("Йога", trainer, datetime(2026, 9, 17, 19, 0), 60, capacity=1)

    client_1 = Client("Клиент 1", "1", "1@example.com")
    client_1.membership = TimeLimitedMembership("М1", date(2026, 9, 1), date(2026, 9, 30))
    client_2 = Client("Клиент 2", "2", "2@example.com")
    client_2.membership = TimeLimitedMembership("М2", date(2026, 9, 1), date(2026, 9, 30))

    booking_1 = client_1.book(training, datetime(2026, 9, 17, 9, 0))
    client_1.cancel_booking(booking_1)

    booking_2 = client_2.book(training, datetime(2026, 9, 17, 9, 30))  # не должно упасть
    assert booking_2.is_active() is True


def test_attendance_cannot_be_registered_for_cancelled_booking(trainer, client_with_active_membership):
    training = Training("Силовая", trainer, datetime(2026, 9, 16, 18, 0), 60, capacity=5)
    booking = client_with_active_membership.book(training, datetime(2026, 9, 16, 10, 0))
    client_with_active_membership.cancel_booking(booking)

    with pytest.raises(ValueError):
        Attendance(booking, datetime(2026, 9, 16, 19, 0))


def test_visit_limited_membership_decreases_on_usage():
    membership = VisitLimitedMembership("2 посещения", visits_left=2)
    membership.register_usage()
    assert membership.visits_left == 1


def test_visit_limited_membership_raises_when_exhausted():
    membership = VisitLimitedMembership("Пусто", visits_left=0)
    assert membership.is_active() is False
    with pytest.raises(ValueError):
        membership.register_usage()