import logging.config

from fastapi import FastAPI

from config.settings import settings
from core.exception import InvalidCategoryInputError, InvalidUrlInputError
from core.exception_handler import exception_404_handler
from routers import category_routers, product_routers, streamer_routers

logging.config.dictConfig(settings.LOGGING_CONFIG)

app = FastAPI(title=settings.PROJECT_NAME)

app.add_exception_handler(InvalidCategoryInputError, exception_404_handler)
app.add_exception_handler(InvalidUrlInputError, exception_404_handler)

app.include_router(streamer_routers, tags=["Streamers"], prefix="/api/streamers")
app.include_router(product_routers, tags=["Products"], prefix="/api/products")
app.include_router(category_routers, tags=["Categories"], prefix="/api/categories")
