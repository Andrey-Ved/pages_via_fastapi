from pydantic import BaseModel


class User(BaseModel):
    name: str
    id: int | None = None


print('init users schemas')
