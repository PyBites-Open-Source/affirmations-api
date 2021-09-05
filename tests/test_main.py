import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from affirmations.models import Affirmation, User
from affirmations.main import app, get_session


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


def test_read_users(session: Session, client: TestClient):
    user_1 = User(name="bob", handle="pybob")
    user_2 = User(name="julian", handle="pyjul")
    session.add(user_1)
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


def test_read_user(session: Session, client: TestClient):
    user_1 = User(name="bob", handle="pybob")
    session.add(user_1)
    session.commit()

    response = client.get(f"/users/{user_1.id}")
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == user_1.name
    assert data["handle"] == user_1.handle
    assert data["id"] == user_1.id


def test_delete_user(session: Session, client: TestClient):
    user_1 = User(name="bob", handle="pybob")
    session.add(user_1)
    session.commit()

    response = client.delete(f"/users/{user_1.id}")
    user_in_db = session.get(User, user_1.id)

    assert response.status_code == 200
    assert user_in_db is None
