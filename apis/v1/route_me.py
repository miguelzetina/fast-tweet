from fastapi import APIRouter, Depends
from starlette import status

from apis.v1.route_auth import get_current_user_from_token
from db.models.users import User


router = APIRouter()


@router.get(
    path="",
    tags=["Home"],
    status_code=status.HTTP_200_OK,
    summary="Show all tweets",
)
def home(current_user: User = Depends(get_current_user_from_token)):
    print(current_user.id)
    return {"Twitter API": "Hello World"}
