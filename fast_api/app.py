from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select

from fast_api.database import get_session
from fast_api.models import User
from fast_api.schemas import (
    Message,
    UserInDB,
    UserList,
    UserPublic,
    UserSchema,
)

app = FastAPI()

database = []


@app.get('/', status_code=HTTPStatus.OK, response_model=Message, tags=['root'])
async def root():
    return {'message': 'Hello World'}


@app.post(
    '/users',
    status_code=HTTPStatus.CREATED,
    response_model=UserPublic,
    tags=['user'],
)
def create_user(user: UserSchema, session=Depends(get_session)):
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f'Username {user.username} already registered',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f'Email {user.email} already registered',
            )

    db_user = User(
        username=user.username, email=user.email, password=user.password
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get('/users/', response_model=UserList, tags=['user'])
async def get_users(session=Depends(get_session)):
    user = session.scalars(
        select(User)
    )
    return {'users': user}


@app.get('/users/{user_id}', response_model=UserPublic, tags=['user'])
def get_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'User with id {user_id} not found',
        )
    return database[user_id - 1]


@app.put('/users/{user_id}', response_model=UserPublic, tags=['user'])
def update_user(user_id: int, user: UserSchema):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'User with id {user_id} not found',
        )

    user_with_id = UserInDB(id=user_id, **user.model_dump())

    database[user_id - 1] = user_with_id

    return user_with_id


@app.delete(
    '/users/{user_id}',
    response_model=Message,
    status_code=HTTPStatus.OK,
    tags=['user'],
)
def delete_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'User with id {user_id} not found',
        )

    del database[user_id - 1]

    return {'message': f'User with id {user_id} deleted'}
