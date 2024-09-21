from src.users.dtos.user_base import UserBase


class GetUserResponseDTO(UserBase):
    id: str

    class Config:
        orm_mode = True
