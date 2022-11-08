"""
Books repository
"""

import asyncio
from fastapi import Depends, HTTPException, status
import requests
from sqlalchemy import extract, select
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

import models
import schemas
from constants import EXTERNAL_API_URL, MONTHS, PROJECT_URL
from database import get_db


async def get_books_by_title(search: str, page: int) -> list:
    """
    This function is used to get books by title from external API

    :param search: search string
    :param page: page number

    :return: list of books
    """

    queryparam_dict = {"search": requests.utils.quote(search), "page": page}
    book_list = requests.get(EXTERNAL_API_URL, params=queryparam_dict)
    if not book_list.status_code == status.HTTP_200_OK:
        raise HTTPException(status_code=book_list.status_code, detail=book_list.json())

    results = book_list.json()
    if results["next"]:
        results["next"] = results["next"].replace(EXTERNAL_API_URL, f"{PROJECT_URL}/book")
    if results["previous"]:
        results["previous"] = results["previous"].replace(EXTERNAL_API_URL, f"{PROJECT_URL}/book")
    results["books"] = results.pop("results")
    return results


async def get_book(book_id: int) -> dict:
    """
    This function is used to get book by id from external API

    :param book_id: book id

    :return: book data
    """

    return requests.get(EXTERNAL_API_URL + str(book_id)).json()


async def create_review(book_id: int, book_review: schemas.BaseBookReview, db: Session = Depends(get_db)):
    """
    This function is used to create book review

    :param book_id: book id
    :param book_review: book review data
    :param db: database session

    :return: book review data
    """

    review = models.BookReview(**book_review.dict(), book_id=book_id)
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


async def get_book_avg_rating(book_id: int, db: Session = Depends(get_db)):
    """
    This function is used to get book average rating

    :param book_id: book id
    :param db: database session

    :return: book reviews and average rating
    """

    avg_rating = select([func.avg(models.BookReview.rating)]).where(models.BookReview.book_id == book_id)
    reviews = select([models.BookReview.review]).where(models.BookReview.book_id == book_id)
    rating_result = db.execute(avg_rating).scalar()
    review_result = db.execute(reviews).fetchall()
    return review_result, rating_result


async def gather_book_and_rating(book_id: int, db: Session = Depends(get_db)):
    """
    This function is used to get book data and average rating

    :param book_id: book id
    :param db: database session

    :return: book data and average rating
    """

    await asyncio.gather(get_book_avg_rating(book_id, db), get_book(book_id))


async def get_book_with_review(book_id: int, db: Session = Depends(get_db)):
    """
    This function is used to get book data and reviews
    
    :param book_id: book id
    :param db: database session
    
    :return: book data and reviews
    """
    
    (reviews, rating), book_data = await asyncio.gather(get_book_avg_rating(book_id, db), get_book(book_id))
    query_dict = {
        "book_id": book_id,
        "reviews": [instance[0] for instance in reviews if reviews],
        "rating": rating or 0.0
    }
    book_data.update(query_dict)
    return book_data    


async def get_top_rated_books(limit:int = 10, db: Session = Depends(get_db)):
    """
    This function is used to get top rated books
    
    :param limit: number of books to return
    :param db: database session
    
    :return: list of top rated books
    """

    top_rated_books = select(
        [models.BookReview.book_id, func.avg(models.BookReview.rating)]
        ).group_by(models.BookReview.book_id).order_by(func.avg(models.BookReview.rating).desc()).limit(limit)
    rating_result = db.execute(top_rated_books)

    query_dict = {}
    for row in rating_result:
        query_dict[row.book_id] = {"book_id": row.book_id, "rating": row.avg, "reviews": []}

    reviews = select([models.BookReview.book_id, models.BookReview.review]).where(models.BookReview.book_id.in_(query_dict.keys()))
    review_result = db.execute(reviews)

    for row in review_result:
        query_dict[row.book_id]["reviews"].append(row.review)
    
    book_results = await asyncio.gather(*[get_book(book_id) for book_id in query_dict.keys()])

    for book_result in book_results:
        book_result['reviews'] = query_dict[book_result['id']]['reviews']
        book_result['rating'] = query_dict[book_result['id']]['rating']
    
    return book_results


async def get_monthly_rating(book_id: int, db: Session = Depends(get_db)):
    """
    This function is used to get monthly rating of a book

    :param book_id: book id
    :param db: database session

    :return: monthly rating of a book
    """

    book_rating_by_month = select(
        [extract('month', models.BookReview.date).label('month'), func.avg(models.BookReview.rating)]
    ).group_by("month").where(models.BookReview.book_id == book_id).order_by("month")
    rating_result = db.execute(book_rating_by_month)

    query_dict = {"book_id": book_id, "ratings": []}
    for row in rating_result:
        query_dict["ratings"].append({"month": MONTHS[row.month], "rating": row.avg})

    return query_dict
