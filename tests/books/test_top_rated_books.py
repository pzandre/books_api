import json

from src.constants import BOOK_SEARCH_ENDPOINT


def test_get_top_rated_books(client):
    book_id = 22400
    data = {"review": "Awesome book", "rating": 5}
    client.post(f"/{BOOK_SEARCH_ENDPOINT}/{book_id}/review", json.dumps(data))
    data = {"review": "Awesome book", "rating": 4}
    client.post(f"/{BOOK_SEARCH_ENDPOINT}/{book_id}/review", json.dumps(data))
    book_id = 22401
    data = {"review": "Awesome book", "rating": 4}
    client.post(f"/{BOOK_SEARCH_ENDPOINT}/{book_id}/review", json.dumps(data))
    data = {"review": "Awesome book", "rating": 4}
    client.post(f"/{BOOK_SEARCH_ENDPOINT}/{book_id}/review", json.dumps(data))
    request = client.get(f"/{BOOK_SEARCH_ENDPOINT}/top-rated")
    assert request.status_code == 200
    assert request.json()["books"][0]["id"] == 22400
    assert request.json()["books"][0]["rating"] == 4.5
    assert request.json()["books"][1]["id"] == 22401
    assert request.json()["books"][1]["rating"] == 4.0


def test_get_top_rated_books_limit_1(client):
    book_id = 22400
    data = {"review": "Awesome book", "rating": 5}
    client.post(f"/{BOOK_SEARCH_ENDPOINT}/{book_id}/review", json.dumps(data))
    data = {"review": "Awesome book", "rating": 4}
    client.post(f"/{BOOK_SEARCH_ENDPOINT}/{book_id}/review", json.dumps(data))
    book_id = 22401
    data = {"review": "Awesome book", "rating": 4}
    client.post(f"/{BOOK_SEARCH_ENDPOINT}/{book_id}/review", json.dumps(data))
    data = {"review": "Awesome book", "rating": 4}
    client.post(f"/{BOOK_SEARCH_ENDPOINT}/{book_id}/review", json.dumps(data))
    request = client.get(f"/{BOOK_SEARCH_ENDPOINT}/top-rated?limit=1")
    assert request.status_code == 200
    assert len(request.json()["books"]) == 1
    assert request.json()["books"][0]["id"] == 22400
    assert request.json()["books"][0]["rating"] == 4.5
