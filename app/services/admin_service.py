from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.admin_repo import AdminRepository
from app.schemas.user import UserOut
from app.utils.logger import logger
from app.models.admin import Admin, admin_company_association

from app.schemas.admin import AdminCreate, AdminUpdate, AdminOut
from app.services.auth_service import AuthService
from app.services.base_service import BaseService


class AdminService(BaseService[AdminRepository]):
    def __init__(self, db: AsyncSession, auth_service: AuthService):
        super().__init__(AdminRepository(db), AdminOut)
        self.auth_service = auth_service

    async def get_all_admins_for_admin(self, current_admin: AdminOut) -> List[AdminOut]:
        company_ids = [company.id for company in current_admin.companies]
        if not company_ids:
            return []
        filters = [
            admin_company_association.c.company_id.in_(company_ids),
            admin_company_association.c.admin_id == Admin.id,
        ]
        return await super().get_all(*filters)

    async def get_admin_by_id_for_admin(self, admin_id: int, current_admin: AdminOut) -> Optional[AdminOut]:
        company_ids = [company.id for company in current_admin.companies]
        if not company_ids:
            return None
        filters = [
            admin_company_association.c.company_id.in_(company_ids),
            admin_company_association.c.admin_id == Admin.id,
        ]
        return await super().get_by_id(admin_id, *filters)

    async def get_all_admins_for_user(self, current_user: UserOut) -> List[AdminOut]:
        company_id = current_user.company_id
        if not company_id:
            return []
        filters = [
            admin_company_association.c.company_id == company_id,
            admin_company_association.c.admin_id == Admin.id,
        ]
        return await super().get_all(*filters)

    async def get_admin_by_id_for_user(self, admin_id: int, current_user: UserOut) -> Optional[AdminOut]:
        company_id = current_user.company_id
        if not company_id:
            return None
        filters = [
            admin_company_association.c.company_id == company_id,
            admin_company_association.c.admin_id == Admin.id,
        ]
        return await super().get_by_id(admin_id, *filters)

    async def create(self, admin_data: AdminCreate) -> Optional[AdminOut]:
        logger.warning("ADMIN_SERVICE: Attempt to create admin")

        admin_data_dict = admin_data.model_dump(exclude={"password"})
        admin_data_dict["hashed_password"] = self.auth_service.hash_password(admin_data.password)

        return await super().create(admin_data_dict)

    async def update(self, admin_id: int, admin_data: AdminUpdate) -> Optional[AdminOut]:
        logger.warning("ADMIN_SERVICE: Attempt to update admin")
        admin = await self.repository.get_by_id(admin_id)
        if not admin:
            logger.warning(f"Attempt to update non-existent admin: {admin_id}")
            return None

        updated_admin = admin_data.model_dump(exclude_unset=True)
        if "password" in updated_admin and updated_admin["password"]:
            updated_admin["hashed_password"] = self.auth_service.hash_password(updated_admin["password"])
            del updated_admin["password"]

        return await super().update(admin_id, updated_admin)

    async def add_company_to_admin(self, admin_id: int, company_id: int) -> Optional[AdminOut]:
        admin = await self.repository.add_company_to_admin(admin_id, company_id)
        return AdminOut.model_validate(admin) if admin else None

    async def remove_company_from_admin(self, admin_id: int, company_id: int) -> Optional[AdminOut]:
        admin = await self.repository.remove_company_from_admin(admin_id, company_id)
        return AdminOut.model_validate(admin) if admin else None

    async def authenticate_admin(self, username: str, password: str) -> Optional[Admin]:
        admin = await self.repository.get_by_username(username)
        if not admin or not self.auth_service.verify_password(password, admin.hashed_password):
            logger.warning("Failed to authenticate admin")
            return None
        return admin

    async def create_admin_token(self, admin: Admin) -> Optional[str]:
        if not admin:
            return None
        token_data = {"sub": admin.username, "role": "admin", "id": admin.id}
        return await self.auth_service.create_access_token(token_data)
