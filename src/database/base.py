import uuid
import sqlalchemy as sql
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = sql.Column(sql.String, primary_key=True, default=lambda: str(uuid.uuid4()))
