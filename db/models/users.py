import uuid
from sqlalchemy import Boolean, Column, String, Date, DateTime, func
from sqlalchemy.dialects.postgresql import UUID


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
