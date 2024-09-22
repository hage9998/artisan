from pydantic import BaseModel


class MessageAnswerDTO(BaseModel):
    sender: str
    message: str
    createdAt: str
    id: str
