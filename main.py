from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from fastapi import FastAPI
from typing import Optional


app = FastAPI()


class UserBase(BaseModel):
    user_id: UUID = Field(...)
    email: EmailStr = Field(...)


class UserLogin(UserBase):
    password: str = Field(..., min_length=8, max_length=64)


class User(UserBase):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    birth_date: Optional[date] = Field(default=None)


class Tweet(BaseModel):
    tweet_id: UUID = Field(..., alias="Tweet id")
    content: str = Field(..., min_length=1, max_length=280, example="My first tweet!")
    created_at: datetime = Field(default=datetime.now())
    updated_at: Optional[datetime] = Field(default=None)
    by: User = Field(..., alias="User")


@app.get("/")
def home():
    return {"Twitter API": "Hello World"}
