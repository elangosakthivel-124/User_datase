from pydantic import BaseModel, EmailStr


# ----------- Request Schemas -----------

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: int
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# ----------- Auth Schemas -----------

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


# ----------- Response Schemas -----------

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int
    role: str  # added role as per your final version

    class Config:
        from_attributes = True  # for SQLAlchemy ORM compatibility


from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
import re


class UserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    age: int = Field(..., ge=13, le=120)


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=64)

    @validator("password")
    def validate_password(cls, v):
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"[0-9]", v):
            raise ValueError("Password must contain at least one digit")
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(UserBase):
    id: int
    role: str

    class Config:
        orm_mode = True


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: Optional[str]
    token_type: str = "bearer"
