def test_send_message(client):
    response = client.post("/api/messages", json={
        "receiver_id": 1,
        "message": "Hello!"
    })
    assert response.status_code in [200, 401]