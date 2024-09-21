from pydantic import BaseModel
from datetime import datetime


class MessageAnswerDTO(BaseModel):
    sender: str
    message: str
    createdAt: str
