from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models, schemas
from db import engine, get_db
from security import hash_password, verify_password
from auth import create_access_token
from dependencies import get_current_user, require_role
from utils.redis_client import blacklist_token
from core.logger import logger

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# ✅ Register
@app.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == user.email).first()

    if existing:
        logger.warning("Duplicate registration attempt")
        raise HTTPException(status_code=400, detail="Email already exists")

    new_user = models.User(
        name=user.name,
        email=user.email,
        age=user.age,
        password=hash_password(user.password),
        role="user"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    logger.info(f"User registered: {user.email}")
    return new_user


# ✅ Login
@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.password):
        logger.warning("Failed login attempt")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token({"sub": db_user.email})

    logger.info(f"User logged in: {user.email}")
    return {
        "access_token": token,
        "token_type": "bearer"
    }


# 🔒 Logout (Token Blacklist)
@app.post("/logout")
def logout(token: str):
    # Expect token from frontend (Authorization header extraction is better in production)
    blacklist_token(token, 900)
    return {"message": "Logged out successfully"}


# 🔒 Protected Route
@app.get("/me", response_model=schemas.UserResponse)
def get_me(current_user = Depends(get_current_user)):
    return current_user


# 👑 Admin Only
@app.get("/admin")
def admin_only(user = Depends(require_role("admin"))):
    return {"message": "Welcome Admin!"}
