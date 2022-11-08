"""
Tests for the /books/{book_id}/monthly-rating endpoint
"""

import json
from datetime import datetime

from src.constants import BOOK_SEARCH_ENDPOINT


def test_get_book_monthly_rating(client):
    month = datetime.now().strftime("%B")
    book_id = 22400
    data = {"review": "Awesome book", "rating": 5}
    client.post(f"/{BOOK_SEARCH_ENDPOINT}/{book_id}/review", json.dumps(data))
    data = {"review": "Awesome book", "rating": 4}
    client.post(f"/{BOOK_SEARCH_ENDPOINT}/{book_id}/review", json.dumps(data))
    request = client.get(f"/{BOOK_SEARCH_ENDPOINT}/{book_id}/monthly-rating")
    assert request.status_code == 200
    assert request.json()["ratings"][0] == {"month": month, "rating": 4.5}
