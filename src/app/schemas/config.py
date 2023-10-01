import configparser

from pydantic import PostgresDsn
from pydantic.dataclasses import dataclass


@dataclass
class DbConfig:
    host: str
    port: int
    user: str
    password: str
    db: str

    @property
    def dsn(self) -> PostgresDsn:
        port = f':{self.port}' if self.port else ''
        return (f'postgresql://{self.user}:{self.password}'
                f'@{self.host}{port}/{self.db}')
