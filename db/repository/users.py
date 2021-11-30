from sqlalchemy.orm import Session

from schemas.users import UserRegister
from db.models.users import User, user_following
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


def deactivate_user(db: Session, user_id: str):
    user = db.query(User).filter(User.id == user_id).first()
    user.is_active = False
    db.commit()
    db.refresh(user)


def get_all_users(db: Session):
    return db.query(User).all()


def get_user(db: Session, user_id: str):
    return db.query(User).filter(User.id == user_id).first()


def update_data_user(db: Session, user_id: str, user_data: dict):
    user = db.query(User).filter(User.id == user_id)
    user.update(user_data)
    db.commit()
    db.refresh(user.first())
    return user.first()


def follow_a_user(db: Session, user: User, user_id: str):
    user_to_follow = db.query(User).filter(User.id == user_id).first()
    user.following.append(user_to_follow)
    db.commit()


def unfollow_a_user(db: Session, user: User, user_id: str):
    user_to_follow = db.query(User).filter(User.id == user_id).first()
    user.following.remove(user_to_follow)
    db.commit()


def following_user(user: User, user_id: str):
    return user.following.filter(user_following.c.following_id == user_id).first()
