import pytest


def create_test_customer(
    client,
    headers,
    name="Test Customer",
    email="customer@test.com",
    plan="Premium",
):
    return client.post(
        "/api/v1/customers/",
        headers=headers,
        json={
            "name": name,
            "email": email,
            "plan": plan,
        },
    )


@pytest.mark.parametrize("role", ["admin", "billing"])
def test_create_customer_success(client, authenticated_users, role):
    headers = authenticated_users[role]["headers"]

    response = create_test_customer(client, headers)

    assert response.status_code == 201
    data = response.json()["data"]
    assert data["name"] == "Test Customer"
    assert data["email"] == "customer@test.com"
    assert data["customer_code"].startswith("CUS-")
    assert data["status"] == "Active"


def test_support_staff_cannot_create_customer(client, authenticated_users):
    headers = authenticated_users["support"]["headers"]

    response = create_test_customer(client, headers)

    assert response.status_code == 403


def test_create_customer_with_duplicate_email(
    client,
    authenticated_users,
):
    headers = authenticated_users["admin"]["headers"]

    create_test_customer(client, headers)

    response = create_test_customer(
        client,
        headers,
        name="Another Customer",
    )

    assert response.status_code == 409


@pytest.mark.parametrize("role", ["admin", "billing", "support"])
def test_list_customers_success(client, authenticated_users, role):
    headers = authenticated_users[role]["headers"]

    create_test_customer(client, authenticated_users["admin"]["headers"])

    response = client.get(
        "/api/v1/customers/",
        headers=headers,
    )

    assert response.status_code == 200
    data = response.json()["data"]
    assert len(data["items"]) == 1
    assert data["pagination"]["total_items"] == 1


@pytest.mark.parametrize("role", ["admin", "billing", "support"])
def test_get_customer_by_id(client, authenticated_users, role):
    admin_headers = authenticated_users["admin"]["headers"]
    headers = authenticated_users[role]["headers"]

    create_response = create_test_customer(client, admin_headers)
    customer_id = create_response.json()["data"]["id"]

    response = client.get(
        f"/api/v1/customers/{customer_id}",
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["data"]["id"] == customer_id


def test_get_nonexistent_customer(client, authenticated_users):
    headers = authenticated_users["admin"]["headers"]

    response = client.get(
        "/api/v1/customers/99999",
        headers=headers,
    )

    assert response.status_code == 404


@pytest.mark.parametrize("role", ["admin", "billing"])
def test_update_customer_success(client, authenticated_users, role):
    admin_headers = authenticated_users["admin"]["headers"]
    headers = authenticated_users[role]["headers"]

    create_response = create_test_customer(client, admin_headers)
    customer_id = create_response.json()["data"]["id"]

    response = client.patch(
        f"/api/v1/customers/{customer_id}",
        headers=headers,
        json={"name": "Updated Customer"},
    )

    assert response.status_code == 200
    assert response.json()["data"]["name"] == "Updated Customer"


def test_support_staff_cannot_update_customer(
    client,
    authenticated_users,
):
    admin_headers = authenticated_users["admin"]["headers"]
    support_headers = authenticated_users["support"]["headers"]

    create_response = create_test_customer(client, admin_headers)
    customer_id = create_response.json()["data"]["id"]

    response = client.patch(
        f"/api/v1/customers/{customer_id}",
        headers=support_headers,
        json={"name": "Unauthorized Update"},
    )

    assert response.status_code == 403


def test_admin_can_deactivate_customer(client, authenticated_users):
    admin_headers = authenticated_users["admin"]["headers"]

    create_response = create_test_customer(client, admin_headers)
    customer_id = create_response.json()["data"]["id"]

    response = client.delete(
        f"/api/v1/customers/{customer_id}",
        headers=admin_headers,
    )

    assert response.status_code == 200

    get_response = client.get(
        f"/api/v1/customers/{customer_id}",
        headers=admin_headers,
    )

    assert get_response.status_code == 200
    assert get_response.json()["data"]["status"] == "Inactive"


@pytest.mark.parametrize("role", ["billing", "support"])
def test_non_admin_cannot_deactivate_customer(
    client,
    authenticated_users,
    role,
):
    admin_headers = authenticated_users["admin"]["headers"]
    headers = authenticated_users[role]["headers"]

    create_response = create_test_customer(client, admin_headers)
    customer_id = create_response.json()["data"]["id"]

    response = client.delete(
        f"/api/v1/customers/{customer_id}",
        headers=headers,
    )

    assert response.status_code == 403


def test_search_customers(client, authenticated_users):
    headers = authenticated_users["admin"]["headers"]

    create_test_customer(
        client,
        headers,
        name="Alice Johnson",
        email="alice@test.com",
    )
    create_test_customer(
        client,
        headers,
        name="Bob Smith",
        email="bob@test.com",
    )

    response = client.get(
        "/api/v1/customers/?search=Alice",
        headers=headers,
    )

    assert response.status_code == 200
    data = response.json()["data"]
    assert len(data["items"]) == 1
    assert data["items"][0]["name"] == "Alice Johnson"


def test_filter_customers_by_status(client, authenticated_users):
    headers = authenticated_users["admin"]["headers"]

    create_response = create_test_customer(client, headers)
    customer_id = create_response.json()["data"]["id"]

    client.delete(
        f"/api/v1/customers/{customer_id}",
        headers=headers,
    )

    response = client.get(
        "/api/v1/customers/?status=Inactive",
        headers=headers,
    )

    assert response.status_code == 200
    data = response.json()["data"]
    assert len(data["items"]) == 1
    assert data["items"][0]["status"] == "Inactive"


def test_customer_pagination(client, authenticated_users):
    headers = authenticated_users["admin"]["headers"]

    for index in range(3):
        create_test_customer(
            client,
            headers,
            name=f"Customer {index}",
            email=f"customer{index}@test.com",
        )

    response = client.get(
        "/api/v1/customers/?page=1&limit=2",
        headers=headers,
    )

    assert response.status_code == 200
    data = response.json()["data"]
    pagination = data["pagination"]

    assert len(data["items"]) == 2
    assert pagination["page"] == 1
    assert pagination["limit"] == 2
    assert pagination["total_items"] == 3
    assert pagination["total_pages"] == 2
    assert pagination["has_next"] is True
    assert pagination["has_previous"] is False
