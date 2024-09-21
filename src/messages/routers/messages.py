from sqlalchemy.orm import Session
from src.database.session import get_db
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from src.messages.enums.sender_enum import SenderEnum
from src.messages.services.websocket_manager import manager
from src.messages.services.messages import get_all_messages_by_user_id, save_message

router = APIRouter(prefix="/messages")


@router.get("/user/{user_id}")
def get_all_messages_by_user_id(user_id: str, db: Session = Depends(get_db)):
    return get_all_messages_by_user_id(db=db, user_id=user_id)


@router.websocket("/ws/chat/{user_id}")
async def websocket_endpoint(
    websocket: WebSocket, user_id: str, db: Session = Depends(get_db)
):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()

            save_message(db, user_id=user_id, message=data, sender=SenderEnum.USER)

            bot_response = "Hello from bot."
            save_message(
                db, user_id=user_id, message=bot_response, sender=SenderEnum.BOT
            )

            await manager.send_personal_message(f"Bot: {bot_response}", websocket)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
