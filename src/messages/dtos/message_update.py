from pydantic import BaseModel


class MessageUpdateDTO(BaseModel):
    name: str
