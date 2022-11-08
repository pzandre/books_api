"""
FastAPI app
"""

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend

from database import Base, engine
from routers import book_router

app = FastAPI()

FastAPICache().init(InMemoryBackend(), prefix="book_api")

Base.metadata.create_all(bind=engine)

app.include_router(book_router)
