from fastapi import HTTPException
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.base import Base
from src.messages.models.messages import Message
from src.messages.services.messages import (
    save_message,
    get_all_messages_by_user_id,
    update_message,
    delete_message,
)
from src.messages.enums.sender_enum import SenderEnum
from src.messages.dtos.message_update import MessageUpdateDTO

DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def test_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        yield db
    finally:
        db.rollback()
        db.close()
        Base.metadata.drop_all(bind=engine)


def test_save_message(test_db):
    result = save_message(
        test_db, user_id="user123", message="Test message", sender=SenderEnum.USER
    )
    assert result.user_id == "user123"
    assert result.message == "Test message"
    assert result.sender == SenderEnum.USER

    all_messages = test_db.query(Message).all()
    assert len(all_messages) == 1


def test_get_all_messages_by_user_id(test_db):
    save_message(
        test_db, user_id="user123", message="First message", sender=SenderEnum.USER
    )
    save_message(
        test_db, user_id="user123", message="Second message", sender=SenderEnum.USER
    )

    messages = get_all_messages_by_user_id(test_db, user_id="user123")
    assert len(messages) == 2
    assert messages[0].message == "First message"
    assert messages[1].message == "Second message"


def test_update_message(test_db):
    message = save_message(
        test_db, user_id="user123", message="Old message", sender=SenderEnum.USER
    )

    new_message_data = MessageUpdateDTO(message="Updated message")
    update_message(test_db, message_id=message.id, new_message=new_message_data)

    updated_message = test_db.query(Message).filter(Message.id == message.id).first()
    assert updated_message.message == "Updated message"


def test_update_message_not_found(test_db):
    new_message_data = MessageUpdateDTO(message="Some message")
    with pytest.raises(HTTPException) as exc_info:
        update_message(
            test_db, message_id="nonexistent_id", new_message=new_message_data
        )
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Message not found"


def test_delete_message(test_db):
    message = save_message(
        test_db, user_id="user123", message="Message to delete", sender=SenderEnum.USER
    )

    all_messages = test_db.query(Message).all()
    assert len(all_messages) == 1

    delete_message(test_db, message_id=message.id)

    all_messages = test_db.query(Message).all()
    assert len(all_messages) == 0


def test_delete_message_not_found(test_db):
    with pytest.raises(HTTPException) as exc_info:
        delete_message(test_db, message_id="nonexistent_id")

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Message not found"
