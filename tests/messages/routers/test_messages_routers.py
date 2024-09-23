import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.auth.services.auth import get_current_user
from src.database.base import Base
from src.database.session import get_db
from src.messages.dtos.message_update import MessageUpdateDTO
from src.messages.enums.sender_enum import SenderEnum
from src.messages.models.messages import Message
from src.messages.services.messages import save_message
from src.messages.routers.messages import router
from src.main import app

engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def mock_get_current_user():
    return "user123"


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


@pytest.fixture(scope="function")
def client(test_db):
    app = FastAPI()
    app.include_router(router)

    app.dependency_overrides[get_current_user] = mock_get_current_user
    app.dependency_overrides[get_db] = lambda: test_db

    yield TestClient(app)

    app.dependency_overrides.clear()


def test_get_all_messages_by_user(client, test_db):
    user_id = "user123"
    save_message(
        test_db, user_id=user_id, message="First message", sender=SenderEnum.USER
    )
    save_message(
        test_db, user_id=user_id, message="Second message", sender=SenderEnum.USER
    )

    response = client.get(f"/messages/user/{user_id}")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_update_message_content(client, test_db):
    user_id = "user123"
    message = save_message(
        test_db, user_id=user_id, message="Old message", sender=SenderEnum.USER
    )

    update_data = MessageUpdateDTO(message="Updated message")
    response = client.patch(f"/messages/{message.id}", json=update_data.dict())

    assert response.status_code == 200
    updated_message = test_db.query(Message).filter(Message.id == message.id).first()
    assert updated_message.message == "Updated message"


def test_delete_message_by_id(client, test_db):
    user_id = "user123"
    message = save_message(
        test_db, user_id=user_id, message="Message to delete", sender=SenderEnum.USER
    )

    response = client.delete(f"/messages/{message.id}")
    assert response.status_code == 200

    all_messages = test_db.query(Message).all()
    assert len(all_messages) == 0
