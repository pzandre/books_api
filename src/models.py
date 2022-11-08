"""
Book Models
"""

from sqlalchemy import Column, DateTime, Integer, SmallInteger, String
from sqlalchemy.orm import validates
from sqlalchemy.sql import func

from src.database import Base


class BookReview(Base):
    """
    Book Review Model
    """

    __tablename__ = "book_reviews"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, nullable=False)
    rating = Column(SmallInteger, nullable=False)
    review = Column(String(length=500), nullable=False)
    date = Column(DateTime(timezone=True), server_default=func.now())

    @validates("rating")
    def validate_name(self, key, value):
        if not 0 <= value <= 5:
            raise ValueError("Rating must be between 0 and 5")
        return value
