from sqlalchemy.orm import Session
from src.database.session import get_db
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from src.messages.enums.sender_enum import SenderEnum
from src.messages.services.websocket_manager import manager
from src.messages.services.messages import save_message
from src.messages.models.messages import Message

router = APIRouter(prefix="/messages")


@router.get("/user/{user_id}")
def get_bla(user_id: str, db: Session = Depends(get_db)):
    return db.query(Message).filter(Message.user_id == user_id).all()


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
