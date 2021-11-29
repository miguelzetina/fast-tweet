from fastapi import APIRouter
from starlette import status

from schemas.tweets import Tweet

router = APIRouter()


@router.post(
    path="",
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
