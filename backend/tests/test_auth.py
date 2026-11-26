from datetime import datetime, timedelta, timezone
from uuid import UUID

from app.models import UserSession


def test_login_success(client, role_users):
    credentials = role_users["credentials"]["admin"]

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": credentials["email"],
            "password": credentials["password"],
        },
    )

    assert response.status_code == 200

    data = response.json()["data"]

    assert data["access_token"]
    assert data["refresh_token"]
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == credentials["email"]


def test_login_invalid_password(client, role_users):
    credentials = role_users["credentials"]["admin"]

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": credentials["email"],
            "password": "WrongPassword@123",
        },
    )

    assert response.status_code == 401


def test_refresh_token_success(client, role_users):
    credentials = role_users["credentials"]["admin"]

    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": credentials["email"],
            "password": credentials["password"],
        },
    )

    refresh_token = login_response.json()["data"]["refresh_token"]

    response = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": refresh_token},
    )

    assert response.status_code == 200
    assert response.json()["data"]["access_token"]
    assert response.json()["data"]["token_type"] == "bearer"


def test_refresh_token_invalid(client):
    response = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": "invalid-token"},
    )

    assert response.status_code == 401


def test_refresh_token_after_logout(client, role_users):
    credentials = role_users["credentials"]["admin"]

    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": credentials["email"],
            "password": credentials["password"],
        },
    )

    login_data = login_response.json()["data"]

    logout_response = client.post(
        "/api/v1/auth/logout",
        headers={
            "Authorization": f"Bearer {login_data['access_token']}"
        },
    )

    assert logout_response.status_code == 200

    refresh_response = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": login_data["refresh_token"]},
    )

    assert refresh_response.status_code == 401



def test_logout_revokes_access_token(client, role_users):
    credentials = role_users["credentials"]["admin"]

    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": credentials["email"],
            "password": credentials["password"],
        },
    )

    access_token = login_response.json()["data"]["access_token"]

    logout_response = client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert logout_response.status_code == 200

    profile_response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert profile_response.status_code == 401


def test_logout_without_authentication(client):
    response = client.post("/api/v1/auth/logout")

    assert response.status_code == 401


def test_change_password_success(client, role_users):
    credentials = role_users["credentials"]["admin"]

    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": credentials["email"],
            "password": credentials["password"],
        },
    )

    access_token = login_response.json()["data"]["access_token"]

    response = client.post(
        "/api/v1/auth/change-password",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "current_password": credentials["password"],
            "new_password": "NewAdminPassword@123",
        },
    )

    assert response.status_code == 200

    old_password_login = client.post(
        "/api/v1/auth/login",
        json={
            "email": credentials["email"],
            "password": credentials["password"],
        },
    )

    assert old_password_login.status_code == 401

    new_password_login = client.post(
        "/api/v1/auth/login",
        json={
            "email": credentials["email"],
            "password": "NewAdminPassword@123",
        },
    )

    assert new_password_login.status_code == 200


def test_change_password_with_incorrect_current_password(
    client,
    role_users,
):
    credentials = role_users["credentials"]["admin"]

    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": credentials["email"],
            "password": credentials["password"],
        },
    )

    access_token = login_response.json()["data"]["access_token"]

    response = client.post(
        "/api/v1/auth/change-password",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "current_password": "WrongPassword@123",
            "new_password": "NewAdminPassword@123",
        },
    )

    assert response.status_code == 400


def test_change_password_to_same_password(client, role_users):
    credentials = role_users["credentials"]["admin"]

    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": credentials["email"],
            "password": credentials["password"],
        },
    )

    access_token = login_response.json()["data"]["access_token"]

    response = client.post(
        "/api/v1/auth/change-password",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "current_password": credentials["password"],
            "new_password": credentials["password"],
        },
    )

    assert response.status_code == 400


def test_login_inactive_user(client, role_users, db_session):
    credentials = role_users["credentials"]["admin"]
    admin_user = role_users["users"]["admin"]

    admin_user.is_active = False
    db_session.flush()

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": credentials["email"],
            "password": credentials["password"],
        },
    )

    assert response.status_code == 401


def test_refresh_token_expired_session(client, role_users, db_session):
    credentials = role_users["credentials"]["admin"]

    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": credentials["email"],
            "password": credentials["password"],
        },
    )

    refresh_token = login_response.json()["data"]["refresh_token"]

    from app.utils.security import decode_refresh_token

    payload = decode_refresh_token(refresh_token)
    session_id = UUID(payload["sid"])

    user_session = db_session.query(UserSession).filter(
        UserSession.id == session_id
    ).first()

    user_session.expires_at = datetime.now(timezone.utc) - timedelta(minutes=5)
    db_session.flush()

    response = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": refresh_token},
    )

    assert response.status_code == 401