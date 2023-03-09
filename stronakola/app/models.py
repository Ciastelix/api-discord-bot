from sqlalchemy import String, Column
from app.db import Base


class User(Base):
    __tablename__ = "User"
    name = Column(String(50), primary_key=True)
    nick = Column(String(20))
    group = Column(String(15))
