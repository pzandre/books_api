import json

from src.constants import BOOK_SEARCH_ENDPOINT


def test_add_review(client):
    book_id = 22400
    data = {"review": "Awesome book", "rating": 5}
    response = client.post(
        f"/{BOOK_SEARCH_ENDPOINT}/{book_id}/review", json.dumps(data)
    )
    assert response.status_code == 201
    assert response.json()["review"] == "Awesome book"
    assert response.json()["rating"] == 5
    assert response.json()["book_id"] == book_id


def test_add_review_invalid_rating(client):
    book_id = 22400
    data = {"review": "Awesome book", "rating": 6}
    response = client.post(
        f"/{BOOK_SEARCH_ENDPOINT}/{book_id}/review", json.dumps(data)
    )
    assert response.status_code == 422
    assert (
        response.json()["detail"][0]["msg"]
        == "ensure this value is less than or equal to 5.0"
    )
    assert response.json()["detail"][0]["type"] == "value_error.number.not_le"
    assert response.json()["detail"][0]["loc"] == ["body", "rating"]


def test_add_review_invalid_book_id(client):
    book_id = 2240000000
    data = {"review": "Awesome book", "rating": 5}
    response = client.post(
        f"/{BOOK_SEARCH_ENDPOINT}/{book_id}/review", json.dumps(data)
    )
    assert response.status_code == 404
    assert response.json()["detail"] == {"detail": "Not found."}


def test_add_review_empty_review(client):
    book_id = 22400
    data = {"review": "", "rating": 5}
    response = client.post(
        f"/{BOOK_SEARCH_ENDPOINT}/{book_id}/review", json.dumps(data)
    )
    assert response.status_code == 422
    assert (
        response.json()["detail"][0]["msg"]
        == "ensure this value has at least 1 characters"
    )
    assert response.json()["detail"][0]["type"] == "value_error.any_str.min_length"
    assert response.json()["detail"][0]["loc"] == ["body", "review"]


def test_add_review_empty_rating(client):
    book_id = 22400
    data = {"review": "Awesome book", "rating": None}
    response = client.post(
        f"/{BOOK_SEARCH_ENDPOINT}/{book_id}/review", json.dumps(data)
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "none is not an allowed value"
    assert response.json()["detail"][0]["type"] == "type_error.none.not_allowed"
    assert response.json()["detail"][0]["loc"] == ["body", "rating"]
