from http import HTTPStatus

from fastapi import FastAPI

from fast_api.schemas import Message,UserSchema, UserPublic

app = FastAPI()


@app.get('/', status_code=HTTPStatus.OK, response_model=Message, tags=['root'])
async def root():
    return {'message': 'Hello World'}

@app.post('/user', status_code=HTTPStatus.CREATED, response_model=UserPublic, tags=['user'])
def create_user(user: UserSchema):
    return user

