from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status
from typing import List

from db.repository.tweets import get_all_tweets
from db.session import get_db
from schemas.tweets import Tweet

router = APIRouter()


@router.get(
    path="",
    response_model=List[Tweet],
    status_code=status.HTTP_200_OK,
    summary="Show all tweets",
)
def home(db: Session = Depends(get_db)):
    return get_all_tweets(db)
