from datetime import date, datetime
from pydantic import BaseModel


class ClientCreate(BaseModel):
    name: str
    phone: str
    email: str


class ClientOut(BaseModel):
    id: int
    name: str
    phone: str
    email: str

    class Config:
        from_attributes = True


class MembershipCreate(BaseModel):
    type: str  # "time_limited" | "visit_limited"
    name: str
    start_date: date | None = None
    end_date: date | None = None
    visits_left: int | None = None


class TrainerCreate(BaseModel):
    name: str
    specialization: str


class TrainingCreate(BaseModel):
    name: str
    trainer_id: int
    start_time: datetime
    duration_minutes: int
    capacity: int


class TrainingOut(BaseModel):
    id: int
    name: str
    start_time: datetime
    duration_minutes: int
    capacity: int


class BookingCreate(BaseModel):
    client_id: int
    training_id: int


class BookingOut(BaseModel):
    id: int
    status: str