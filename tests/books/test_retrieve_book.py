import json

from src.constants import BOOK_SEARCH_ENDPOINT


def test_retrieve_book(client):
    book_id = 22400
    data = {"review": "Awesome book", "rating": 5}
    client.post(f"/{BOOK_SEARCH_ENDPOINT}/{book_id}/review", json.dumps(data))
    request = client.get(f"/{BOOK_SEARCH_ENDPOINT}/{book_id}")
    assert request.status_code == 200
    assert request.json()["id"] == book_id
    assert request.json()["reviews"][0] == "Awesome book"
    assert request.json()["rating"] == 5


def test_get_book_avg_rating(client):
    book_id = 22400
    data = {"review": "Awesome book", "rating": 5}
    client.post(f"/{BOOK_SEARCH_ENDPOINT}/{book_id}/review", json.dumps(data))
    data = {"review": "Awesome book", "rating": 4}
    client.post(f"/{BOOK_SEARCH_ENDPOINT}/{book_id}/review", json.dumps(data))
    request = client.get(f"/{BOOK_SEARCH_ENDPOINT}/{book_id}")
    assert request.status_code == 200
    assert request.json()["rating"] == 4.5
