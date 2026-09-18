from datetime import date, datetime

from db.sa_base import SessionLocal
from fitness_club.client import Client
from fitness_club.membership import TimeLimitedMembership
from fitness_club.trainer import Trainer
from fitness_club.training import Training
from repositories_sa.client_repository import ClientRepositorySA
from repositories_sa.training_repository import TrainingRepositorySA
from repositories_sa.booking_repository import BookingRepositorySA
from services.rebooking_sa import reschedule_booking


def demo():
    session = SessionLocal()
    client_repo = ClientRepositorySA(session)
    training_repo = TrainingRepositorySA(session)
    booking_repo = BookingRepositorySA(session, client_repo, training_repo)

    client = Client("Алия Садыкова", "+7 700 111 22 33", "aliya@example.com")
    client.membership = TimeLimitedMembership("Месячный", date(2026, 9, 1), date(2026, 9, 30))
    client_repo.save(client)

    trainer = Trainer("Алексей Иванов", "Фитнес")
    training_1 = Training("Силовая", trainer, datetime(2026, 9, 16, 18, 0), 60, capacity=5)
    training_repo.save(training_1)
    training_2 = Training("Кроссфит", trainer, datetime(2026, 9, 17, 18, 0), 60, capacity=5)
    training_repo.save(training_2)
    session.commit()

    print("Тренировки тренера:", [t.name for t in training_repo.filter_by_trainer(trainer.id)])

    booking = client.book(training_1, datetime.now())
    booking_repo.save(booking)
    session.commit()

    print("Записи клиента:", [b.training.name for b in booking_repo.filter_by_client(client.id)])
    print("Клиенты тренировки:", [b.client.name for b in booking_repo.filter_by_training(training_1.id)])

    new_booking = reschedule_booking(booking, training_2, datetime.now(), session, booking_repo)
    print("После переноса: старая активна:", booking.is_active(), "| новая:", new_booking)

    session.close()


if __name__ == "__main__":
    demo()