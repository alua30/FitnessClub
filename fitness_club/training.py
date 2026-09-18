from orm.model import Model
from fitness_club.trainer import Trainer


class Training(Model):
    table_name = "trainings"
    fields = ["name", "trainer_id", "start_time", "duration_minutes", "capacity"]

    def __init__(self, name, trainer, start_time, duration_minutes, capacity):
        super().__init__()
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
        from fitness_club.attendance import Attendance
        attendance = Attendance(booking, at)
        booking.client.membership.register_usage()
        return attendance

    def save(self, connection=None, commit=True):
        if self.trainer.id is None:
            self.trainer.save(connection, commit)
        return super().save(connection, commit)

    def to_row(self):
        return {
            "name": self.name,
            "trainer_id": self.trainer.id,
            "start_time": self.start_time,
            "duration_minutes": self.duration_minutes,
            "capacity": self.capacity,
        }

    @classmethod
    def from_row(cls, row):
        trainer = Trainer.get(row["trainer_id"])
        obj = cls(row["name"], trainer, row["start_time"], row["duration_minutes"], row["capacity"])
        obj.id = row["id"]
        return obj

    def __str__(self):
        return f"Тренировка: {self.name} ({self.trainer.name}, {self.start_time})"