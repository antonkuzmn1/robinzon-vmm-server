from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.services.admin_service import AdminService
from app.services.auth_service import AuthService
from app.services.company_service import CompanyService
from app.services.config_service import ConfigService
from app.services.owner_service import OwnerService
from app.services.user_service import UserService


async def get_auth_service() -> AuthService:
    return AuthService()

async def get_user_service(
    db: Annotated[AsyncSession, Depends(get_db)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
) -> UserService:
    return UserService(db, auth_service)

async def get_admin_service(
        db: Annotated[AsyncSession, Depends(get_db)],
        auth_service: Annotated[AuthService, Depends(get_auth_service)]
) -> AdminService:
    return AdminService(db, auth_service)

async def get_company_service(
        db: Annotated[AsyncSession, Depends(get_db)]
) -> CompanyService:
    return CompanyService(db)

async def get_owner_service(
        db: Annotated[AsyncSession, Depends(get_db)],
        auth_service: Annotated[AuthService, Depends(get_auth_service)]
) -> OwnerService:
    return OwnerService(db, auth_service)

async def get_config_service(
        db: Annotated[AsyncSession, Depends(get_db)]
) -> ConfigService:
    return ConfigService(db)