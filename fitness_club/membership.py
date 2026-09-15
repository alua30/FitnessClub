from datetime import date


class Membership:
    def __init__(self, name, start_date, end_date):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date

    def is_active(self, on_date=None):
        if on_date is None:
            on_date = date.today()
        return self.start_date <= on_date <= self.end_date

    def __str__(self):
        return f"Абонемент: {self.name} ({self.start_date} — {self.end_date})"