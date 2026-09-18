from db.sa_base import SessionLocal
from repositories_sa.client_repository import ClientRepositorySA
from repositories_sa.training_repository import TrainingRepositorySA
from repositories_sa.booking_repository import BookingRepositorySA


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_client_repo(session):
    return ClientRepositorySA(session)


def get_training_repo(session):
    return TrainingRepositorySA(session)


def get_booking_repo(session, client_repo, training_repo):
    return BookingRepositorySA(session, client_repo, training_repo)