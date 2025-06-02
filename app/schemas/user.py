from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    mobile: Optional[constr(regex=r'^\d{10}$')] = None
    role: str = "student"

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: Optional[EmailStr] = None
    mobile: Optional[constr(regex=r'^\d{10}$')] = None
    password: str
    fcm_token: Optional[str] = None

class UserResponse(UserBase):
    id: str
    is_verified: bool
    last_login: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True