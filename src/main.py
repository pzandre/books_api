"""
FastAPI app
"""

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from starlette.config import Config

from books.router import book_router
from database import Base, engine

config = Config(".env")

ENVIRONMENT = config("ENVIRONMENT", default="local")
SHOW_DOCS_ENVIRONMENT = ("local",)

app_configs = {"title": "Books API"}

if ENVIRONMENT not in SHOW_DOCS_ENVIRONMENT:
    app_configs["openapi_url"] = None

app = FastAPI(**app_configs)

FastAPICache().init(InMemoryBackend(), prefix="book_api")

Base.metadata.create_all(bind=engine)

app.include_router(book_router)
