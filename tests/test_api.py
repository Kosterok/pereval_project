import pytest
from api import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()

@pytest.fixture
def sample_pereval():
    return {
        "beauty_title": "пер.",
        "title": "Тестовый перевал",
        "other_titles": "Тест",
        "connect": "",
        "add_time": "2025-11-01 13:18:13",
        "user": {
            "email": "test@test.ru",
            "fam": "Иванов",
            "name": "Иван",
            "otc": "Иванович",
            "phone": "+79999999999"
        },
        "coords": {
            "latitude": "55.727739",
            "longitude": "37.606945",
            "height": "1000"
        },
        "level": {"summer": "1А"},
        "images": [{"data": "img1", "title": "Седловина"}]
    }

# Тест POST /submitData
def test_submit_data_success(client, sample_pereval, monkeypatch):
    class MockDB:
        def add_pereval(self, data):
            return 123, None
    monkeypatch.setattr("api.PerevalDatabase", lambda: MockDB())

    response = client.post("/submitData", json=sample_pereval)
    res = response.get_json()
    assert response.status_code == 200
    assert res["status"] == 200
    assert res["id"] == 123

def test_submit_data_missing_fields(client):
    response = client.post("/submitData", json={"title": "test"})
    res = response.get_json()
    assert response.status_code == 400
    assert "отсутствуют" in res["message"]

# Тест GET /submitData/<id>
def test_get_pereval_not_found(client, monkeypatch):
    class MockCursor:
        def __enter__(self): return self
        def __exit__(self, *args): pass
        def execute(self, *args, **kwargs): pass
        def fetchone(self): return None

    class MockConnection:
        def cursor(self): return MockCursor()

    monkeypatch.setattr("api.db", type("DB", (), {"connection": MockConnection()})())

    response = client.get("/submitData/9999")
    res = response.get_json()

    assert response.status_code == 404
    assert "не найден" in res["message"]

# Тест GET /submitData?user__email
def test_get_perevals_by_email_no_param(client):
    response = client.get("/submitData")
    res = response.get_json()
    assert response.status_code == 400
    assert "user__email" in res["message"]
