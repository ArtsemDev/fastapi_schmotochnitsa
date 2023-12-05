from fastapi.testclient import TestClient
from starlette import status

from app import app
from core.types import CategoryDetail


client = TestClient(app=app)


def test_category_list():
    response = client.get(url=app.url_path_for("category_list"))
    assert response.status_code == status.HTTP_200_OK
    assert response.headers.get("Content-Type") in {"application/json", "application/json; charset=utf-8"}
    data = response.json()
    try:
        [CategoryDetail(**category) for category in data]
    except Exception as e:
        assert False
