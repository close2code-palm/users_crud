from fastapi import APIRouter, Depends, HTTPException, Query
from starlette import status

from src.app.schemas.user import UserCreateModel, UserUpdateModel, Ordering
from src.app.services.db import UserRepo, session

router = APIRouter(prefix='/users')


@router.get('/')
async def list_users(
        repo: UserRepo = Depends(session),
        email: str | None = Query(None),
        order_by: Ordering | None = Query(None)
):
    return await repo.get_all_users(email, order_by)


@router.post('/')
async def register_user(user: UserCreateModel, repo: UserRepo = Depends(session)):
    if await repo.check_user_email(user.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Email already exists.')
    if user.username and await repo.check_username(user.username):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Username already exists.')
    uid = await repo.create_user(user)
    return await repo.get_user_by_id(uid)


@router.get('/{user_id}')
async def get_concrete_user(user_id: int, repo: UserRepo = Depends(session)):
    return await repo.get_user_by_id(user_id)


@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remove_user(user_id: int, repo: UserRepo = Depends(session)):
    await repo.remove_by_id(user_id)


@router.patch('/user_id')
async def update_user(
        user: UserUpdateModel,
        user_id: int,
        repo: UserRepo = Depends(session)
):
    if user.email and await repo.check_user_email(user.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Email already exists.')

    if user.username and await repo.check_username(user.username):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Username already exists.')

    return await repo.update_user(user, user_id)
