from abc import ABC, abstractmethod


class Repository(ABC):
    @abstractmethod
    def save(self, obj):
        """Сохраняет объект (INSERT или UPDATE), возвращает его id."""
        ...

    @abstractmethod
    def get_by_id(self, obj_id):
        """Возвращает объект предметной модели по id, либо None."""
        ...

    @abstractmethod
    def list(self):
        """Возвращает список всех объектов."""
        ...