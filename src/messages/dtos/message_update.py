from pydantic import BaseModel


class MessageUpdateDTO(BaseModel):
    message: str
