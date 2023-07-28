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


class PhotoDb(BaseModel):
    id: int
    photo: str
    description: str | None
    qr_code: str | None

    class Config:
        orm_mode = True


class PhotoResponse(BaseModel):
    photo: PhotoDb
    detail: str = "Photo was created successfully"


class DescriptionUpdate(BaseModel):
    done: bool


class PhotoSearch(BaseModel):
    id: int
    photo: str
    qr_code: str | None
    description: str | None
    average_rating: float


class Config:
    orm_mode = True
