import uuid
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from src.database.base import Base


class User(Base):
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    auth_token = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    messages = relationship("Message", back_populates="user")
