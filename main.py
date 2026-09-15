from datetime import date, datetime

from fitness_club.client import Client
from fitness_club.membership import Membership
from fitness_club.trainer import Trainer
from fitness_club.training import Training


# 1. Регистрация клиента
client_1 = Client("Алия Садыкова", "+7 700 111 22 33", "aliya@example.com")
client_2 = Client("Данияр Ахметов", "+7 701 444 55 66", "daniyar@example.com")

# 2. Оформление абонемента
client_1.membership = Membership("Месячный абонемент", date(2026, 9, 1), date(2026, 9, 30))
client_2.membership = Membership("Годовой абонемент", date(2025, 1, 1), date(2025, 12, 31))  # истёк

# 3. Создание тренировки
trainer_1 = Trainer("Алексей Иванов", "Фитнес")
training_1 = Training("Силовая тренировка", trainer_1, datetime(2026, 9, 16, 18, 0), 60, capacity=1)

# 4. Запись клиента на тренировку
booking_1 = client_1.book(training_1, datetime.now())
print(booking_1)

# Попытка записи клиента с истёкшим абонементом
try:
    client_2.book(training_1, datetime.now())
except ValueError as e:
    print("Ошибка:", e)

# 5. Отмена записи
client_1.cancel_booking(booking_1)
print(booking_1)

# Теперь клиент 2 не может записаться всё равно (абонемент истёк), но место свободно
try:
    client_2.book(training_1, datetime.now())
except ValueError as e:
    print("Ошибка:", e)

# Продлим клиенту 2 абонемент и повторим
client_2.membership = Membership("Месячный абонемент", date(2026, 9, 1), date(2026, 9, 30))
booking_2 = client_2.book(training_1, datetime.now())
print(booking_2)

# 6. Регистрация посещения
attendance = training_1.register_attendance(booking_2, datetime(2026, 9, 16, 19, 0))
print(attendance)