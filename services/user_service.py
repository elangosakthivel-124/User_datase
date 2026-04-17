from sqlalchemy.orm import Session
import models
from security import hash_password, verify_password

def create_user(db: Session, user_data):
    existing = db.query(models.User).filter(models.User.email == user_data.email).first()
    if existing:
        return None

    user = models.User(
        name=user_data.name,
        email=user_data.email,
        age=user_data.age,
        password=hash_password(user_data.password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(models.User).filter(models.User.email == email).first()

    if not user or not verify_password(password, user.password):
        return None

    return user
