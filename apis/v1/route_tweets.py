from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session
from starlette import status

from apis.v1.route_auth import get_current_user_from_token
from db.repository.tweets import create_new_tweet
from schemas.tweets import Tweet, TweetCreate
from db.models.users import User
from db.session import get_db

router = APIRouter()


@router.post(
    path="",
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary="Post a tweet",
    tags=["Tweets"],
)
def post_tweet(
    tweet: TweetCreate = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
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
    return create_new_tweet(db, tweet, current_user)


@router.get(
    path="/{tweet_id}",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Show a tweet",
    tags=["Tweets"],
)
def show_tweet():
    pass


@router.delete(
    path="/{tweet_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a tweet",
    tags=["Tweets"],
)
def delete_tweet():
    pass


@router.put(
    path="/{tweet_id}",
    status_code=status.HTTP_200_OK,
    summary="Update a tweet",
    tags=["Tweets"],
)
def update_tweet():
    pass
