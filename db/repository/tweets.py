from sqlalchemy.orm import Session
from sqlalchemy import func, text

from schemas.tweets import TweetCreate
from db.models.tweets import Tweet
from db.models.users import User


def create_new_tweet(db: Session, tweet: TweetCreate, user: User):
    new_tweet = Tweet(content=tweet.content, user=user)
    db.add(new_tweet)
    db.commit()
    db.refresh(new_tweet)
    return new_tweet


def get_tweet(db: Session, tweet_id: str):
    return db.query(Tweet).filter(Tweet.id == tweet_id).first()


def deactivate_tweet(db: Session, tweet_id: str):
    tweet = db.query(Tweet).filter(Tweet.id == tweet_id).first()
    tweet.is_active = False
    db.commit()
    db.refresh(tweet)


def update_content_tweet(db: Session, tweet: Tweet, content: str):
    tweet.content = content
    tweet.updated_at = func.now()  # TODO Find way of update field automatically
    db.commit()
    db.refresh(tweet)
    return tweet


def get_all_tweets(db: Session):
    return db.query(Tweet).all()


def mark_tweet_as_liked(db, tweet: Tweet, user: User):
    liked_tweets = [str(it.id) for it in user.liked_tweets]
    if str(tweet.id) in liked_tweets:
        return
    user.liked_tweets.append(tweet)
    db.commit()


def mark_tweet_as_unliked(db, tweet: Tweet, user: User):
    liked_tweets = [str(it.id) for it in user.liked_tweets]
    if str(tweet.id) not in liked_tweets:
        return
    user.liked_tweets.remove(tweet)
    db.commit()
