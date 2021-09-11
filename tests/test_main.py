import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from affirmations.main import app, get_session
from affirmations.models import Affirmation, User


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="user_1")
def user_fixture(session: Session):
    user = User(name="bob", handle="pybob")
    session.add(user)
    session.commit()
    yield user
    session.delete(user)


def test_create_user(client: TestClient):
    response = client.post("/users/", json={"name": "bob", "handle": "pybob"})
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "bob"
    assert data["handle"] == "pybob"
    assert data["id"] is not None


def test_create_user_incomplete(client: TestClient):
    # No hande
    response = client.post("/users/", json={"name": "bob"})
    assert response.status_code == 422


def test_create_user_invalid(client: TestClient):
    # handle has an invalid type
    response = client.post("/users/", json={"name": "bob", "handle": {"key": "value"}})
    assert response.status_code == 422


def test_read_users(session: Session, client: TestClient, user_1: User):
    user_2 = User(name="julian", handle="pyjul")
    session.add(user_2)
    session.commit()

    response = client.get("/users/")
    data = response.json()

    assert response.status_code == 200

    assert len(data) == 2
    assert data[0]["name"] == user_1.name
    assert data[0]["handle"] == user_1.handle
    assert data[0]["id"] == user_1.id
    assert data[1]["name"] == user_2.name
    assert data[1]["handle"] == user_2.handle
    assert data[1]["id"] == user_2.id


def test_read_user(session: Session, client: TestClient, user_1: User):
    response = client.get(f"/users/{user_1.id}")
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == user_1.name
    assert data["handle"] == user_1.handle
    assert data["id"] == user_1.id


def test_delete_user(session: Session, client: TestClient, user_1: User):
    response = client.delete(f"/users/{user_1.id}")
    user_in_db = session.get(User, user_1.id)

    assert response.status_code == 200
    assert user_in_db is None


def test_create_affirmation(client: TestClient, user_1: User):
    response = client.post(
        "/affirmations/",
        json={"text": "I can overcome any problem", "user_id": user_1.id},
    )
    data = response.json()

    assert response.status_code == 200
    assert data["text"] == "I can overcome any problem"
    assert data["user_id"] == 1
    assert data["id"] is not None


def test_create_affirmation_wrong_user(client: TestClient, user_1: User):
    response = client.post(
        "/affirmations/", json={"text": "I can overcome any problem", "user_id": 0}
    )

    data = response.json()

    assert response.status_code == 400
    assert data["detail"] == "Not a valid user id"


def test_delete_affirmation(session: Session, client: TestClient, user_1: User):
    response = client.post(
        "/affirmations/",
        json={"text": "I can overcome any problem", "user_id": user_1.id},
    )
    data = response.json()

    affirmation_id = data["id"]
    response = client.delete(f"/affirmations/{affirmation_id}")
    assert response.status_code == 200

    affirmation_in_db = session.get(Affirmation, affirmation_id)
    assert affirmation_in_db is None


def test_read_affirmations(client: TestClient, user_1: User):
    affirmations = (
        "I am unstoppable",
        "I can overcome any challenge",
        "I am energetic",
        "I workout everyday",
    )
    for text in affirmations:
        client.post("/affirmations/", json={"text": text, "user_id": user_1.id})
    response = client.get("/affirmations/")
    data = response.json()

    assert response.status_code == 200

    assert len(data) == 4
    stored_affirmations = sorted(row["text"] for row in data)
    assert stored_affirmations == sorted(affirmations)


def test_delete_user_deletes_assoc_affirmations(client: TestClient, user_1: User):
    affirmations = (
        "I do my affirmations first thing in the morning",
        "I eat healthy foods",
        "I am in control",
    )
    for text in affirmations:
        client.post("/affirmations/", json={"text": text, "user_id": user_1.id})
    response = client.get("/affirmations/")

    data = response.json()
    assert len(data) == 3

    response = client.delete(f"/users/{user_1.id}")
    assert response.status_code == 200

    # cascade: affirmations of user get deleted as well upon user deletion
    response = client.get("/affirmations/")
    data = response.json()
    assert len(data) == 0
