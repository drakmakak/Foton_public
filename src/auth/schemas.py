from typing import Optional

from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    username:str
    email: str


class UserCreate(schemas.BaseUserCreate):
    username:str
    email: str

class UserUpdate(schemas.BaseUserUpdate):
    username: Optional[str] = None