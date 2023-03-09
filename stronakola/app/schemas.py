from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from app.models import User
UserSchema = sqlalchemy_to_pydantic(User)