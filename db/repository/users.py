from sqlalchemy.orm import Session

from schemas.users import UserRegister
from db.models.users import User
from core.hashing import Hasher


def create_new_user(user: UserRegister, db: Session):
    new_user = User(
        email=user.email.lower(),
        first_name=user.first_name,
        last_name=user.last_name,
        hashed_password=Hasher.get_password_hash(user.password),
        is_active=True,
        is_superuser=False,
        birth_date=user.birth_date,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email.lower()).first()
