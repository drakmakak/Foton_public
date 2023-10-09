from pydantic import BaseModel





class MessageModel(BaseModel):
    user_id: int
    data: str
    sender: int