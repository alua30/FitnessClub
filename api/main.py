from fastapi import FastAPI
from api.routers import clients, trainings, bookings

app = FastAPI(title="FitnessClub API")

app.include_router(clients.router)
app.include_router(trainings.router)
app.include_router(bookings.router)