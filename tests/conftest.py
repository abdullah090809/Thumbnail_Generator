import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.cores.config import settings
from app.cores.database import Base, get_db
from app.models.user import User
from app.cores.security import (
    hash_password,
    create_access_token
)

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.DATABASE_USERNAME}:"
    f"{settings.DATABASE_PASSWORD}@"
    f"{settings.DATABASE_HOSTNAME}:"
    f"{settings.DATABASE_PORT}/"
    f"{settings.DATABASE_NAME}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)

    yield

    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def session():

    connection = engine.connect()

    transaction = connection.begin()

    db = TestingSessionLocal(bind=connection)

    try:
        yield db
    finally:
        db.close()
        transaction.rollback()
        connection.close()


@pytest.fixture()
def client(session):

    def override_get_db():
        try:
            yield session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture()
def test_user(session):

    user_data = {
        "email": "test@example.com",
        "password": "password123"
    }

    user = User(
        email=user_data["email"],
        password=hash_password(user_data["password"])
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    user_data["id"] = user.id

    return user_data


@pytest.fixture()
def token(test_user):

    return create_access_token(
        {"user_id": test_user["id"]}
    )


@pytest.fixture()
def authorized_client(client, token):

    client.headers.update(
        {
            "Authorization": f"Bearer {token}"
        }
    )

    return client
