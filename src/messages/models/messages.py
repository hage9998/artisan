from sqlalchemy import Column, Integer, String, Enum as SQLAlchemyEnum, ForeignKey
from sqlalchemy.orm import relationship
from src.database.base import Base
from src.messages.enums.sender_enum import SenderEnum


class Message(Base):
    __tablename__ = "messages"

    user_id = Column(Integer, ForeignKey("users.id"))
    message = Column(String)
    sender = Column(SQLAlchemyEnum(SenderEnum))

    user = relationship("User", back_populates="messages")
