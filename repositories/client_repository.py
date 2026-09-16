from fitness_club.client import Client
from fitness_club.membership import TimeLimitedMembership, VisitLimitedMembership
from repositories.base import Repository


class ClientRepository(Repository):
    def __init__(self, connection):
        self._connection = connection

    def _save_membership(self, membership):
        if membership is None:
            return None
        with self._connection.cursor() as cur:
            if isinstance(membership, TimeLimitedMembership):
                cur.execute(
                    """INSERT INTO memberships (type, name, start_date, end_date, visits_left)
                       VALUES (%s, %s, %s, %s, NULL) RETURNING id""",
                    ("time_limited", membership.name, membership.start_date, membership.end_date),
                )
            elif isinstance(membership, VisitLimitedMembership):
                cur.execute(
                    """INSERT INTO memberships (type, name, start_date, end_date, visits_left)
                       VALUES (%s, %s, NULL, NULL, %s) RETURNING id""",
                    ("visit_limited", membership.name, membership.visits_left),
                )
            else:
                raise ValueError(f"Неизвестный тип абонемента: {type(membership)}")
            return cur.fetchone()[0]

    def _load_membership(self, membership_id):
        if membership_id is None:
            return None
        with self._connection.cursor() as cur:
            cur.execute(
                "SELECT type, name, start_date, end_date, visits_left FROM memberships WHERE id = %s",
                (membership_id,),
            )
            row = cur.fetchone()
        if row is None:
            return None
        mtype, name, start_date, end_date, visits_left = row
        if mtype == "time_limited":
            return TimeLimitedMembership(name, start_date, end_date)
        if mtype == "visit_limited":
            return VisitLimitedMembership(name, visits_left)
        raise ValueError(f"Неизвестный тип абонемента в БД: {mtype}")

    def save(self, client):
        membership_id = self._save_membership(client.membership)
        with self._connection.cursor() as cur:
            cur.execute(
                """INSERT INTO clients (name, phone, email, membership_id)
                   VALUES (%s, %s, %s, %s) RETURNING id""",
                (client.name, client.phone, client.email, membership_id),
            )
            client.id = cur.fetchone()[0]
        self._connection.commit()
        return client.id

    def get_by_id(self, client_id):
        with self._connection.cursor() as cur:
            cur.execute(
                "SELECT name, phone, email, membership_id FROM clients WHERE id = %s",
                (client_id,),
            )
            row = cur.fetchone()
        if row is None:
            return None
        name, phone, email, membership_id = row
        client = Client(name, phone, email)
        client.id = client_id
        client.membership = self._load_membership(membership_id)
        return client

    def list(self):
        with self._connection.cursor() as cur:
            cur.execute("SELECT id FROM clients")
            ids = [r[0] for r in cur.fetchall()]
        return [self.get_by_id(i) for i in ids]