from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import Optional, List

from app.models.company import Company
from app.repositories.base_repo import BaseRepository


class CompanyRepository(BaseRepository[Company]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Company)

    async def get_by_id(self, company_id: int, *filters) -> Optional[Company]:
        base_filters = [Company.id == company_id, Company.deleted.is_(False)]
        if filters:
            base_filters.extend(filters)
        stmt = (
            select(Company)
            .options(selectinload(Company.admins))
            .options(selectinload(Company.users))
            .where(*base_filters)
        )
        return await self.db.scalar(stmt)

    async def get_by_username(self, username: str, *filters) -> Optional[Company]:
        base_filters = [Company.username == username, Company.deleted.is_(False)]
        if filters:
            base_filters.extend(filters)
        stmt = (
            select(Company)
            .options(selectinload(Company.users))
            .options(selectinload(Company.admins))
            .where(*base_filters)
        )
        return await self.db.scalar(stmt)

    async def get_all(self, *filters) -> List[Company]:
        base_filters = [Company.deleted.is_(False)]
        if filters:
            base_filters.extend(filters)
        stmt = (
            select(Company)
            .options(selectinload(Company.users))
            .options(selectinload(Company.admins))
            .where(*base_filters)
            .distinct()
        )
        result = await self.db.scalars(stmt)
        return list(result.all())