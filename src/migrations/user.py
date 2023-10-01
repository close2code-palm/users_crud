import asyncio

import asyncpg
from asyncpg import Connection

from src.app.config import read_db_config


async def create_users():
    create_user_table_q = """CREATE TABLE IF NOT EXISTS users(
    user_id SMALLSERIAL PRIMARY KEY,
    email TEXT,
    password TEXT,
    username TEXT
    );"""
    con = await asyncpg.connect(read_db_config('config.ini').dsn)
    await con.execute(create_user_table_q)
    await con.close()


if __name__ == '__main__':
    asyncio.run(create_users())
