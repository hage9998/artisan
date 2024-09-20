from sqlalchemy import Column, Integer, String
from src.database.base import Base


class Users(Base):
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
