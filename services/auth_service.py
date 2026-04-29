from sqlalchemy.orm import Session
from fastapi import HTTPException, status

import models
from core.security import hash_password, verify_password
from core.token import create_access_token, create_refresh_token


def register_user(db: Session, user_data):
    # Normalize email
    email = user_data.email.lower().strip()

    existing_user = db.query(models.User).filter(models.User.email == email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    new_user = models.User(
        name=user_data.name.strip(),
        email=email,
        age=user_data.age,
        password=hash_password(user_data.password),
        role="user"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Return safe response (avoid exposing password)
    return {
        "id": new_user.id,
        "name": new_user.name,
        "email": new_user.email,
        "age": new_user.age,
        "role": new_user.role
    }


def login_user(db: Session, user_data):
    email = user_data.email.lower().strip()

    db_user = db.query(models.User).filter(models.User.email == email).first()

    if not db_user or not verify_password(user_data.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    token_data = {
        "sub": db_user.email,
        "role": db_user.role
    }

    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
