from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from apis.v1.route_auth import get_current_user_from_token
from db.repository.users import (
    deactivate_user,
    follow_a_user,
    following_user,
    get_all_users,
    get_user,
    unfollow_a_user,
    update_data_user,
)
from db.session import get_db
from schemas.users import User, UserBasicData, UserDetail
from schemas.mixins import Detail
from db.models.users import User as UserModel

router = APIRouter()


@router.get(
    path="",
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary="Show all users",
)
def show_all_users(db: Session = Depends(get_db)):
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
    return get_all_users(db)


@router.get(
    path="/me",
    response_model=UserDetail,
    status_code=status.HTTP_200_OK,
    summary="Show current user data",
)
def me(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user_from_token),
):
    return current_user


@router.get(
    path="/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Show a user",
    responses={404: {"model": Detail}},
)
def show_user(user_id: str, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete(
    path="/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a user",
    responses={403: {"model": Detail}, 404: {"model": Detail}},
)
def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user_from_token),
):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="You are not authorized")

    if not get_user(db, user_id):
        raise HTTPException(status_code=404, detail="User not found")

    deactivate_user(db, user_id)


@router.put(
    path="/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Update a user",
    responses={403: {"model": Detail}, 404: {"model": Detail}},
)
def update_user(
    user_id: str,
    user_data: UserBasicData = Body(...),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user_from_token),
):
    if str(current_user.id) != user_id or not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="You are not authorized")

    if not get_user(db, user_id):
        raise HTTPException(status_code=404, detail="User not found")

    return update_data_user(db, user_id, user_data.dict())


@router.post(
    path="/{user_id}/follow",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Follow a user",
    responses={400: {"model": Detail}, 404: {"model": Detail}},
)
def follow_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user_from_token),
):
    if str(current_user.id) == user_id:
        raise HTTPException(status_code=400, detail="You cannot follow you")

    if not get_user(db, user_id):
        raise HTTPException(status_code=404, detail="User not found")

    user_is_followed = following_user(current_user, user_id)
    if user_is_followed:
        return

    follow_a_user(db, current_user, user_id)


@router.delete(
    path="/{user_id}/follow",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Unfollow a user",
    responses={400: {"model": Detail}, 404: {"model": Detail}},
)
def unfollow_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user_from_token),
):
    if str(current_user.id) == user_id:
        raise HTTPException(status_code=400, detail="You cannot unfollow you")

    if not get_user(db, user_id):
        raise HTTPException(status_code=404, detail="User not found")

    user_is_followed = following_user(current_user, user_id)
    if not user_is_followed:
        return

    unfollow_a_user(db, current_user, user_id)
