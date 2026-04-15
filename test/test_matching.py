def test_get_matches(client):
    response = client.get("/api/matches")
    assert response.status_code in [200, 401]