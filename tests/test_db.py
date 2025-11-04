import pytest
from unittest.mock import MagicMock, patch
from db import PerevalDatabase

@pytest.fixture
def mock_db():
    db = PerevalDatabase()
    db.connection = MagicMock()
    return db

def test_add_pereval_success(mock_db):
    data = {"title": "Тестовый перевал", "user": {"email": "test@test.ru"}}
    cur = MagicMock()
    cur.fetchone.return_value = [1]
    mock_db.connection.cursor.return_value.__enter__.return_value = cur

    with patch("json.dumps", return_value="{}"):
        result = mock_db.add_pereval(data)

    assert cur.execute.called

def test_add_pereval_db_error(mock_db):
    mock_db.connection.cursor.side_effect = Exception("DB error")

    new_id, error = mock_db.add_pereval({"title": "Ошибка"})
    assert new_id is None
    assert "DB error" in error
