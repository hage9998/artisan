from sqlalchemy.orm import Session
from src.auth.services.auth import get_current_user
from src.database.session import get_db
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from src.messages.dtos.message_answer import MessageAnswerDTO
from src.messages.enums.sender_enum import SenderEnum
from src.messages.services.websocket_manager import manager
from src.messages.services.messages import get_all_messages_by_user_id, save_message

router = APIRouter(prefix="/messages")


@router.get("/user/{user_id}")
def get_all_messages_by_user(
    user_id: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    return get_all_messages_by_user_id(db=db, user_id=user_id)


@router.websocket("/ws/chat/{user_id}")
async def websocket_endpoint(
    websocket: WebSocket, user_id: str, db: Session = Depends(get_db)
):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()

            user_message = save_message(
                db, user_id=user_id, message=data, sender=SenderEnum.USER
            )

            await manager.send_personal_message(
                MessageAnswerDTO(**user_message.to_dict()),
                websocket,
            )

            bot_response = "Hello from bot."
            bot_message = save_message(
                db, user_id=user_id, message=bot_response, sender=SenderEnum.BOT
            )

            await manager.send_personal_message(
                MessageAnswerDTO(**bot_message.to_dict()),
                websocket,
            )

    except WebSocketDisconnect:
        manager.disconnect(websocket)
