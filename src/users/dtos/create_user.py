from src.users.dtos.get_user import UserBase


class UserCreateDTO(UserBase):
    password: str


class UserResponseDTO(UserBase):
    id: str

    class Config:
        orm_mode = True
