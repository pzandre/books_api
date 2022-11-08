"""
Book Models
"""

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func

from database import Base


class BookReview(Base):
    """
    Book Review Model
    """

    __tablename__ = "book_reviews"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer)
    rating = Column(Integer)
    review = Column(String)
    date = Column(DateTime(timezone=True), server_default=func.now())
