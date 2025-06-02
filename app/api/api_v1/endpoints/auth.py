from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.security import verify_password, create_access_token, get_password_hash
from app.db.base import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse
import uuid

router = APIRouter()

@router.post("/register", response_model=dict)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if user.email:
        if db.query(User).filter(User.email == user.email).first():
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )
    if user.mobile:
        if db.query(User).filter(User.mobile == user.mobile).first():
            raise HTTPException(
                status_code=400,
                detail="Mobile already registered"
            )
    
    db_user = User(
        id=str(uuid.uuid4()),
        name=user.name,
        email=user.email,
        mobile=user.mobile,
        hashed_password=get_password_hash(user.password),
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return {"message": "User registered successfully"}

@router.post("/login", response_model=dict)
def login(user_in: UserLogin, db: Session = Depends(get_db)):
    if user_in.email:
        user = db.query(User).filter(User.email == user_in.email).first()
    elif user_in.mobile:
        user = db.query(User).filter(User.mobile == user_in.mobile).first()
    else:
        raise HTTPException(
            status_code=400,
            detail="Email or mobile is required"
        )
    
    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(
            status_code=400,
            detail="Incorrect email/mobile or password"
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse.from_orm(user)
    }