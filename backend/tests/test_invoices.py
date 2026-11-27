import pytest
from app.models import Invoice

def create_test_customer(
    client,
    headers,
    name="Invoice Test Customer",
    email="invoice.customer@test.com",
    plan="Premium",
):
    response = client.post(
        "/api/v1/customers/",
        json={
            "name": name,
            "email": email,
            "plan": plan,
        },
        headers=headers,
    )

    assert response.status_code == 201
    return response.json()["data"]


def create_test_invoice(
    client,
    headers,
    customer_id=None,
    items=None,
):
    if customer_id is None:
        customer = create_test_customer(client, headers)
        customer_id = customer["id"]

    payload = {
        "customer_id": customer_id,
        "invoice_date": "2026-11-27",
        "due_date": "2026-12-15",
        "notes": "Invoice API test",
        "items": items or [
            {
                "description": "Development Service",
                "quantity": "2.00",
                "unit_price": "1000.00",
                "tax_rate": "18.00",
            },
            {
                "description": "Support Service",
                "quantity": "1.00",
                "unit_price": "500.00",
                "tax_rate": "18.00",
            },
        ],
    }

    response = client.post(
        "/api/v1/invoices/",
        json=payload,
        headers=headers,
    )

    assert response.status_code == 201
    return response.json()["data"]


@pytest.mark.parametrize("role", ["admin", "billing"])
def test_create_invoice_success(client, authenticated_users, role):
    headers = authenticated_users[role]["headers"]

    invoice = create_test_invoice(client, headers)

    assert invoice["id"] is not None
    assert invoice["customer_id"] is not None
    assert invoice["invoice_number"].startswith("INV-2026-")
    assert invoice["status"] == "Draft"

    assert invoice["subtotal"] == "2500.00"
    assert invoice["tax_amount"] == "450.00"
    assert invoice["total_amount"] == "2950.00"

    assert len(invoice["items"]) == 2



def test_support_staff_cannot_create_invoice(
    client,
    authenticated_users,
):
    admin_headers = authenticated_users["admin"]["headers"]
    support_headers = authenticated_users["support"]["headers"]

    customer = create_test_customer(client, admin_headers)

    response = client.post(
        "/api/v1/invoices/",
        json={
            "customer_id": customer["id"],
            "invoice_date": "2026-11-27",
            "items": [
                {
                    "description": "Development Service",
                    "quantity": "1.00",
                    "unit_price": "1000.00",
                    "tax_rate": "18.00",
                }
            ],
        },
        headers=support_headers,
    )

    assert response.status_code == 403



def test_create_invoice_with_invalid_quantity(client, authenticated_users):
    headers = authenticated_users["billing"]["headers"]
    customer = create_test_customer(client, headers)

    response = client.post(
        "/api/v1/invoices/",
        json={
            "customer_id": customer["id"],
            "invoice_date": "2026-11-27",
            "items": [
                {
                    "description": "Invalid Service",
                    "quantity": "0.00",
                    "unit_price": "100.00",
                    "tax_rate": "18.00",
                }
            ],
        },
        headers=headers,
    )

    assert response.status_code == 422


def test_create_invoice_with_invalid_tax_rate(client, authenticated_users):
    headers = authenticated_users["billing"]["headers"]
    customer = create_test_customer(client, headers)

    response = client.post(
        "/api/v1/invoices/",
        json={
            "customer_id": customer["id"],
            "invoice_date": "2026-11-27",
            "items": [
                {
                    "description": "Invalid Service",
                    "quantity": "1.00",
                    "unit_price": "100.00",
                    "tax_rate": "120.00",
                }
            ],
        },
        headers=headers,
    )

    assert response.status_code == 422


def test_create_invoice_with_due_date_before_invoice_date(
    client,
    authenticated_users,
):
    headers = authenticated_users["billing"]["headers"]
    customer = create_test_customer(client, headers)

    response = client.post(
        "/api/v1/invoices/",
        json={
            "customer_id": customer["id"],
            "invoice_date": "2026-11-27",
            "due_date": "2026-11-20",
            "items": [
                {
                    "description": "Development Service",
                    "quantity": "1.00",
                    "unit_price": "1000.00",
                }
            ],
        },
        headers=headers,
    )

    assert response.status_code == 422



