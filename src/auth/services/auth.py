import uuid
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from src.database.session import get_db
from src.users.models.users import User
from fastapi.security import OAuth2PasswordBearer
import secrets


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.auth_token == token).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid authentication token")

    return user


def verify_password(plain_password, hashed_password):
    return bcrypt.verify(plain_password, hashed_password)


def sign_in(db: Session, user_email: str, user_password: str):
    user = db.query(User).filter(User.email == user_email).first()

    if not user or not verify_password(user_password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    user.auth_token = generate_auth_token()
    db.commit()

    return {"access_token": user.auth_token, "user_id": user.id}


def generate_auth_token():
    return str(uuid.uuid4())
