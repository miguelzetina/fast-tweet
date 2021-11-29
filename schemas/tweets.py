from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from schemas.users import User


class Tweet(BaseModel):
    tweet_id: UUID = Field(..., alias="Tweet id")
    content: str = Field(..., min_length=1, max_length=280, example="My first tweet!")
    created_at: datetime = Field(default=datetime.now())
    updated_at: Optional[datetime] = Field(default=None)
    by: User = Field(..., alias="User")
