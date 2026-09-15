from datetime import date, datetime

from fitness_club.client import Client
from fitness_club.membership import Membership
from fitness_club.trainer import Trainer
from fitness_club.training import Training
from fitness_club.booking import Booking
from fitness_club.attendance import Attendance


# Регистрация клиентов
client_1 = Client("Алия Садыкова", "+7 700 111 22 33", "aliya@example.com")
client_2 = Client("Данияр Ахметов", "+7 701 444 55 66", "daniyar@example.com")

# Оформление абонементов
membership_1 = Membership("Месячный абонемент", date(2026, 9, 1), date(2026, 9, 30))
membership_2 = Membership("Годовой абонемент", date(2025, 1, 1), date(2025, 12, 31))  # уже истёк

client_1.membership = membership_1
client_2.membership = membership_2

print(client_1.has_active_membership())  # True
print(client_2.has_active_membership())  # False — абонемент истёк

# Тренеры и тренировка с маленькой вместимостью для демонстрации правила
trainer_1 = Trainer("Алексей Иванов", "Фитнес")
training_1 = Training("Силовая тренировка", trainer_1, datetime(2026, 9, 16, 18, 0), 60, capacity=1)

# Запись клиента 1 — успешно
booking_1 = Booking(client_1, training_1, datetime.now())
training_1.add_booking(booking_1)
print(training_1.has_free_slots())  # False — мест больше нет

# Попытка записать клиента 2 — превышение вместимости
booking_2 = Booking(client_2, training_1, datetime.now())
try:
    training_1.add_booking(booking_2)
except ValueError as e:
    print("Ошибка:", e)

# Отмена записи клиента 1 — место освобождается
booking_1.cancel()
print(training_1.has_free_slots())  # True

# Теперь клиент 2 может записаться
training_1.add_booking(booking_2)
print(training_1.active_bookings_count())  # 1

# Посещение по активной записи — ок
attendance = Attendance(booking_2, datetime(2026, 9, 16, 19, 0))
print(attendance)

# Посещение по отменённой записи — ошибка
try:
    Attendance(booking_1, datetime(2026, 9, 16, 19, 0))
except ValueError as e:
    print("Ошибка:", e)