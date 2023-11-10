from fastapi import APIRouter, Depends, Response

from app.core.exceptions import UserAlreadyExistsException
from app.users.schemas import User
from app.users.models import users
from app.users.services import (
    create_user_id,
    get_current_user_id,
    get_user_name
)


router = APIRouter()


@router.post("/login")
async def login_user(
        response: Response,
        user: User,
) -> User:
    if user.id:
        if user.id in users:
            raise UserAlreadyExistsException
    else:
        user.id = create_user_id()

    users[user.id] = user.name

    response.set_cookie(
        "example_user_id",
        str(user.id),
        path="/",
    )

    return user


@router.post("/logout")
async def logout_user(
        response: Response
) -> None:
    response.delete_cookie("example_user_id")


@router.get("/current_user")
async def get_current_user(
        current_user_id: int = Depends(get_current_user_id)
) -> User:
    return User(
        name=await get_user_name(current_user_id),
        id=current_user_id
    )


print('init users routers')
