from fastapi import FastAPI, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

import models, schemas
from db import engine, get_db
from security import hash_password, verify_password
from auth import create_access_token
from dependencies import get_current_user, require_role
from utils.redis_client import blacklist_token
from core.logger import logger

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Management API", version="1.0.0")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# =========================
# ✅ Register
# =========================
@app.post("/register", response_model=schemas.UserResponse, status_code=201)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        existing_user = db.query(models.User).filter(
            models.User.email == user.email
        ).first()

        if existing_user:
            logger.warning(f"Duplicate registration: {user.email}")
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )

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

    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


# =========================
# ✅ Login
# =========================
@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if not db_user or not verify_password(user.password, db_user.password):
        logger.warning(f"Failed login: {user.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = create_access_token({"sub": db_user.email})

    logger.info(f"User logged in: {user.email}")

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# =========================
# 🔒 Logout (Improved)
# =========================
@app.post("/logout")
def logout(token: str = Depends(oauth2_scheme)):
    try:
        # Blacklist token for 15 minutes (adjust based on token expiry)
        blacklist_token(token, 900)

        logger.info("User logged out")
        return {"message": "Logged out successfully"}

    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        raise HTTPException(status_code=500, detail="Logout failed")


# =========================
# 🔒 Protected Route
# =========================
@app.get("/me", response_model=schemas.UserResponse)
def get_me(current_user=Depends(get_current_user)):
    return current_user
from fastapi import FastAPI
from db import engine
import models

from routers import auth, users

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Management API", version="1.1.0")

# Include Routers
app.include_router(auth.router, tags=["Auth"])
app.include_router(users.router, tags=["Users"])
from fastapi import FastAPI
from db import engine
import models

from routers import auth, users

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Management API", version="1.2.0")

app.include_router(auth.router, tags=["Auth"])
app.include_router(users.router, tags=["Users"])
