from typing import Optional
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.models import Owner, Admin, User
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.services.admin_service import AdminService
from app.services.owner_service import OwnerService
from app.dependencies.services import get_auth_service, get_user_service, get_owner_service, get_admin_service


oauth2_user_scheme = OAuth2PasswordBearer(tokenUrl="users/login", auto_error=False)
oauth2_admin_scheme = OAuth2PasswordBearer(tokenUrl="admins/login", auto_error=False)
oauth2_owner_scheme = OAuth2PasswordBearer(tokenUrl="owner/login", auto_error=False)


async def get_current_user(
    token: Optional[str] = Depends(oauth2_user_scheme),
    auth_service: AuthService = Depends(get_auth_service),
    user_service: UserService = Depends(get_user_service)
) -> Optional[User]:
    if not token:
        return None

    payload = await auth_service.verify_token(token)
    if payload.get("role") != "user":
        return None

    return await user_service.get_by_username(payload.get("sub"))

async def get_current_admin(
    token: Optional[str] = Depends(oauth2_admin_scheme),
    auth_service: AuthService = Depends(get_auth_service),
    admin_service: AdminService = Depends(get_admin_service)
) -> Optional[Admin]:
    if not token:
        return None

    payload = await auth_service.verify_token(token)
    if payload.get("role") != "admin":
        return None

    return await admin_service.get_by_username(payload.get("sub"))

async def get_current_owner(
    token: Optional[str] = Depends(oauth2_owner_scheme),
    auth_service: AuthService = Depends(get_auth_service),
    owner_service: OwnerService = Depends(get_owner_service)
) -> Optional[Owner]:
    if not token:
        return None

    payload = await auth_service.verify_token(token)
    if payload.get("role") != "owner":
        return None

    return await owner_service.get_by_username(payload.get("sub"))
