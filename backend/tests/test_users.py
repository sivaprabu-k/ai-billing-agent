
def test_admin_create_user(client, authenticated_users, role_users):
    admin_headers = authenticated_users["admin"]["headers"]

    response = client.post(
        "/api/v1/users",
        headers=admin_headers,
        json={
            "name": "New Billing User",
            "email": "newbilling@test.com",
            "password": "NewBilling@123",
            "role_id": role_users["users"]["billing"].role_id,
        },
    )

    assert response.status_code == 201
    assert response.json()["data"]["email"] == "newbilling@test.com"
    assert response.json()["data"]["is_active"] is True


def test_admin_get_all_users(client, authenticated_users):
    admin_headers = authenticated_users["admin"]["headers"]

    response = client.get(
        "/api/v1/users",
        headers=admin_headers,
    )

    assert response.status_code == 200
    assert len(response.json()["data"]) == 3


def test_admin_get_user_by_id(client, authenticated_users):
    admin_headers = authenticated_users["admin"]["headers"]
    support_user = authenticated_users["support"]["user"]

    response = client.get(
        f"/api/v1/users/{support_user.id}",
        headers=admin_headers,
    )

    assert response.status_code == 200
    assert response.json()["data"]["email"] == "support@test.com"


def test_admin_update_user(client, authenticated_users):
    admin_headers = authenticated_users["admin"]["headers"]
    billing_user = authenticated_users["billing"]["user"]

    response = client.patch(
        f"/api/v1/users/{billing_user.id}",
        headers=admin_headers,
        json={
            "name": "Updated Billing User",
        },
    )

    assert response.status_code == 200
    assert response.json()["data"]["name"] == "Updated Billing User"


def test_admin_deactivate_user(client, authenticated_users):
    admin_headers = authenticated_users["admin"]["headers"]
    support_user = authenticated_users["support"]["user"]

    response = client.delete(
        f"/api/v1/users/{support_user.id}",
        headers=admin_headers,
    )

    assert response.status_code == 200
    assert response.json()["data"]["is_active"] is False


def test_billing_staff_cannot_access_user_list(
    client,
    authenticated_users,
):
    billing_headers = authenticated_users["billing"]["headers"]

    response = client.get(
        "/api/v1/users",
        headers=billing_headers,
    )

    assert response.status_code == 403


def test_support_staff_cannot_create_user(
    client,
    authenticated_users,
    role_users,
):
    support_headers = authenticated_users["support"]["headers"]

    response = client.post(
        "/api/v1/users",
        headers=support_headers,
        json={
            "name": "Unauthorized User",
            "email": "unauthorized@test.com",
            "password": "Unauthorized@123",
            "role_id": role_users["users"]["billing"].role_id,
        },
    )

    assert response.status_code == 403


def test_unauthenticated_user_cannot_access_user_list(client):
    response = client.get("/api/v1/users")

    assert response.status_code == 401


def test_admin_create_user_with_duplicate_email(
    client,
    authenticated_users,
    role_users,
):
    admin_headers = authenticated_users["admin"]["headers"]

    response = client.post(
        "/api/v1/users",
        headers=admin_headers,
        json={
            "name": "Duplicate User",
            "email": "billing@test.com",
            "password": "Duplicate@123",
            "role_id": role_users["users"]["billing"].role_id,
        },
    )

    assert response.status_code == 409
