def test_get_all_items_empty(client):
    response = client.get("/inventory")
    assert response.status_code == 200
    assert response.get_json() == []


def test_create_item(client):
    response = client.post("/inventory", json={"name": "Almond Milk", "price": 3.99})
    assert response.status_code == 201

    data = response.get_json()
    assert data["name"] == "Almond Milk"
    assert data["price"] == 3.99
    assert data["id"] == 1


def test_create_item_missing_name(client):
    response = client.post("/inventory", json={"price": 3.99})
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_get_single_item(client):
    client.post("/inventory", json={"name": "Almond Milk"})

    response = client.get("/inventory/1")
    assert response.status_code == 200
    assert response.get_json()["name"] == "Almond Milk"


def test_get_single_item_not_found(client):
    response = client.get("/inventory/999")
    assert response.status_code == 404


def test_update_item(client):
    client.post("/inventory", json={"name": "Almond Milk", "price": 3.99})

    response = client.patch("/inventory/1", json={"price": 4.49, "quantity": 10})
    assert response.status_code == 200

    data = response.get_json()
    assert data["price"] == 4.49
    assert data["quantity"] == 10
    assert data["name"] == "Almond Milk"  # unchanged fields stay the same


def test_update_item_not_found(client):
    response = client.patch("/inventory/999", json={"price": 4.49})
    assert response.status_code == 404


def test_delete_item(client):
    client.post("/inventory", json={"name": "Almond Milk"})

    response = client.delete("/inventory/1")
    assert response.status_code == 200

    follow_up = client.get("/inventory/1")
    assert follow_up.status_code == 404


def test_delete_item_not_found(client):
    response = client.delete("/inventory/999")
    assert response.status_code == 404


def test_get_all_items_after_multiple_creates(client):
    client.post("/inventory", json={"name": "Almond Milk"})
    client.post("/inventory", json={"name": "Oat Milk"})

    response = client.get("/inventory")
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]["name"] == "Almond Milk"
    assert data[1]["name"] == "Oat Milk"
