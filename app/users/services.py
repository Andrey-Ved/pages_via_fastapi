from time import time
from fastapi import Request

from app.users.models import users
from app.core.exceptions import (
    UserIdAbsentException,
    UserIsNotPresentException,
)


def create_user_id() -> int:
    user_id = int(time() * 1000)

    while user_id in users:
        user_id += 1

    return user_id


async def get_current_user_id(
        request: Request
) -> int:

    user_id = int(request.cookies.get("example_user_id", '0'))

    if not user_id:
        raise UserIdAbsentException

    return user_id


async def get_user_name(
        user_id: int) -> str:

    if user_id not in users:
        raise UserIsNotPresentException

    return users[user_id]


print('init users services')
