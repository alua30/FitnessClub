class Training:
    def __init__(self, name, trainer, start_time, duration_minutes, capacity):
        self.name = name
        self.trainer = trainer
        self.start_time = start_time
        self.duration_minutes = duration_minutes
        self.capacity = capacity
        self.bookings = []  # список записей на эту тренировку

    def __str__(self):
        return f"Тренировка: {self.name} ({self.trainer.name}, {self.start_time})"