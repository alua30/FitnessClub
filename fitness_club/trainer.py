class Trainer:
    def __init__(self, name, specialization):
        self.name = name
        self.specialization = specialization

    def __str__(self):
        return f"Тренер: {self.name} ({self.specialization})"