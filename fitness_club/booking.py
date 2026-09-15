class Booking:
    def __init__(self, client, training, created_at):
        self.client = client
        self.training = training
        self.created_at = created_at
        self._status = "active"

    @property
    def status(self):
        return self._status

    def is_active(self):
        return self._status == "active"

    def cancel(self):
        self._status = "cancelled"

    def __str__(self):
        return f"Запись: {self.client.name} → {self.training.name} [{self._status}]"