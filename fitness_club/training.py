from fitness_club.attendance import Attendance


class Training:
    def __init__(self, name, trainer, start_time, duration_minutes, capacity):
        self.name = name
        self.trainer = trainer
        self.start_time = start_time
        self.duration_minutes = duration_minutes
        self.capacity = capacity
        self._bookings = []

    @property
    def bookings(self):
        return list(self._bookings)

    def active_bookings_count(self):
        return len([b for b in self._bookings if b.is_active()])

    def has_free_slots(self):
        return self.active_bookings_count() < self.capacity

    def has_active_booking_for(self, client):
        return any(b.client is client and b.is_active() for b in self._bookings)

    def add_booking(self, booking):
        if not self.has_free_slots():
            raise ValueError("Нет свободных мест на тренировку")
        if self.has_active_booking_for(booking.client):
            raise ValueError("У клиента уже есть активная запись на эту тренировку")
        self._bookings.append(booking)

    def register_attendance(self, booking, at):
        if booking.training is not self:
            raise ValueError("Эта запись относится к другой тренировке")
        return Attendance(booking, at)

    def __str__(self):
        return f"Тренировка: {self.name} ({self.trainer.name}, {self.start_time})"