from fitness_club.client import Client
from fitness_club.membership import TimeLimitedMembership, VisitLimitedMembership
from repositories.base import BaseRepository


class ClientRepository(BaseRepository):
    table_name = "clients"

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
        self._pending_membership_id = membership_id
        return super().save(client)

    def _to_row(self, client):
        return {
            "name": client.name,
            "phone": client.phone,
            "email": client.email,
            "membership_id": self._pending_membership_id,
        }

    def _from_row(self, row):
        client = Client(row["name"], row["phone"], row["email"])
        client.id = row["id"]
        client.membership = self._load_membership(row["membership_id"])
        return client