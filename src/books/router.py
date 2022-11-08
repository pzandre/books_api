"""
Book API router
"""

from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from fastapi_cache.decorator import cache
from sqlalchemy.orm import Session

import books.repository as repository
import books.schemas as schemas
from constants import BOOK_SEARCH_ENDPOINT
from database import get_db

book_router = APIRouter(tags=["books"])


@book_router.get(
    f"/{BOOK_SEARCH_ENDPOINT}",
    response_model=schemas.APIResponse,
    status_code=status.HTTP_200_OK,
    summary="Search for books by title",
    description="Search for books by title",
)
@cache(expire=60)
async def search_books(
    search: str = Query(...), page: Optional[int] = Query(default=None, ge=1)
):
    """
    Search for books by title

    :param search: Search term
    :param page: Page number

    :return: List of books
    """

    results = await repository.get_books_by_title(search, page)
    return results


@book_router.get(
    f"/{BOOK_SEARCH_ENDPOINT}/top-rated",
    response_model=schemas.BookListWithReview,
    status_code=status.HTTP_200_OK,
    summary="Get top rated books",
    description="Get top rated books",
)
async def get_top_rated_books(
    limit: Optional[int] = Query(default=10, ge=1), db: Session = Depends(get_db)
):
    """
    Get top rated books

    :param limit: Number of results to return
    :param db: Database session

    :return: List of top rated books
    """

    results = await repository.get_top_rated_books(limit, db)
    return {"books": results}


@book_router.get(
    f"/{BOOK_SEARCH_ENDPOINT}/" + "{book_id}/monthly-rating",
    response_model=schemas.MonthlyRatingList,
    status_code=status.HTTP_200_OK,
    summary="Get book monthly rating",
    description="Get book monthly rating",
)
async def get_monthly_rating(book_id: int, db: Session = Depends(get_db)):
    """
    Get book monthly rating

    :param book_id: Book ID
    :param db: Database session

    :return: Book monthly rating
    """

    results = await repository.get_monthly_rating(book_id, db)
    return results


@book_router.post(
    f"/{BOOK_SEARCH_ENDPOINT}/" + "{book_id}/review",
    response_model=schemas.BookReviewWithRatingAndBookID,
    status_code=status.HTTP_201_CREATED,
    summary="Add a review for a book",
    description="Add a review for a book",
)
async def add_review(
    book_id: int,
    book_review: schemas.BookReviewAndRating,
    db: Session = Depends(get_db),
):
    """
    Add a review for a book

    :param book_id: Book ID
    :param book_review: Book review
    :param db: Database session

    :return: Book with review
    """

    review = await repository.create_review(book_id, book_review, db)
    return review


@book_router.get(
    f"/{BOOK_SEARCH_ENDPOINT}/" + "{book_id}",
    response_model=schemas.BookWithReview,
    status_code=status.HTTP_200_OK,
    summary="Get book details",
    description="Get book details",
)
@cache(expire=60)
async def get_book(book_id: int, db: Session = Depends(get_db)):
    """
    Get book details, with reviews and rating

    :param book_id: Book ID
    :param db: Database session

    :return: Book details
    """

    results = await repository.get_book_with_review(book_id, db)
    return results
