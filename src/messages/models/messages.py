import datetime
from sqlalchemy import Column, DateTime, String, Enum as SQLAlchemyEnum, ForeignKey
from sqlalchemy.orm import relationship
from src.database.base import Base
from src.messages.enums.sender_enum import SenderEnum


class Message(Base):
    __tablename__ = "messages"

    user_id = Column(String, ForeignKey("user.id"))
    message = Column(String)
    sender = Column(SQLAlchemyEnum(SenderEnum))
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))

    user = relationship("User", back_populates="messages")

    def to_dict(self):
        return {
            "sender": self.sender,
            "message": self.message,
            "id": self.id,
            "createdAt": self.created_at.isoformat(),
        }
