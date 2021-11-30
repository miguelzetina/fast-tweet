from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from schemas.users import User


class Tweet(BaseModel):
    id: UUID
    content: str
    created_at: datetime
    updated_at: datetime
    user: User

    class Config:
        orm_mode = True


class TweetCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=250, example="My first tweet!")
