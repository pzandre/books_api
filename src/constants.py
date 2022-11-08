"""
Project constants
"""

import os

EXTERNAL_API_URL = os.getenv("EXTERNAL_API_URL", "https://gutendex.com/books/")
PROJECT_URL = os.getenv("PROJECT_URL", "http://localhost:8000")
BOOK_SEARCH_ENDPOINT = "books"

MONTHS = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December",
}
