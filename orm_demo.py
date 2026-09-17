from datetime import datetime

from fitness_club.trainer import Trainer
from fitness_club.training import Training


def demo():
    # save() на первой модели
    trainer = Trainer("Мария Петрова", "Йога")
    trainer.save()
    print("Тренер создан:", Trainer.get(trainer.id))

    # save() на второй модели — единый API, разное поведение внутри
    training = Training("Йога", trainer, datetime(2026, 9, 20, 10, 0), 60, capacity=8)
    training.save()
    print("Тренировка создана:", Training.get(training.id))

    # all()
    print("Все тренеры:", [str(t) for t in Trainer.all()])

    # update через save() — id уже есть
    trainer.specialization = "Йога и стретчинг"
    trainer.save()
    print("После обновления:", Trainer.get(trainer.id))

    # delete()
    training.delete()
    print("После удаления тренировки:", Training.get(training.id))  # None


if __name__ == "__main__":
    demo()