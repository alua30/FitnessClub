from datetime import date, datetime

from fitness_club.client import Client
from fitness_club.membership import TimeLimitedMembership, VisitLimitedMembership
from fitness_club.trainer import Trainer
from fitness_club.training import Training


client_1 = Client("Алия Садыкова", "+7 700 111 22 33", "aliya@example.com")
client_2 = Client("Данияр Ахметов", "+7 701 444 55 66", "daniyar@example.com")

# Два РАЗНЫХ типа абонемента — клиентский код не знает, какой именно
client_1.membership = TimeLimitedMembership("Месячный абонемент", date(2026, 9, 1), date(2026, 9, 30))
client_2.membership = VisitLimitedMembership("Абонемент на 2 посещения", visits_left=2)

trainer_1 = Trainer("Алексей Иванов", "Фитнес")
training_1 = Training("Силовая тренировка", trainer_1, datetime(2026, 9, 16, 18, 0), 60, capacity=5)

# Полиморфный вызов is_active — одинаковый код для обоих типов
for client in (client_1, client_2):
    print(client.name, "- активен:", client.has_active_membership())

booking_1 = client_1.book(training_1, datetime.now())
booking_2 = client_2.book(training_1, datetime.now())

# Полиморфный вызов register_usage при посещении — без проверки типа абонемента
training_1.register_attendance(booking_1, datetime(2026, 9, 16, 19, 0))
training_1.register_attendance(booking_2, datetime(2026, 9, 16, 19, 0))

print(client_2.membership)  # осталось 1 посещение

training_1.register_attendance(booking_2, datetime(2026, 9, 16, 19, 5))
print(client_2.membership)  # осталось 0 посещений — abonement исчерпан

print(client_2.has_active_membership())  # False — тот же полиморфный is_active()