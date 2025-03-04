from typing import List, Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.admin import Admin
from app.models.company import admin_company_association, Company
from app.repositories.base_repo import BaseRepository
from app.utils.logger import logger


class AdminRepository(BaseRepository[Admin]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Admin)

    async def get_by_username(self, username: str, *filters) -> Optional[Admin]:
        base_filters = [Admin.username == username, Admin.deleted.is_(False)]
        if filters:
            base_filters.extend(filters)
        stmt = (
            select(Admin)
            .options(selectinload(Admin.companies))
            .where(*base_filters)
        )
        return await self.db.scalar(stmt)

    async def get_all(self, *filters) -> List[Admin]:
        base_filters = [Admin.deleted.is_(False)]
        if filters:
            base_filters.extend(filters)
        stmt = (
            select(Admin)
            .options(selectinload(Admin.companies))
            .where(*base_filters)
            .distinct()
        )
        result = await self.db.scalars(stmt)
        return list(result.all())

    async def get_by_id(self, admin_id: int, *filters) -> Optional[Admin]:
        base_filters = [Admin.id == admin_id, Admin.deleted.is_(False)]
        if filters:
            base_filters.extend(filters)
        stmt = (
            select(Admin)
            .options(selectinload(Admin.companies))
            .where(*base_filters)
        )
        return await self.db.scalar(stmt)

    async def get_all_admins_by_company(self, company_id: int) -> List[Admin]:
        try:
            stmt = (
                select(Admin)
                .options(selectinload(Admin.companies))
                .join(admin_company_association)
                .where(admin_company_association.c.company_id == company_id)
            )
            result = await self.db.scalars(stmt)
            return list(result.all())
        except SQLAlchemyError as e:
            logger.error(f"Error fetching admins by company: {e}")
            await self.db.rollback()
            return []

    async def get_all_companies_by_admin(self, admin_id: int) -> List[Company]:
        try:
            stmt = (
                select(Admin)
                .options(selectinload(Admin.companies))
                .where(
                    Admin.id == admin_id,
                    Admin.deleted.is_(False)
                )
            )
            admin = await self.db.scalar(stmt)
            return admin.companies if admin else []
        except SQLAlchemyError as e:
            logger.error(f"Error fetching companies by admin: {e}")
            await self.db.rollback()
            return []

    async def add_company_to_admin(self, admin_id: int, company_id: int) -> Optional[Admin]:
        try:
            admin = await self.get_by_id(admin_id)
            company = await self.db.scalar(
                select(Company).where(Company.id == company_id)
            )

            if not admin or not company or company in admin.companies:
                return None

            admin.companies.append(company)
            await self.db.commit()
            await self.db.refresh(admin)
            return admin
        except SQLAlchemyError as e:
            logger.error(f"Error adding company to admin: {e}")
            await self.db.rollback()
            return None

    async def remove_company_from_admin(self, admin_id: int, company_id: int) -> Optional[Admin]:
        try:
            admin = await self.get_by_id(admin_id)
            company = await self.db.scalar(
                select(Company).where(Company.id == company_id)
            )

            if not admin or not company or company not in admin.companies:
                return None

            admin.companies.remove(company)
            await self.db.commit()
            await self.db.refresh(admin)
            return admin
        except SQLAlchemyError as e:
            logger.error(f"Error removing company from admin: {e}")
            await self.db.rollback()
            return None
