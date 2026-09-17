from datetime import date, datetime

from db.connection import get_connection
from fitness_club.client import Client
from fitness_club.membership import TimeLimitedMembership
from fitness_club.trainer import Trainer
from fitness_club.training import Training
from fitness_club.booking import Booking
from repositories.client_repository import ClientRepository
from services.rebooking import reschedule_booking


def demo():
    connection = get_connection()
    client_repo = ClientRepository(connection)

    client = Client("Алия Садыкова", "+7 700 111 22 33", "aliya@example.com")
    client.membership = TimeLimitedMembership("Месячный", date(2026, 9, 1), date(2026, 9, 30))
    client_repo.save(client)

    trainer = Trainer("Алексей Иванов", "Фитнес")
    trainer.save(connection)

    training_1 = Training("Силовая", trainer, datetime(2026, 9, 16, 18, 0), 60, capacity=5)
    training_1.save(connection)
    training_2 = Training("Кроссфит", trainer, datetime(2026, 9, 17, 18, 0), 60, capacity=5)
    training_2.save(connection)

    # 1:N — все тренировки конкретного тренера
    trainings_of_trainer = Training.filter(connection, trainer_id=trainer.id)
    print("Тренировки тренера:", [t.name for t in trainings_of_trainer])

    # M:N — клиент записывается, затем видно связь и с той, и с другой стороны
    booking = client.book(training_1, datetime.now(), connection)
    print("Записи клиента:", [b.training.name for b in Booking.filter(connection, client_id=client.id)])
    print("Клиенты тренировки:", [b.client.name for b in Booking.filter(connection, training_id=training_1.id)])

    # Транзакция — перенос записи с одной тренировки на другую
    new_booking = reschedule_booking(booking, training_2, datetime.now(), connection)
    print("После переноса:", new_booking, "| старая активна:", booking.is_active())

    connection.close()


if __name__ == "__main__":
    demo()