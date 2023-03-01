from pydantic import BaseModel


class UserSchema(BaseModel):
    name: str | None = None
    nick: str | None = None
    group: str | None = None