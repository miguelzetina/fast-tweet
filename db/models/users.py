import uuid
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Date,
    ForeignKey,
    String,
    Table,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.base_class import Base
from db.models.tweets import Tweet


class User(Base):
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=uuid.uuid4,
    )
    email = Column(String, nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    first_name = Column(String(256), nullable=False)
    last_name = Column(String(256), nullable=False)
    birth_date = Column(Date, nullable=True)
    created_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        server_onupdate=func.now(),
    )
    tweets = relationship(
        "Tweet", foreign_keys="[Tweet.user_id]", back_populates="user"
    )
    following = relationship(
        "User",
        lambda: user_following,
        primaryjoin=lambda: User.id == user_following.c.user_id,
        secondaryjoin=lambda: User.id == user_following.c.following_id,
        lazy="dynamic",
    )
    followers = relationship(
        "User",
        lambda: user_following,
        primaryjoin=lambda: User.id == user_following.c.following_id,
        secondaryjoin=lambda: User.id == user_following.c.user_id,
        lazy="dynamic",
    )

    liked_tweets = relationship(
        "Tweet",
        lambda: user_like_tweet,
        primaryjoin=lambda: User.id == user_like_tweet.c.user_id,
        secondaryjoin=lambda: Tweet.id == user_like_tweet.c.tweet_id,
        lazy="dynamic",
        backref="likes",
    )

    @property
    def following_count(self):
        return self.following.count()

    @property
    def followers_count(self):
        return self.followers.count()


user_like_tweet = Table(
    "user_like_tweet",
    Base.metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey("user.id"), primary_key=True),
    Column("tweet_id", UUID(as_uuid=True), ForeignKey("tweet.id"), primary_key=True),
)


user_following = Table(
    "user_following",
    Base.metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey(User.id), primary_key=True),
    Column("following_id", UUID(as_uuid=True), ForeignKey(User.id), primary_key=True),
)
