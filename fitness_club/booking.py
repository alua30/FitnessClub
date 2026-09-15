class Booking:
    def __init__(self, client, training, created_at):
        self.client = client
        self.training = training
        self.created_at = created_at
        self.status = "active"  # active / cancelled

    def __str__(self):
        return f"Запись: {self.client.name} → {self.training.name} [{self.status}]"