from pydantic import BaseModel
from typing import List, Literal


class MessageSchema(BaseModel):
    sender: str
    text: str
    time: str
    direction: Literal["in", "out"]


class BulkMessageSchema(BaseModel):
    messages: List[MessageSchema]


class HeaderSchema(BaseModel):
    name: str
    status: str
