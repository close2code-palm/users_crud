import asyncpg
from asyncpg import Connection
from fastapi import Depends, HTTPException
from starlette import status

from src.app.schemas.config import DbConfig
from src.app.schemas.user import UserCreateModel, UserUpdateModel, UserDBModel, OrderingType, Ordering
from src.app.utils.stubs import config


class UserRepo:
    def __init__(self, conn: Connection):
        self._conn = conn

    async def remove_by_id(self, user_id: int):
        rbi_q = """DELETE FROM users WHERE user_id = $1;"""
        await self._conn.execute(rbi_q, user_id)

    async def check_user_email(self, email: str):
        cue_q = """SELECT user_id FROM users WHERE email = $1;"""
        res = await self._conn.fetchval(cue_q, email)
        return bool(res)

    async def check_username(self, username: str):
        cu_q = """SELECT user_id FROM users WHERE username = $1;"""
        res = await self._conn.fetchval(cu_q, username)
        return bool(res)

    async def create_user(self, user: UserCreateModel) -> int:
        cu_q = """INSERT INTO users(email, password, username)
        VALUES ($1, $2, $3) RETURNING user_id;"""
        return await self._conn.fetchval(
            cu_q, user.email, user.password, user.username)

    async def get_user_by_id(self, user_id: int):
        gubi_q = """SELECT * FROM users WHERE user_id = $1;"""
        user_data = await self._conn.fetchrow(gubi_q, user_id)
        if not user_data:
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
        return dict(user_data)

    async def update_user(self, user: UserUpdateModel, user_id: int):
        user_data = user.model_dump(exclude_none=True)
        user_in_db = await self.get_user_by_id(user_id)
        for k in user_data:
            user_in_db[k] = user_data[k]
        uu_q = """UPDATE users SET email = $1, password = $2,
        username = $3 WHERE user_id = $4;"""
        user = UserDBModel(**user_in_db)
        await self._conn.execute(
            uu_q, user.email, user.password,
            user.username, user.user_id)
        return user_in_db

    async def get_all_users(
            self,
            email_filter: str | None,
            order_by: Ordering | None
    ):
        ef_q = f""" WHERE email LIKE '%{email_filter}%'""" if email_filter else ""
        ob_q = f""" ORDER BY {order_by.value}""" if order_by else ""
        gau_q = f"""SELECT * FROM users{ef_q}{ob_q};"""
        return await self._conn.fetch(gau_q)


async def session(db_config: DbConfig = Depends(config)):
    con: Connection = await asyncpg.connect(db_config.dsn)
    try:
        yield UserRepo(con)
    finally:
        await con.close()

