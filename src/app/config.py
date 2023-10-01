import configparser

from src.app.schemas.config import DbConfig


def read_db_config(cfg_path: str):
    """Db config factory.

    Used in migrations and app connections.
    """
    cfg = configparser.ConfigParser()
    cfg.read(cfg_path)

    db = cfg['pgsql']

    return DbConfig(
        host=db.get('DB_HOST'),
        port=db.getint('DB_PORT'),
        user=db.get('DB_USER'),
        password=db.get('DB_PWD'),
        db=db.get('DB_NAME')
    )
