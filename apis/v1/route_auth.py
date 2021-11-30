from datetime import timedelta

from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status


from core.config import settings
from core.hashing import Hasher
from core.security import create_access_token
from db.repository.users import get_user_by_email, create_new_user
from db.session import get_db
from schemas.tokens import Token
from schemas.users import User, UserRegister
from jose import JWTError, jwt


router = APIRouter()


def authenticate_user(email: str, password: str, db: Session):
    user = get_user_by_email(db=db, email=email)
    if not user:
        return None
    if not Hasher.verify_password(password, user.hashed_password):
        return None
    return user


@router.post(
    path="/signup",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Register a user",
)
def signup(user: UserRegister = Body(...), db: Session = Depends(get_db)):
    """
    Signup

    This path operation register a user in the app

    Parameters:
        - Request body parameter
            - user: UserRegister
    Return a json with the basic user information:
        - user_id: UUID
        - email: EmailStr
        - first_name: str
        - last_name: str
        - birth_date: date
    """
    exists = get_user_by_email(db, user.email)
    if exists:
        raise HTTPException(status_code=400, detail="Email already registered")
    user_result = create_new_user(user, db)
    return user_result


@router.post(
    path="/login",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    summary="Login a user",
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user_from_token(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(email=username, db=db)
    if user is None:
        raise credentials_exception
    return user
