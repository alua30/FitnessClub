from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from db.sa_base import Base


class TrainerORM(Base):
    __tablename__ = "trainers"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    specialization = Column(String, nullable=False)

    trainings = relationship("TrainingORM", back_populates="trainer")


class MembershipORM(Base):
    __tablename__ = "memberships"

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    name = Column(String, nullable=False)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    visits_left = Column(Integer, nullable=True)


class ClientORM(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    membership_id = Column(Integer, ForeignKey("memberships.id"), nullable=True)

    membership = relationship("MembershipORM")
    bookings = relationship("BookingORM", back_populates="client")


class TrainingORM(Base):
    __tablename__ = "trainings"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    trainer_id = Column(Integer, ForeignKey("trainers.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    capacity = Column(Integer, nullable=False)

    trainer = relationship("TrainerORM", back_populates="trainings")
    bookings = relationship("BookingORM", back_populates="training")


class BookingORM(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    training_id = Column(Integer, ForeignKey("trainings.id"), nullable=False)
    created_at = Column(DateTime, nullable=False)
    status = Column(String, nullable=False, default="active")

    client = relationship("ClientORM", back_populates="bookings")
    training = relationship("TrainingORM", back_populates="bookings")