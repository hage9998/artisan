from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.auth.services.auth import get_current_user, sign_in
from src.database.session import get_db
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from src.messages.dtos.message_answer import MessageAnswerDTO
from src.messages.enums.sender_enum import SenderEnum
from src.messages.services.websocket_manager import manager
from src.messages.services.messages import get_all_messages_by_user_id, save_message

router = APIRouter(prefix="/auth")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    response = sign_in(
        db=db, user_email=form_data.username, user_password=form_data.password
    )

    return {
        "accessToken": response["access_token"],
        "userId": response["user_id"],
        "tokenType": "bearer",
    }
