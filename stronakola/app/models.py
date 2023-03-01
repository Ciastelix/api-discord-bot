from sqlalchemy import String, Column
from app.db import Base


class User(Base):
    __tablename__ = "User"
    name = Column(String, primary_key=True)
    nick = Column(String)
    group = Column(String)
    class Config:
        arbitrary_types_allowed = True
        orm_mode = True