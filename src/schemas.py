from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    avatar: str
    is_active: bool

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    email: str
    avatar: str


class UserStatusUpdate(BaseModel):
    is_active: bool
