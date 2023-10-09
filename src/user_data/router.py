from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.database import get_async_session

router = APIRouter(
    prefix='/user',
    tags=['User']
)


@router.get("/")
async def get_users(username:str, session: AsyncSession = Depends(get_async_session)):
    data = select(User.email, User.id).where(User.email == username)
    res = await session.execute(data)
    users = {}
    for i in res.all():
        print(i)
        users[i[0]] = i[1]

    return users
