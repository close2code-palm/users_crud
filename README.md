To start the application:

1. Create postgres database, replace `config.ini.template`
   with `config.ini` and fill the parameters for connection
2. Make venv(from `pyproject.toml`) with poetry or with pip
   (you will need asyncpg, fastapi, pydantic[email] and some kind of ASGI Web server)
4. To run migrations, type `python -m src.migrations.user`
5. To run server, use app factory according to your server documentation:
   for example `uvicorn --factory src.app.main:app_factory`
6. After started, documentation will be available at \<Running server>/docs
