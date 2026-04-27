from sqlalchemy import Column, Integer, String
from app.db.base import Base
from fastapi import APIRouter, Depends
from dependencies import get_current_user, require_role
import schemas

router = APIRouter()


@router.get("/me", response_model=schemas.UserResponse)
def get_me(current_user=Depends(get_current_user)):
    return current_user


@router.get("/admin")
def admin_only(user=Depends(require_role("admin"))):
    return {"message": "Welcome Admin!"}
def get_current_user_data(current_user):
    return current_user


def admin_access():
    return {"message": "Welcome Admin!"}
from fastapi import APIRouter, Depends
from dependencies import get_current_user, require_role
import schemas
from services.user_service import get_current_user_data, admin_access

router = APIRouter()


@router.get("/me", response_model=schemas.UserResponse)
def get_me(current_user=Depends(get_current_user)):
    return get_current_user_data(current_user)


@router.get("/admin")
def admin_only(user=Depends(require_role("admin"))):
    return admin_access()
from fastapi import APIRouter, Depends
from dependencies import get_current_user, require_role
import schemas

router = APIRouter()


@router.get("/me", response_model=schemas.UserResponse)
def get_me(current_user=Depends(get_current_user)):
    return current_user


# 🔒 Now truly protected admin route
@router.get("/admin")
def admin_only(user=Depends(require_role("admin"))):
    return {"message": "Welcome Admin!"}
