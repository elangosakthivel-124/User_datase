from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    age: int

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    age: int

    class Config:
        from_attributes = True
from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    age: int

class UserUpdate(BaseModel):
    name: str
    email: str
    age: int

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    age: int

    class Config:
        from_attributes = True
