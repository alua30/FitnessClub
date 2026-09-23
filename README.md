# FitnessClub

Сервис управления клиентами фитнес-клуба: абонементы, тренировки, тренеры, записи на тренировки и посещения.

Учебный проект, выполненный в рамках практикума по ООП на Python — от объектной модели до REST API.

## Технологии

- Python
- PostgreSQL
- psycopg
- SQLAlchemy
- FastAPI
- Pydantic
- pytest

## Предметная область

Клиент приобретает абонемент и получает возможность посещать клуб и записываться на тренировки. Тренировку проводит тренер, она имеет время и ограниченную вместимость. Запись может быть создана или отменена.

**Сущности:**

- Клиент
- Абонемент
- Тренер
- Тренировка
- Запись на тренировку
- Посещение

**Основные сценарии:**

1. Регистрация клиента
2. Оформление абонемента
3. Создание тренировки
4. Запись клиента на тренировку
5. Отмена записи
6. Регистрация посещения

**Бизнес-правила:**

- клиент с недействующим абонементом не может использовать функции, требующие активного абонемента;
- количество записей не должно превышать вместимость тренировки;
- клиент не может иметь две активные записи на одну тренировку;
- отменённая запись не считается активной.

## Архитектура проекта

```text
FitnessClub/
│
├── fitness_club/                  # Основная бизнес-логика
│   ├── __init__.py
│   ├── client.py                  # Клиенты и их записи
│   ├── membership.py              # Абонементы
│   ├── trainer.py                 # Тренеры
│   ├── training.py                # Тренировки и записи
│   ├── booking.py                 # Записи на тренировки
│   └── attendance.py              # Посещения
│
├── orm/                           # Собственная ORM
│   ├── __init__.py
│   └── model.py                   # Базовая модель и CRUD-операции
│
├── repositories/                  # Работа с БД через psycopg
│   ├── __init__.py
│   ├── base.py                    # Общий Repository
│   ├── client_repository.py       # Репозиторий клиентов
│   ├── trainer_repository.py      # Репозиторий тренеров
│   └── training_repository.py     # Репозиторий тренировок
│
├── repositories_sa/               # Репозитории на SQLAlchemy
│   ├── __init__.py
│   ├── client_repository.py       # Клиенты
│   ├── trainer_repository.py      # Тренеры
│   ├── training_repository.py     # Тренировки
│   └── booking_repository.py      # Записи
│
├── db/                            # Подключение и модели БД
│   ├── __init__.py
│   ├── connection.py              # Подключение через psycopg
│   ├── schema.sql                 # Структура базы данных
│   ├── sa_base.py                 # SQLAlchemy engine и session
│   └── sa_models.py               # SQLAlchemy-модели
│
├── services/                      # Составные бизнес-операции
│   ├── __init__.py
│   ├── rebooking.py               # Перенос записи
│   └── rebooking_sa.py            # Перенос через SQLAlchemy
│
├── api/                           # REST API на FastAPI
│   ├── __init__.py
│   ├── main.py                    # FastAPI-приложение
│   ├── schemas.py                 # Pydantic-схемы
│   ├── dependencies.py            # Зависимости API
│   └── routers/                   # API-маршруты
│       ├── __init__.py
│       ├── clients.py             # Клиенты
│       ├── trainings.py           # Тренировки
│       └── bookings.py             # Записи
│
├── tests/                         # Тесты
│   ├── __init__.py
│   ├── test_business_rules.py     # Тесты бизнес-логики
│   ├── test_orm.py                # Тесты собственной ORM
│   └── test_sqlalchemy.py         # Тесты SQLAlchemy
│
├── scenarios.py                   # Бизнес-сценарии
├── main.py                        # Точка входа
├── db_demo.py                     # Примеры работы с Repository
├── orm_relations_demo.py          # Примеры работы собственной ORM
├── sa_demo.py                     # Примеры работы SQLAlchemy
│
├── README.md
└── .gitignore
```

## Запуск

Установка зависимостей:
```bash
pip install "psycopg[binary]" sqlalchemy fastapi "uvicorn[standard]" pytest
```

Создание базы данных и применение схемы:
```bash
createdb fitness_club
psql -d fitness_club -f db/schema.sql
```

Запуск in-memory сценариев:
```bash
python main.py
```

Запуск тестов:
```bash
pytest tests/ -v
```

Запуск REST API:
```bash
uvicorn api.main:app --reload
```
Документация: http://127.0.0.1:8000/docs

## Сравнение собственной ORM и SQLAlchemy

| Критерий | Собственная ORM (PR-08/09) | SQLAlchemy (PR-10) |
|---|---|---|
| Mapping | Ручной `to_row`/`from_row` в каждой модели | Декларативный класс с `Column`, автоматически |
| CRUD | Написан вручную (`save`/`get`/`delete`/`all`) | Готовые `session.add`, `session.get`, `session.delete` |
| Связи | Через ручной `filter()` по внешнему ключу | `relationship()` с `back_populates`, автоматическая подгрузка |
| Транзакции | Ручной `commit`/`rollback`, флаг `commit=False` | `Session` сама управляет unit of work |
| Ограничения | Нет ленивой загрузки, только equality-фильтры, нет кэша | Более полный функционал, но выше порог входа |

## История практик (теги Git)

| Тег | Практика |
|---|---|
| [pr-01](../../tree/pr-01) | Классы и объекты |
| [pr-02](../../tree/pr-02) | Поведение и инкапсуляция |
| [pr-03](../../tree/pr-03) | Взаимодействие объектов и композиция |
| [pr-04](../../tree/pr-04) | Абстракция, наследование и полиморфизм |
| [pr-05](../../tree/pr-05) | Завершённая объектная модель |
| [pr-06](../../tree/pr-06) | Repository и PostgreSQL |
| [pr-07](../../tree/pr-07) | Рефакторинг слоя хранения |
| [pr-08](../../tree/pr-08) | Базовая ORM-модель |
| [pr-09](../../tree/pr-09) | Развитие собственной ORM |
| [pr-10](../../tree/pr-10) | Переход на SQLAlchemy |
| [pr-11](../../tree/pr-11) | REST API на FastAPI |
