from fastapi import HTTPException
from passlib.hash import bcrypt
from sqlalchemy.orm import Session
from src.users.dtos.create_user import UserCreateDTO
from src.users.models.users import User


def create_new_user(db: Session, user: UserCreateDTO):
    hashed_password = bcrypt.hash(user.password)
    new_user = User(name=user.name, email=user.email, password=hashed_password)

    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()
