from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.dependencies import get_session
from api.schemas import ClientCreate, ClientOut, MembershipCreate
from repositories_sa.client_repository import ClientRepositorySA
from fitness_club.client import Client
from fitness_club.membership import TimeLimitedMembership, VisitLimitedMembership

router = APIRouter(prefix="/clients", tags=["clients"])


@router.post("", response_model=ClientOut, status_code=201)
def create_client(payload: ClientCreate, session: Session = Depends(get_session)):
    client = Client(payload.name, payload.phone, payload.email)
    repo = ClientRepositorySA(session)
    repo.save(client)
    session.commit()
    return client


@router.get("/{client_id}", response_model=ClientOut)
def get_client(client_id: int, session: Session = Depends(get_session)):
    repo = ClientRepositorySA(session)
    client = repo.get_by_id(client_id)
    if client is None:
        raise HTTPException(status_code=404, detail="Клиент не найден")
    return client


@router.post("/{client_id}/membership", response_model=ClientOut)
def assign_membership(client_id: int, payload: MembershipCreate, session: Session = Depends(get_session)):
    repo = ClientRepositorySA(session)
    client = repo.get_by_id(client_id)
    if client is None:
        raise HTTPException(status_code=404, detail="Клиент не найден")

    if payload.type == "time_limited":
        client.membership = TimeLimitedMembership(payload.name, payload.start_date, payload.end_date)
    elif payload.type == "visit_limited":
        client.membership = VisitLimitedMembership(payload.name, payload.visits_left)
    else:
        raise HTTPException(status_code=422, detail="Неизвестный тип абонемента")

    repo.save(client)
    session.commit()
    return client