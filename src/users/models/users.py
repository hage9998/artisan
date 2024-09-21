from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from src.database.base import Base


class User(Base):
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    messages = relationship("Message", back_populates="user")
