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
