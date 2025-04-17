from http import HTTPStatus

from fastapi import FastAPI, HTTPException

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
def create_user(user: UserSchema):
    user_with_id = UserInDB(id=len(database) + 1, **user.model_dump())

    database.append(user_with_id)

    return user_with_id


@app.get('/users/', response_model=UserList, tags=['user'])
async def get_users():
    return {'users': database}


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
