from fitness_club.booking import Booking


class Client:
    def __init__(self, name, phone, email):
        self.id = None
        self.name = name
        self.phone = phone
        self.email = email
        self.membership = None

    def has_active_membership(self, on_date=None):
        return self.membership is not None and self.membership.is_active(on_date)

    def book(self, training, at):
        if not self.has_active_membership(at.date()):
            raise ValueError("Нельзя записаться без действующего абонемента")

        booking = Booking(self, training, at)
        training.add_booking(booking)
        return booking

    def cancel_booking(self, booking):
        if booking.client is not self:
            raise ValueError("Нельзя отменить чужую запись")
        booking.cancel()

    def __str__(self):
        return f"Клиент: {self.name}"