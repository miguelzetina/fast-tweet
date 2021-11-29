from datetime import date
from typing import Optional
from uuid import UUID

from pydantic import Field, validator

from schemas.mixins import PasswordMixin, EmailMixin


class UserLogin(PasswordMixin, EmailMixin):
    pass


class UserData(EmailMixin):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    birth_date: Optional[date] = Field(default=None)


class User(UserData):
    id: UUID = Field(...)

    class Config:
        orm_mode = True


class UserRegister(UserData, PasswordMixin):
    pass
