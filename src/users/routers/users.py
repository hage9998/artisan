from sqlalchemy.orm import Session
from src.database.session import get_db
from src.users.dtos.create_user import UserCreateDTO, UserResponseDTO
from fastapi import APIRouter, Depends, HTTPException

from src.users.dtos.get_user import GetUserResponseDTO
from src.users.services.user import get_user_by_email, create_new_user

router = APIRouter(prefix="/users")


@router.post("/", response_model=UserResponseDTO)
async def create_user(create_user: UserCreateDTO, db: Session = Depends(get_db)):
    new_user = create_new_user(db=db, user=create_user)

    return new_user


# @router.get("/users", response_model=GetUserResponseDTO)
# async def get_user_by_email(create_user: UserCreateDTO, db: Session = Depends(get_db)):
#     return get_user_by_email(db=db, email="bla")
