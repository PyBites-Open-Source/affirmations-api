from typing import List

from .db import create_db_and_tables, engine
from .models import (
    User,
    UserCreate,
    UserRead,
    Affirmation,
    AffirmationCreate,
    AffirmationRead,
)

from fastapi import FastAPI, HTTPException
from sqlmodel import Session, select

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/users/", response_model=UserRead)
def create_user(user: UserCreate):
    with Session(engine) as session:
        db_user = User.from_orm(user)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user


@app.get("/users/", response_model=List[UserRead])
def read_users():
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        return users


@app.get("/users/{user_id}", response_model=UserRead)
def read_user(user_id: int):
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user


@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        session.delete(user)
        session.commit()
        return {"ok": True}


@app.post("/affirmations/", response_model=AffirmationRead)
def create_affirmation(affirmation: AffirmationCreate):
    with Session(engine) as session:
        db_affirmation = Affirmation.from_orm(affirmation)
        session.add(db_affirmation)
        session.commit()
        session.refresh(db_affirmation)
        return db_affirmation


@app.get("/affirmations/", response_model=List[AffirmationRead])
def read_affirmations():
    with Session(engine) as session:
        affirmations = session.exec(select(Affirmation)).all()
        return affirmations


@app.get("/affirmations/{affirmation_id}", response_model=AffirmationRead)
def read_affirmation(affirmation_id: int):
    with Session(engine) as session:
        affirmation = session.get(Affirmation, affirmation_id)
        if not affirmation:
            raise HTTPException(status_code=404, detail="Affirmation not found")
        return affirmation


@app.delete("/affirmations/{affirmation_id}")
def delete_affirmation(affirmation_id: int):
    with Session(engine) as session:
        affirmation = session.get(Affirmation, affirmation_id)
        if not affirmation:
            raise HTTPException(status_code=404, detail="Affirmation not found")
        session.delete(affirmation)
        session.commit()
        return {"ok": True}
