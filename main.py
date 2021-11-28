import uuid
from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from fastapi import status, Body, FastAPI
from typing import List, Optional


app = FastAPI()


class PasswordMixin(BaseModel):
    password: str = Field(..., min_length=8, max_length=64)


class EmailMixin(BaseModel):
    email: EmailStr = Field(...)


class UserLogin(PasswordMixin, EmailMixin):
    pass


class UserData(EmailMixin):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    birth_date: Optional[date] = Field(default=None)


class User(UserData):
    user_id: UUID = Field(...)


class UserRegister(User):
    pass


class UserInDB(UserRegister):
    hashed_password: str = Field(...)


class Tweet(BaseModel):
    tweet_id: UUID = Field(..., alias="Tweet id")
    content: str = Field(..., min_length=1, max_length=280, example="My first tweet!")
    created_at: datetime = Field(default=datetime.now())
    updated_at: Optional[datetime] = Field(default=None)
    by: User = Field(..., alias="User")


@app.get(
    path="/",
    # response_model=List[Tweet],
    tags=["Tweets"],
    status_code=status.HTTP_200_OK,
    summary="Show all tweets",
)
def home():
    return {"Twitter API": "Hello World"}


@app.post(
    path="/auth/signup",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Register a user",
    tags=["Auth"],
)
def signup(user: UserRegister = Body(...)):
    """
    Signup

    This path operation register a user in the app

    Parameters:
        - Request body parameter
            - user: UserRegister
    Return a json with the basic user information:
        - user_id: UUID
        - email: EmailStr
        - first_name: str
        - last_name: str
        - birth_date: date
    """
    user_result = User(**user.dict(), user_id=uuid.uuid4())
    return user_result


@app.post(
    path="/auth/login",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Login a user",
    tags=["Auth"],
)
def login():
    pass


# Users
@app.get(
    path="/users",
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary="Show all users",
    tags=["Users"],
)
def show_all_users():
    """
    List users

    This path operation show all users in the app

    Parameters:
        -
    Return a json list with the basic user information:
        - user_id: UUID
        - email: EmailStr
        - first_name: str
        - last_name: str
        - birth_date: date
    """
    pass


@app.get(
    path="/users/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Show a user",
    tags=["Users"],
)
def show_user():
    pass


@app.delete(
    path="/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a user",
    tags=["Users"],
)
def delete_user():
    pass


@app.put(
    path="/users/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Update a user",
    tags=["Users"],
)
def update_user():
    pass


# Tweets
@app.post(
    path="/tweet",
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary="Post a tweet",
    tags=["Tweets"],
)
def post_tweet():
    """
    Post a tweet

    This path operation post a tweet in the app

    Parameters:
        - Request body parameter
            - tweet: Tweet

    Returns a json with the basic tweet information:
        tweet_id: UUID
        content: str
        created_at: datetime
        updated_at: Optional[datetime]
        by: User
    """
    pass


@app.get(
    path="/tweet/{tweet_id}",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Show a tweet",
    tags=["Tweets"],
)
def show_tweet():
    pass


@app.delete(
    path="/tweet/{tweet_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a tweet",
    tags=["Tweets"],
)
def delete_tweet():
    pass


@app.put(
    path="/tweet/{tweet_id}",
    status_code=status.HTTP_200_OK,
    summary="Update a tweet",
    tags=["Tweets"],
)
def update_tweet():
    pass