@pytest.mark.parametrize("role", ["admin", "billing", "support"])
def test_list_invoices_success(client, authenticated_users, role):
    admin_headers = authenticated_users["admin"]["headers"]
    role_headers = authenticated_users[role]["headers"]

    create_test_invoice(client, admin_headers)
    response = client.get(
        "/api/v1/invoices/",
        headers=role_headers,
    )

    assert response.status_code == 200

    data = response.json()["data"]

    assert "items" in data
    assert "pagination" in data
    assert len(data["items"]) >= 1



def test_list_invoices_with_pagination(client, authenticated_users):
    headers = authenticated_users["admin"]["headers"]

    customer = create_test_customer(client, headers)

    create_test_invoice(
        client,
        headers,
        customer_id=customer["id"],
    )
    create_test_invoice(
        client,
        headers,
        customer_id=customer["id"],
    )
    response = client.get(
        "/api/v1/invoices/?page=1&limit=1",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()["data"]

    assert len(data["items"]) == 1
    assert data["pagination"]["page"] == 1
    assert data["pagination"]["limit"] == 1
    assert data["pagination"]["total_items"] == 2



def test_list_invoices_with_search(client, authenticated_users):
    headers = authenticated_users["admin"]["headers"]

    invoice = create_test_invoice(client, headers)

    response = client.get(
        f"/api/v1/invoices/?search={invoice['invoice_number']}",
        headers=headers,
    )

    assert response.status_code == 200

    items = response.json()["data"]["items"]

    assert any(
        item["invoice_number"] == invoice["invoice_number"]
        for item in items
    )


def test_list_invoices_with_status_filter(client, authenticated_users):
    headers = authenticated_users["admin"]["headers"]

    create_test_invoice(client, headers)

    response = client.get(
        "/api/v1/invoices/?status=Draft",
        headers=headers,
    )

    assert response.status_code == 200

    items = response.json()["data"]["items"]

    assert all(item["status"] == "Draft" for item in items)


def test_list_invoices_with_invalid_status(client, authenticated_users):
    headers = authenticated_users["admin"]["headers"]

    response = client.get(
        "/api/v1/invoices/?status=Invalid",
        headers=headers,
    )

    assert response.status_code == 422


@pytest.mark.parametrize("role", ["admin", "billing", "support"])
def test_get_invoice_success(client, authenticated_users, role):
    admin_headers = authenticated_users["admin"]["headers"]
    role_headers = authenticated_users[role]["headers"]

    invoice = create_test_invoice(client, admin_headers)

    response = client.get(
        f"/api/v1/invoices/{invoice['id']}",
        headers=role_headers,
    )

    assert response.status_code == 200

    data = response.json()["data"]

    assert data["id"] == invoice["id"]
    assert data["invoice_number"] == invoice["invoice_number"]
    assert len(data["items"]) == 2


def test_get_invoice_not_found(client, authenticated_users):
    headers = authenticated_users["admin"]["headers"]

    response = client.get(
        "/api/v1/invoices/99999",
        headers=headers,
    )

    assert response.status_code == 404


@pytest.mark.parametrize("role", ["admin", "billing"])
def test_update_invoice_success(client, authenticated_users, role):
    headers = authenticated_users[role]["headers"]

    invoice = create_test_invoice(client, headers)

    response = client.patch(
        f"/api/v1/invoices/{invoice['id']}",
        json={
            "due_date": "2026-12-20",
            "notes": "Updated invoice notes",
        },
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()["data"]

    assert data["id"] == invoice["id"]
    assert data["due_date"] == "2026-12-20"
    assert data["notes"] == "Updated invoice notes"


def test_support_staff_cannot_update_invoice(client, authenticated_users):
    admin_headers = authenticated_users["admin"]["headers"]
    support_headers = authenticated_users["support"]["headers"]

    invoice = create_test_invoice(client, admin_headers)

    response = client.patch(
        f"/api/v1/invoices/{invoice['id']}",
        json={"notes": "Unauthorized update"},
        headers=support_headers,
    )

    assert response.status_code == 403


def test_update_invoice_with_invalid_due_date(client, authenticated_users):
    headers = authenticated_users["admin"]["headers"]

    invoice = create_test_invoice(client, headers)

    response = client.patch(
        f"/api/v1/invoices/{invoice['id']}",
        json={"due_date": "2026-11-20"},
        headers=headers,
    )

    assert response.status_code == 400


@pytest.mark.parametrize("role", ["admin", "billing"])
def test_update_invoice_item_success(client, authenticated_users, role):
    headers = authenticated_users[role]["headers"]

    invoice = create_test_invoice(client, headers)
    item_id = invoice["items"][0]["id"]

    response = client.patch(
        f"/api/v1/invoices/{invoice['id']}/items/{item_id}",
        json={
            "quantity": "3.00",
            "unit_price": "1000.00",
            "tax_rate": "18.00",
        },
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()["data"]

    assert data["id"] == invoice["id"]
    assert data["subtotal"] == "3500.00"
    assert data["tax_amount"] == "630.00"
    assert data["total_amount"] == "4130.00"

    updated_item = next(
        item for item in data["items"]
        if item["id"] == item_id
    )

    assert updated_item["quantity"] == "3.00"
    assert updated_item["line_subtotal"] == "3000.00"
    assert updated_item["tax_amount"] == "540.00"
    assert updated_item["line_total"] == "3540.00"


def test_support_staff_cannot_update_invoice_item(
    client,
    authenticated_users,
):
    admin_headers = authenticated_users["admin"]["headers"]
    support_headers = authenticated_users["support"]["headers"]

    invoice = create_test_invoice(client, admin_headers)
    item_id = invoice["items"][0]["id"]

    response = client.patch(
        f"/api/v1/invoices/{invoice['id']}/items/{item_id}",
        json={"quantity": "3.00"},
        headers=support_headers,
    )

    assert response.status_code == 403


def test_update_invoice_item_not_found(client, authenticated_users):
    headers = authenticated_users["admin"]["headers"]

    invoice = create_test_invoice(client, headers)

    response = client.patch(
        f"/api/v1/invoices/{invoice['id']}/items/99999",
        json={"quantity": "3.00"},
        headers=headers,
    )

    assert response.status_code == 400


def test_update_invoice_item_with_invalid_quantity(
    client,
    authenticated_users,
):
    headers = authenticated_users["admin"]["headers"]

    invoice = create_test_invoice(client, headers)
    item_id = invoice["items"][0]["id"]

    response = client.patch(
        f"/api/v1/invoices/{invoice['id']}/items/{item_id}",
        json={"quantity": "0.00"},
        headers=headers,
    )

    assert response.status_code == 422


def test_admin_can_delete_draft_invoice(client, authenticated_users):
    headers = authenticated_users["admin"]["headers"]

    invoice = create_test_invoice(client, headers)

    response = client.delete(
        f"/api/v1/invoices/{invoice['id']}",
        headers=headers,
    )

    assert response.status_code == 200

    get_response = client.get(
        f"/api/v1/invoices/{invoice['id']}",
        headers=headers,
    )

    assert get_response.status_code == 404


@pytest.mark.parametrize("role", ["billing", "support"])
def test_non_admin_cannot_delete_invoice(client, authenticated_users, role):
    admin_headers = authenticated_users["admin"]["headers"]
    role_headers = authenticated_users[role]["headers"]

    invoice = create_test_invoice(client, admin_headers)

    response = client.delete(
        f"/api/v1/invoices/{invoice['id']}",
        headers=role_headers,
    )

    assert response.status_code == 403



def test_cannot_delete_issued_invoice(
    client,
    authenticated_users,
    db_session,
):
    headers = authenticated_users["admin"]["headers"]

    invoice = create_test_invoice(client, headers)

    db_invoice = db_session.query(Invoice).filter(
        Invoice.id == invoice["id"]
    ).first()

    db_invoice.status = "Issued"
    db_session.flush()

    response = client.delete(
        f"/api/v1/invoices/{invoice['id']}",
        headers=headers,
    )

    assert response.status_code == 400

    get_response = client.get(
        f"/api/v1/invoices/{invoice['id']}",
        headers=headers,
    )

    assert get_response.status_code == 200
