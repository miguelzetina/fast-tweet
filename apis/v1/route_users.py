from typing import List

from fastapi import APIRouter
from starlette import status

from schemas.users import User

router = APIRouter()


@router.get(
    path="",
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


@router.get(
    path="/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Show a user",
    tags=["Users"],
)
def show_user():
    pass


@router.delete(
    path="/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a user",
    tags=["Users"],
)
def delete_user():
    pass


@router.put(
    path="/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Update a user",
    tags=["Users"],
)
def update_user():
    pass
