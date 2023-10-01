from fastapi import FastAPI

from src.app.config import read_db_config
from src.app.endpoints import users
from src.app.utils.errors import app_error_handler
from src.app.utils.stubs import config


def app_factory() -> FastAPI:
    db_config = read_db_config('config.ini')
    app = FastAPI()
    app.include_router(users.router)
    app.add_exception_handler(Exception, app_error_handler)
    app.dependency_overrides[config] = lambda: db_config
    return app


if __name__ == '__main__':
    app_factory()
