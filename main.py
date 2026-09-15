from datetime import date, datetime

from fitness_club.client import Client
from fitness_club.membership import Membership
from fitness_club.trainer import Trainer
from fitness_club.training import Training
from fitness_club.booking import Booking
from fitness_club.attendance import Attendance


# 1. Регистрация клиентов
client_1 = Client("Алия Садыкова", "+7 700 111 22 33", "aliya@example.com")
client_2 = Client("Данияр Ахметов", "+7 701 444 55 66", "daniyar@example.com")

# 2. Оформление абонементов
membership_1 = Membership("Месячный абонемент", date(2026, 9, 1), date(2026, 9, 30))
membership_2 = Membership("Годовой абонемент", date(2026, 9, 1), date(2027, 8, 31))

client_1.membership = membership_1
client_2.membership = membership_2

# Тренеры
trainer_1 = Trainer("Алексей Иванов", "Фитнес")
trainer_2 = Trainer("Мария Петрова", "Йога")

# 3. Создание тренировок
training_1 = Training("Силовая тренировка", trainer_1, datetime(2026, 9, 16, 18, 0), 60, 10)
training_2 = Training("Йога", trainer_2, datetime(2026, 9, 17, 19, 0), 60, 15)

# 4. Запись клиентов на тренировки
booking_1 = Booking(client_1, training_1, datetime.now())
booking_2 = Booking(client_2, training_2, datetime.now())

training_1.bookings.append(booking_1)
training_2.bookings.append(booking_2)

# 6. Регистрация посещений
attendance_1 = Attendance(booking_1, datetime(2026, 9, 16, 19, 0))
attendance_2 = Attendance(booking_2, datetime(2026, 9, 17, 20, 0))

# Демонстрация
print(client_1)
print(client_2)
print(membership_1)
print(membership_2)
print(trainer_1)
print(trainer_2)
print(training_1)
print(training_2)
print(booking_1)
print(booking_2)
print(attendance_1)
print(attendance_2)