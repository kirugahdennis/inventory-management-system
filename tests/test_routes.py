
def test_get_all_items(client):
    resp = client.get("/inventory")
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data) == 1
    assert data[0]["name"] == "Test Item"


def test_get_item_found(client):
    resp = client.get("/inventory/1")
    assert resp.status_code == 200
    assert resp.get_json()["id"] == 1


def test_get_item_not_found(client):
    resp = client.get("/inventory/999")
    assert resp.status_code == 404


def test_create_item(client):
    payload = {"name": "New Item", "quantity": 10, "price": 4.5}
    resp = client.post("/inventory", json=payload)
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["name"] == "New Item"
    assert data["id"] == 2

    # confirm it's actually stored
    resp2 = client.get("/inventory")
    assert len(resp2.get_json()) == 2


def test_create_item_missing_name(client):
    resp = client.post("/inventory", json={"quantity": 3})
    assert resp.status_code == 400


def test_update_item(client):
    resp = client.patch("/inventory/1", json={"price": 9.99, "quantity": 2})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["price"] == 9.99
    assert data["quantity"] == 2


def test_update_item_not_found(client):
    resp = client.patch("/inventory/999", json={"price": 1.0})
    assert resp.status_code == 404


def test_update_item_no_body(client):
    resp = client.patch("/inventory/1", json={})
    assert resp.status_code == 400


def test_delete_item(client):
    resp = client.delete("/inventory/1")
    assert resp.status_code == 204

    resp2 = client.get("/inventory/1")
    assert resp2.status_code == 404


def test_delete_item_not_found(client):
    resp = client.delete("/inventory/999")
    assert resp.status_code == 404