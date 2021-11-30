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
        backref="followers",
        lazy="dynamic",
    )


user_following = Table(
    "user_following",
    Base.metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey(User.id), primary_key=True),
    Column("following_id", UUID(as_uuid=True), ForeignKey(User.id), primary_key=True),
)
