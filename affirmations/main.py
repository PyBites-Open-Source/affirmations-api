from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Session, select

from .db import create_db_and_tables, get_session
from .models import (
    Affirmation,
    AffirmationCreate,
    AffirmationRead,
    User,
    UserCreate,
    UserRead,
)

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/users/", response_model=UserRead)
def create_user(*, session: Session = Depends(get_session), user: UserCreate):
    query = select(User).where(User.handle == user.handle)
    existing_user = session.exec(query).first()
    if existing_user is not None:
        raise HTTPException(status_code=400, detail="User already exists")

    db_user = User.from_orm(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@app.get("/users/", response_model=list[UserRead])
def read_users(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100)
):
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users


@app.get("/users/{user_id}", response_model=UserRead)
def read_user(*, session: Session = Depends(get_session), user_id: int):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.delete("/users/{user_id}")
def delete_user(*, session: Session = Depends(get_session), user_id: int):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"ok": True}


@app.post("/affirmations/", response_model=AffirmationRead)
def create_affirmation(
    *, session: Session = Depends(get_session), affirmation: AffirmationCreate
):
    query = select(Affirmation).where(Affirmation.text == affirmation.text)
    existing_affirmation = session.exec(query).first()
    if existing_affirmation is not None:
        raise HTTPException(status_code=400, detail="Affirmation already exists")

    db_affirmation = Affirmation.from_orm(affirmation)

    user = session.get(User, affirmation.user_id)
    if user is None:
        raise HTTPException(status_code=400, detail="Not a valid user id")

    session.add(db_affirmation)
    session.commit()
    session.refresh(db_affirmation)
    return db_affirmation


@app.get("/affirmations/", response_model=list[AffirmationRead])
def read_affirmations(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100)
):
    affirmations = session.exec(select(Affirmation).offset(offset).limit(limit)).all()
    return affirmations


@app.get("/affirmations/{affirmation_id}", response_model=AffirmationRead)
def read_affirmation(*, session: Session = Depends(get_session), affirmation_id: int):
    affirmation = session.get(Affirmation, affirmation_id)
    if not affirmation:
        raise HTTPException(status_code=404, detail="Affirmation not found")
    return affirmation


@app.delete("/affirmations/{affirmation_id}")
def delete_affirmation(*, session: Session = Depends(get_session), affirmation_id: int):
    affirmation = session.get(Affirmation, affirmation_id)
    if not affirmation:
        raise HTTPException(status_code=404, detail="Affirmation not found")
    session.delete(affirmation)
    session.commit()
    return {"ok": True}
