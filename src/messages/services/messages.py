from sqlalchemy.orm import Session
from src.messages.models.messages import Message
from src.messages.enums.sender_enum import SenderEnum


def save_message(db: Session, user_id: str, message: str, sender: SenderEnum):
    new_message = Message(user_id=user_id, message=message, sender=sender)
    print(f"{new_message}")
    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    return new_message
