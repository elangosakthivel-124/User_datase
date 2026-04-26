from sqlalchemy.orm import Session
import models
from core.security import hash_password, verify_password
from core.token import create_access_token, create_refresh_token
from core.logger import logger


def register_user(db: Session, user_data):
    existing_user = db.query(models.User).filter(models.User.email == user_data.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = models.User(
        name=user_data.name,
        email=user_data.email,
        age=user_data.age,
        password=hash_password(user_data.password),
        role="user"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def login_user(db: Session, user_data):
    db_user = db.query(models.User).filter(models.User.email == user_data.email).first()

    if not db_user or not verify_password(user_data.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = create_access_token({"sub": db_user.email})
    refresh_token = create_refresh_token({"sub": db_user.email})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
