import datetime
from pydantic import BaseModel, Field


class GetAllMessagesDTO(BaseModel):
    sender: str
    message: str
    created_at: datetime.datetime = Field(serialization_alias="createdAt")
    id: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
