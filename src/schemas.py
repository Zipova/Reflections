from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional


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


class UserUpdate(BaseModel):
    email: str
    avatar: str


class UserStatusUpdate(BaseModel):
    is_active: bool


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    email: EmailStr


class PhotoModel(BaseModel):
    description: str
    tags: List[str] = []

class PhotoDb(BaseModel):
    id: int
    photo: str
    description: Optional[str] = None
    qr_code: Optional[str] = None
    transformed_image_url: Optional[str] = None

    class Config:
        from_attributes = True


class PhotoResponse(BaseModel):
    photo: PhotoDb
    detail: str = "Photo was created successfully"


class DescriptionUpdate(BaseModel):
    done: bool


class PhotoSearch(BaseModel):
    id: int
    photo: str
    qr_code: Optional[str] = None
    description: Optional[str] = None
    average_rating: float


class Config:
    orm_mode = True
