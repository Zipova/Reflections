from datetime import datetime
from typing import List

from pydantic import BaseModel, Field, EmailStr


class UserModel(BaseModel):
    username: str = Field(min_length=6, max_length=25)
    email: EmailStr
    password: str = Field(min_length=6, max_length=15)


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    avatar: str
    is_active: bool


class Username(BaseModel):
    id: int
    username: str


class UserUpdate(BaseModel):
    username: str


class UserStatusUpdate(BaseModel):
    is_active: bool


class UserRoleUpdate(BaseModel):
    role: str


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    email: EmailStr


class CommentModel(BaseModel):
    comment: str


class CommentResponse(CommentModel):
    user: Username
    photo_id: int
    comment: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class PhotoModel(BaseModel):
    description: str


class PhotoDb(BaseModel):
    id: int
    url: str
    description: str | None

    class Config:
        orm_mode = True


class PhotoResponse(BaseModel):
    photo: PhotoDb
    detail: str = "Photo was created successfully"


class PhotoResp(BaseModel):
    url: str
    description: str | None
    comments: List[CommentResponse]

    class Config:
        orm_mode = True


class DescriptionUpdate(BaseModel):
    done: bool


class PhotoSearch(BaseModel):
    id: int
    photo: str
    qr_code: str | None
    description: str | None
    average_rating: float | None


class Config:
    orm_mode = True




