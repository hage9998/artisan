from fastapi import HTTPException
from sqlalchemy import delete
from sqlalchemy.orm import Session
from src.messages.dtos.message_update import MessageUpdateDTO
from src.messages.models.messages import Message
from src.messages.enums.sender_enum import SenderEnum


def save_message(db: Session, user_id: str, message: str, sender: SenderEnum):
    """
    Saves a new message to the database.

    Parameters
    ----------
    db : Session
        The database session.
    user_id : str
        The ID of the user sending the message.
    message : str
        The content of the message to be saved.
    sender : SenderEnum
        The sender of the message (user or bot).

    Returns
    -------
    Message
        The Message object that was saved.
    """

    new_message = Message(user_id=user_id, message=message, sender=sender)

    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    return new_message


def get_all_messages_by_user_id(db: Session, user_id: str):
    """
    Retrieves all messages sent by a specific user.

    Parameters
    ----------
    db : Session
        The database session.
    user_id : str
        The ID of the user whose messages should be retrieved.

    Returns
    -------
    List[Message]
        A list of Message objects belonging to the user.
    """

    return db.query(Message).filter(Message.user_id == user_id).all()


def update_message(db: Session, message_id: str, new_message: MessageUpdateDTO):
    """
    Updates the content of an existing message.

    Parameters
    ----------
    db : Session
        The database session.
    message_id : str
        The ID of the message to be updated.
    new_message : MessageUpdateDTO
        An object containing the new message data.

    Raises
    ------
    HTTPException
        If the message is not found (404).
    """

    current_message = db.query(Message).filter(Message.id == message_id).first()

    if not current_message:
        raise HTTPException(status_code=404, detail="Message not found")

    current_message.message = new_message

    db.commit()


def delete_message(db: Session, message_id: str):
    """
    Deletes an existing message from the database.

    Parameters
    ----------
    db : Session
        The database session.
    message_id : str
        The ID of the message to be deleted.

    Raises
    ------
    HTTPException
        If the message is not found (404).
    """

    current_message = db.query(Message).filter(Message.id == message_id).first()

    if not current_message:
        raise HTTPException(status_code=404, detail="Message not found")

    stmt = delete(Message).where(Message.id == message_id)

    db.execute(stmt)
    db.commit()
