class Attendance:
    def __init__(self, booking, attended_at):
        if not booking.is_active():
            raise ValueError("Нельзя зарегистрировать посещение по отменённой записи")
        self.booking = booking
        self.attended_at = attended_at

    def __str__(self):
        return f"Посещение: {self.booking.client.name} на {self.booking.training.name}"