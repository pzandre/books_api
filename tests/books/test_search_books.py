from src.constants import BOOK_SEARCH_ENDPOINT, PROJECT_URL


def test_search_book(client):
    request = client.get(f"/{BOOK_SEARCH_ENDPOINT}/?search=Tolkien")
    assert request.status_code == 200
    assert request.json()["books"][0]["id"] == 43737
    assert (
        request.json()["books"][0]["title"]
        == "A Middle English Vocabulary, Designed for use with Sisam's Fourteenth Century Verse & Prose"
    )


def test_search_book_invalid(client):
    request = client.get(
        f"/{BOOK_SEARCH_ENDPOINT}/?search=01101110 01101111 01110100 00100000 01100001 00100000 01100010 01101111 01101111 01101011"
    )
    assert request.status_code == 200
    assert request.json()["books"] == []


def test_search_book_empty(client):
    request = client.get(f"/{BOOK_SEARCH_ENDPOINT}/?search=")
    assert request.status_code == 400
    assert request.json()["detail"] == "Search string is required"


def test_search_books_pagination(client):
    request = client.get(f"/{BOOK_SEARCH_ENDPOINT}?search=ghosts")
    assert request.status_code == 200
    assert (
        request.json()["next"]
        == f"{PROJECT_URL}/{BOOK_SEARCH_ENDPOINT}?page=2&search=ghosts"
    )
    assert request.json()["previous"] == None
    request = client.get(f"/{BOOK_SEARCH_ENDPOINT}?search=ghosts&page=2")
    assert request.status_code == 200
    assert request.json()["next"] == None
    assert (
        request.json()["previous"]
        == f"{PROJECT_URL}/{BOOK_SEARCH_ENDPOINT}?search=ghosts"
    )
