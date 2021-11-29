from pydantic import BaseModel, Field, EmailStr


class PasswordMixin(BaseModel):
    password: str = Field(..., min_length=8, max_length=64)


class EmailMixin(BaseModel):
    email: EmailStr = Field(...)
