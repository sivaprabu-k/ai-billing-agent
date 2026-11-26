import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session

from app.config import settings
from app.db.base import Base
from app.db.database import get_db
from app.main import app
from app.models import Role, User
from app.utils.security import hash_password

from app import models as _models  # noqa: F401


# Connect exclusively to the test database.
test_database_url = make_url(settings.DATABASE_URL).set(
    database="ai_billing_test_db"
)

test_engine = create_engine(
    test_database_url,
    echo=False,
)


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Create test tables before running tests and remove them afterward."""
    Base.metadata.create_all(bind=test_engine)

    yield

    Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()


@pytest.fixture
def db_session():
    """Provide an isolated database session for each test."""
    connection = test_engine.connect()
    transaction = connection.begin()

    session = Session(
        bind=connection,
        join_transaction_mode="create_savepoint",
    )

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session):
    """Provide a FastAPI test client with an overridden database."""

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()



@pytest.fixture
def role_users(db_session):
    """Create test users for all three application roles."""

    role_data = [
        ("Admin", "Administrator"),
        ("Billing Staff", "Billing operations"),
        ("Support Staff", "Customer support"),
    ]

    roles = {}

    for name, description in role_data:
        role = Role(
            name=name,
            description=description,
        )
        db_session.add(role)
        roles[name] = role

    db_session.flush()

    test_users = {
        "admin": {
            "name": "Test Admin",
            "email": "admin@test.com",
            "password": "AdminTest@123",
            "role": roles["Admin"],
        },
        "billing": {
            "name": "Test Billing",
            "email": "billing@test.com",
            "password": "BillingTest@123",
            "role": roles["Billing Staff"],
        },
        "support": {
            "name": "Test Support",
            "email": "support@test.com",
            "password": "SupportTest@123",
            "role": roles["Support Staff"],
        },
    }

    users = {}

    for key, user_data in test_users.items():
        user = User(
            name=user_data["name"],
            email=user_data["email"],
            hashed_password=hash_password(user_data["password"]),
            role_id=user_data["role"].id,
            is_active=True,
        )

        db_session.add(user)
        users[key] = user

    db_session.flush()

    return {
        "users": users,
        "credentials": test_users,
    }


@pytest.fixture
def authenticated_users(client, role_users):
    """Authenticate test users through the actual login endpoint."""

    authenticated = {}

    for key, credentials in role_users["credentials"].items():
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": credentials["email"],
                "password": credentials["password"],
            },
        )

        assert response.status_code == 200

        access_token = response.json()["data"]["access_token"]

        authenticated[key] = {
            "user": role_users["users"][key],
            "headers": {
                "Authorization": f"Bearer {access_token}"
            },
        }

    return authenticated
