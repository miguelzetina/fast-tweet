from fastapi import FastAPI

from apis.base import api_router
from db.session import engine
from db.base import Base
from core.config import settings

Base.metadata.create_all(bind=engine)


def include_router(app):
    app.include_router(api_router)


def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    Base.metadata.create_all(bind=engine)
    include_router(app)
    return app


app = start_application()
