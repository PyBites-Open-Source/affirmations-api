from .db import create_db_and_tables, engine
from .models import Affirmation

from fastapi import FastAPI
from sqlmodel import Session

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/affirmations/", response_model=Affirmation)
def create_affirmation(affirmation: Affirmation):
    with Session(engine) as session:
        session.add(affirmation)
        session.commit()
        session.refresh(affirmation)
        return affirmation
