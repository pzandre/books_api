"""
Book schemas
"""

from typing import List, Optional

from pydantic import BaseModel, Field


class BookAuthor(BaseModel):
    """
    Book author schema
    """

    name: str
    birth_year: Optional[int] = None
    death_year: Optional[int] = None


class Book(BaseModel):
    """
    Book schema
    """

    id: int
    title: str
    authors: List[BookAuthor]
    languages: List[str]
    download_count: int


class BaseBookReview(BaseModel):
    """
    Base book review schema
    """

    review: str = Field(..., min_length=1, max_length=500, description="Book review")


class BaseBookId(BaseModel):
    """
    Base book ID schema
    """

    book_id: int


class BookRating(BaseModel):
    """
    Book rating schema
    """

    rating: float = Field(default=0.0, ge=0.0, le=5.0, description="Book rating")


class MonthlyRating(BookRating):
    """
    Monthly rating schema
    """

    month: str


class MonthlyRatingList(BaseBookId):
    """
    Monthly rating list schema
    """

    ratings: List[MonthlyRating]

    class Config:
        orm_mode = True


class BookWithReview(Book, BookRating):
    """
    Book with review schema
    """

    reviews: List[Optional[str]] = list()

    class Config:
        orm_mode = True


class BookListWithReview(BaseModel):
    """
    Book list with review schema
    """

    books: List[BookWithReview]


class APIResponse(BaseModel):
    """
    API response schema
    """

    count: int
    next: Optional[str]
    previous: Optional[str]
    books: List[Book]


class BookReviewAndRating(BaseBookReview, BookRating):
    """
    Book review and rating schema
    """


class BookReviewWithRatingAndBookID(BookReviewAndRating, BaseBookId):
    """
    Book review with rating and Book ID schema
    """

    class Config:
        orm_mode = True
