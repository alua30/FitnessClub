from orm.model import Model


class Trainer(Model):
    table_name = "trainers"
    fields = ["name", "specialization"]

    def __init__(self, name, specialization):
        super().__init__()
        self.name = name
        self.specialization = specialization

    def to_row(self):
        return {"name": self.name, "specialization": self.specialization}

    @classmethod
    def from_row(cls, row):
        obj = cls(row["name"], row["specialization"])
        obj.id = row["id"]
        return obj

    def __str__(self):
        return f"Тренер: {self.name} ({self.specialization})"