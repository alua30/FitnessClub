from fitness_club.booking import Booking
from db.sa_models import BookingORM


class BookingRepositorySA:
    def __init__(self, session, client_repo, training_repo):
        self._session = session
        self._client_repo = client_repo
        self._training_repo = training_repo

    def _to_domain(self, orm_obj):
        client = self._client_repo.get_by_id(orm_obj.client_id)
        training = self._training_repo.get_by_id(orm_obj.training_id)
        booking = Booking(client, training, orm_obj.created_at)
        booking.id = orm_obj.id
        booking._status = orm_obj.status
        return booking

    def save(self, booking):
        if booking.id is None:
            orm_obj = BookingORM(
                client_id=booking.client.id, training_id=booking.training.id,
                created_at=booking.created_at, status=booking.status,
            )
            self._session.add(orm_obj)
            self._session.flush()
            booking.id = orm_obj.id
        else:
            orm_obj = self._session.get(BookingORM, booking.id)
            orm_obj.status = booking.status
        return booking.id

    def filter_by_client(self, client_id):
        orm_objs = self._session.query(BookingORM).filter_by(client_id=client_id).all()
        return [self._to_domain(o) for o in orm_objs]

    def filter_by_training(self, training_id):
        orm_objs = self._session.query(BookingORM).filter_by(training_id=training_id).all()
        return [self._to_domain(o) for o in orm_objs]