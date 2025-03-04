from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.repositories.user_repo import UserRepository
from app.schemas.admin import AdminOut
from app.schemas.user import UserOut, UserCreate, UserUpdate
from app.services.auth_service import AuthService
from app.services.base_service import BaseService


class UserService(BaseService[UserRepository]):
    def __init__(self, db: AsyncSession, auth_service: AuthService):
        super().__init__(UserRepository(db), UserOut)
        self.auth_service = auth_service

    async def get_all_users_for_admin(self, current_admin: AdminOut) -> List[UserOut]:
        company_ids = [company.id for company in current_admin.companies]
        if not company_ids:
            return []
        filters = [User.company_id.in_(company_ids)]
        return await super().get_all(*filters)

    async def get_all_users_for_user(self, current_user: UserOut) -> List[UserOut]:
        company_id = current_user.company_id
        if not company_id:
            return []
        filters = [User.company_id == company_id]
        return await super().get_all(*filters)

    async def get_user_by_id_for_admin(self, user_id: int, current_admin: AdminOut) -> Optional[UserOut]:
        company_ids = [company.id for company in current_admin.companies]
        if not company_ids:
            return None
        filters = [User.company_id.in_(company_ids)]
        return await super().get_by_id(user_id, *filters)

    async def get_user_by_id_for_user(self, user_id: int, current_user: UserOut) -> Optional[AdminOut]:
        company_id = current_user.company_id
        if not company_id:
            return None
        filters = [User.company_id == company_id]
        return await super().get_by_id(user_id, *filters)

    async def create_by_admin(self, user: UserCreate, current_admin: AdminOut) -> Optional[UserOut]:
        company_ids = [company.id for company in current_admin.companies]
        if not user.company_id or user.company_id not in company_ids:
            return None
        return await super().create(user)

    async def update_by_admin(self, user_id: int, user_data: UserUpdate, current_admin: AdminOut) -> Optional[UserOut]:
        company_ids = [company.id for company in current_admin.companies]
        user = await self.get_by_id(user_id)
        if not user:
            return None

        old_company_id = user.company_id

        if not old_company_id or old_company_id not in company_ids:
            return None

        if not user_data.company_id or user_data.company_id not in company_ids:
            return None

        return await super().update(user_id, user)

    async def delete_by_admin(self, user_id: int, current_admin: AdminOut) -> Optional[UserOut]:
        company_ids = [company.id for company in current_admin.companies]
        old_company_id = (await self.get_by_id(user_id)).company_id

        if not old_company_id or old_company_id not in company_ids:
            return None

        return await super().delete(user_id)

    async def authenticate_user(self, username: str, password: str):
        user = await self.repository.get_by_username(username)
        if not user or user.password != password:
            return None
        return user

    async def create_user_token(self, user) -> Optional[str]:
        if not user:
            return None
        token_data = {"sub": user.username, "role": "user", "id": user.id}
        return await self.auth_service.create_access_token(token_data)
