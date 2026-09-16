from abc import ABC, abstractmethod
from datetime import date


class Membership(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def is_active(self, on_date=None):
        """Действует ли абонемент на указанную дату."""
        ...

    @abstractmethod
    def register_usage(self):
        """Учитывает факт использования абонемента (например, посещение)."""
        ...

    def __str__(self):
        return f"Абонемент: {self.name}"


class TimeLimitedMembership(Membership):
    """Абонемент, ограниченный периодом действия (месяц, год и т.д.)."""

    def __init__(self, name, start_date, end_date):
        super().__init__(name)
        self.start_date = start_date
        self.end_date = end_date

    def is_active(self, on_date=None):
        if on_date is None:
            on_date = date.today()
        return self.start_date <= on_date <= self.end_date

    def register_usage(self):
        pass  # посещения не ограничены количеством, время не расходуется

    def __str__(self):
        return f"{super().__str__()} ({self.start_date} — {self.end_date})"


class VisitLimitedMembership(Membership):
    """Абонемент на фиксированное количество посещений."""

    def __init__(self, name, visits_left):
        super().__init__(name)
        self.visits_left = visits_left

    def is_active(self, on_date=None):
        return self.visits_left > 0

    def register_usage(self):
        if self.visits_left <= 0:
            raise ValueError("Посещения по абонементу закончились")
        self.visits_left -= 1

    def __str__(self):
        return f"{super().__str__()} (осталось посещений: {self.visits_left})"