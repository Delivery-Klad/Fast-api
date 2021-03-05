from pydantic import BaseModel


class User(BaseModel):
    user_id: int
    score: int


class AuthDetails(BaseModel):
    username: str
    password: str
