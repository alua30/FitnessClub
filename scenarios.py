from datetime import date, datetime

from fitness_club.client import Client
from fitness_club.membership import TimeLimitedMembership, VisitLimitedMembership
from fitness_club.trainer import Trainer
from fitness_club.training import Training


def scenario_successful_booking():
    """Клиент с действующим абонементом успешно записывается на тренировку."""
    client = Client("Алия Садыкова", "+7 700 111 22 33", "aliya@example.com")
    client.membership = TimeLimitedMembership("Месячный абонемент", date(2026, 9, 1), date(2026, 9, 30))

    trainer = Trainer("Алексей Иванов", "Фитнес")
    training = Training("Силовая тренировка", trainer, datetime(2026, 9, 16, 18, 0), 60, capacity=5)

    booking = client.book(training, datetime(2026, 9, 16, 10, 0))
    return client, training, booking


def scenario_cancel_frees_slot():
    """Клиент отменяет запись, место освобождается, второй клиент записывается."""
    client_1 = Client("Алия Садыкова", "+7 700 111 22 33", "aliya@example.com")
    client_2 = Client("Данияр Ахметов", "+7 701 444 55 66", "daniyar@example.com")
    client_1.membership = TimeLimitedMembership("Месячный абонемент", date(2026, 9, 1), date(2026, 9, 30))
    client_2.membership = TimeLimitedMembership("Месячный абонемент", date(2026, 9, 1), date(2026, 9, 30))

    trainer = Trainer("Мария Петрова", "Йога")
    training = Training("Йога", trainer, datetime(2026, 9, 17, 19, 0), 60, capacity=1)

    booking_1 = client_1.book(training, datetime(2026, 9, 17, 9, 0))
    client_1.cancel_booking(booking_1)
    booking_2 = client_2.book(training, datetime(2026, 9, 17, 9, 30))

    return training, booking_1, booking_2


def scenario_attendance_consumes_visit_membership():
    """Клиент с абонементом на посещения посещает тренировку, счётчик уменьшается."""
    client = Client("Данияр Ахметов", "+7 701 444 55 66", "daniyar@example.com")
    client.membership = VisitLimitedMembership("Абонемент на 2 посещения", visits_left=2)

    trainer = Trainer("Алексей Иванов", "Фитнес")
    training = Training("Силовая тренировка", trainer, datetime(2026, 9, 16, 18, 0), 60, capacity=5)

    booking = client.book(training, datetime(2026, 9, 16, 10, 0))
    attendance = training.register_attendance(booking, datetime(2026, 9, 16, 19, 0))

    return client, attendance