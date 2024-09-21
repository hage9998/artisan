from sqlalchemy.orm import Session
from src.messages.models.messages import Message
from src.messages.enums.sender_enum import SenderEnum


def save_message(db: Session, user_id: str, message: str, sender: SenderEnum):
    new_message = Message(user_id=user_id, message=message, sender=sender)

    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    return new_message


def get_all_messages_by_user_id(db: Session, user_id: str):
    return db.query(Message).filter(Message.user_id == user_id).all()
