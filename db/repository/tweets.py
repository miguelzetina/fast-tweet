from sqlalchemy.orm import Session

from schemas.tweets import TweetCreate
from db.models.tweets import Tweet
from db.models.users import User


def create_new_tweet(db: Session, tweet: TweetCreate, user: User):
    new_tweet = Tweet(content=tweet.content, user=user)
    db.add(new_tweet)
    db.commit()
    db.refresh(new_tweet)
    return new_tweet
