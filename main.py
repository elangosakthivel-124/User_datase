from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from db import engine, get_db
from security import hash_password, verify_password
from auth import create_access_token

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# ✅ Register
@app.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = models.User(
        name=user.name,
        email=user.email,
        age=user.age,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# ✅ Login
@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": db_user.email})

    return {"access_token": token, "token_type": "bearer"}

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from db import engine, get_db
from security import hash_password, verify_password
from auth import create_access_token
from dependencies import get_current_user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# ✅ Register
@app.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = models.User(
        name=user.name,
        email=user.email,
        age=user.age,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# ✅ Login (OAuth2 style)
@app.post("/login", response_model=schemas.Token)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": db_user.email})

    return {"access_token": token, "token_type": "bearer"}


# 🔒 Protected Route
@app.get("/me", response_model=schemas.UserResponse)
def get_me(current_user = Depends(get_current_user)):
    return current_user
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from db import engine, get_db
from auth import create_access_token, create_refresh_token, decode_token
from dependencies import get_current_user
from services.user_service import create_user, authenticate_user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# ✅ Register
@app.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = create_user(db, user)

    if not new_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    return new_user


# ✅ Login → Access + Refresh
@app.post("/login", response_model=schemas.TokenPair)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = authenticate_user(db, user.email, user.password)

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access = create_access_token({"sub": db_user.email})
    refresh = create_refresh_token({"sub": db_user.email})

    return {
        "access_token": access,
        "refresh_token": refresh
    }


# 🔄 Refresh Token
@app.post("/refresh", response_model=schemas.TokenPair)
def refresh_token(refresh_token: str):
    payload = decode_token(refresh_token)

    if payload is None or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    email = payload.get("sub")

    new_access = create_access_token({"sub": email})
    new_refresh = create_refresh_token({"sub": email})

    return {
        "access_token": new_access,
        "refresh_token": new_refresh
    }


# 🔒 Protected Route
@app.get("/me", response_model=schemas.UserResponse)
def get_me(current_user = Depends(get_current_user)):
    return current_user
