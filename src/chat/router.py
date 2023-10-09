from typing import Dict, List

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy import select, exists, update, and_, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import Message
from src.database import get_async_session, async_session_maker

router = APIRouter(

)


async def add_data(user_id: int, sender: int, message: str):
    async with async_session_maker() as session:
        data = Message(
            user_id=user_id,
            sender=sender,
            data=message,
        )
        session.add(data)
        await session.commit()
        await session.refresh(data)



class ConnectManager:
    def __init__(self):
        self.active_users: Dict[int, WebSocket] = {}

    def connect(self, user_id, websocket):
        self.active_users[user_id] = websocket

    def disconnect(self, user_id):
        del self.active_users[user_id]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)


async def test(user_id: int, websocket: WebSocket):
    async with async_session_maker() as session:
        query = select(Message.sender, Message.data).where(Message.user_id == user_id)
        res = await session.execute(query)
        for i in res.all():
            await manager.send_personal_message(f'{i[0]}:{i[1]}', websocket)
            stmt = delete(Message).where(and_(Message.user_id == user_id, Message.data == i[1]))
            await session.execute(stmt)
            await session.commit()


manager = ConnectManager()


@router.websocket("/protected-route/ws/{user_id}")
async def websocket_endpoint(user_id: int, websocket: WebSocket):
    await websocket.accept()
    manager.connect(user_id, websocket)
    await test(user_id, websocket)
    try:
        await websocket.send_text('welcome')
        while True:

            data = await websocket.receive_json()
            if data['user_id'] in manager.active_users:
                await manager.send_personal_message(data['data'], manager.active_users[data['user_id']])
            else:
                await add_data(data['user_id'], user_id, data['data'])
    except WebSocketDisconnect:
        manager.disconnect(user_id)
