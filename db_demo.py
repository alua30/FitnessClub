from datetime import date, datetime

from db.connection import get_connection
from fitness_club.trainer import Trainer
from fitness_club.training import Training
from fitness_club.client import Client
from fitness_club.membership import TimeLimitedMembership, VisitLimitedMembership
from repositories.client_repository import ClientRepository


def write_data():
    connection = get_connection()
    client_repo = ClientRepository(connection)

    client_1 = Client("Алия Садыкова", "+7 700 111 22 33", "aliya@example.com")
    client_1.membership = TimeLimitedMembership("Месячный абонемент", date(2026, 9, 1), date(2026, 9, 30))
    client_repo.save(client_1)

    client_2 = Client("Данияр Ахметов", "+7 701 444 55 66", "daniyar@example.com")
    client_2.membership = VisitLimitedMembership("Абонемент на 2 посещения", visits_left=2)
    client_repo.save(client_2)

    trainer = Trainer("Алексей Иванов", "Фитнес")
    training = Training("Силовая тренировка", trainer, datetime(2026, 9, 16, 18, 0), 60, capacity=10)
    training.save(connection)  # теперь ORM-метод самой модели, а не репозиторий

    connection.close()
    return client_1.id, client_2.id, training.id


def read_data(client_id_1, client_id_2, training_id):
    connection = get_connection()  # новое соединение — как будто программа перезапущена
    client_repo = ClientRepository(connection)

    restored_client_1 = client_repo.get_by_id(client_id_1)
    restored_client_2 = client_repo.get_by_id(client_id_2)
    restored_training = Training.get(training_id, connection)  # тоже ORM-метод

    print(restored_client_1, "-", restored_client_1.membership)
    print(restored_client_2, "-", restored_client_2.membership)
    print(restored_training, "-", restored_training.trainer)

    connection.close()


if __name__ == "__main__":
    ids = write_data()
    read_data(*ids)