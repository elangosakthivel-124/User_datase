from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr   # ✅ validates email format
    age: int

class UserUpdate(BaseModel):
    name: str
    email: EmailStr
    age: int

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int

    class Config:
        from_attributes = True
