from fitness_club.client import Client
from fitness_club.membership import TimeLimitedMembership, VisitLimitedMembership
from db.sa_models import ClientORM, MembershipORM


class ClientRepositorySA:
    def __init__(self, session):
        self._session = session

    def _save_membership(self, membership):
        if membership is None:
            return None
        if isinstance(membership, TimeLimitedMembership):
            orm_obj = MembershipORM(
                type="time_limited", name=membership.name,
                start_date=membership.start_date, end_date=membership.end_date,
            )
        elif isinstance(membership, VisitLimitedMembership):
            orm_obj = MembershipORM(type="visit_limited", name=membership.name, visits_left=membership.visits_left)
        else:
            raise ValueError(f"Неизвестный тип абонемента: {type(membership)}")
        self._session.add(orm_obj)
        self._session.flush()
        return orm_obj.id

    def _load_membership(self, membership_id):
        if membership_id is None:
            return None
        orm_obj = self._session.get(MembershipORM, membership_id)
        if orm_obj is None:
            return None
        if orm_obj.type == "time_limited":
            return TimeLimitedMembership(orm_obj.name, orm_obj.start_date, orm_obj.end_date)
        return VisitLimitedMembership(orm_obj.name, orm_obj.visits_left)

    def save(self, client):
        membership_id = self._save_membership(client.membership)
        if client.id is None:
            orm_obj = ClientORM(name=client.name, phone=client.phone, email=client.email, membership_id=membership_id)
            self._session.add(orm_obj)
            self._session.flush()
            client.id = orm_obj.id
        else:
            orm_obj = self._session.get(ClientORM, client.id)
            orm_obj.name = client.name
            orm_obj.phone = client.phone
            orm_obj.email = client.email
            orm_obj.membership_id = membership_id  # добавлено — раньше пропускалось
        return client.id

    def get_by_id(self, client_id):
        orm_obj = self._session.get(ClientORM, client_id)
        if orm_obj is None:
            return None
        client = Client(orm_obj.name, orm_obj.phone, orm_obj.email)
        client.id = client_id
        client.membership = self._load_membership(orm_obj.membership_id)
        return client