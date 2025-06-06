import sys, os
# Добавляем в PYTHONPATH корень проекта (один уровень выше папки tests)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_page():
    """
    Проверяет, что главная страница возвращает HTML с кодом 200.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

@pytest.fixture(scope="module")
def api_client():
    return TestClient(app)

def test_read_sites_empty(api_client):
    """
    Проверяет, что API GET /api/sites/ возвращает список.
    """
    response = api_client.get("/api/sites/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_and_delete_site(api_client):
    """
    Тест создания и удаления строительного объекта.
    """
    new_site = {"name": "Тестовый объект", "address": "ул. Примерная, 1"}
    create_resp = api_client.post("/api/sites/", json=new_site)
    assert create_resp.status_code == 200
    created = create_resp.json()
    assert created["name"] == new_site["name"]
    
    site_id = created["id"]
    delete_resp = api_client.delete(f"/api/sites/{site_id}")
    assert delete_resp.status_code == 200
    assert delete_resp.json().get("message") == "Site deleted successfully"
