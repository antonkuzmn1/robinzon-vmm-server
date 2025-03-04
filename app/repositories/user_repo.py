from typing import List, Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models import Company
from app.models.user import User
from app.repositories.base_repo import BaseRepository
from app.utils.logger import logger


class UserRepository(BaseRepository[User]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, User)

    async def get_by_username(self, username: str, *filters) -> Optional[User]:
        base_filters = [User.username == username, User.deleted.is_(False)]
        if filters:
            base_filters.extend(filters)
        stmt = (
            select(User)
            .options(selectinload(User.company))
            .where(*base_filters)
        )
        return await self.db.scalar(stmt)

    async def get_all(self, *filters) -> List[User]:
        base_filters = [User.deleted.is_(False)]
        if filters:
            base_filters.extend(filters)
        stmt = (
            select(User)
            .options(selectinload(User.company))
            .where(*base_filters)
            .distinct()
        )
        result = await self.db.scalars(stmt)
        return list(result.all())

    async def get_by_id(self, user_id: int, *filters) -> Optional[User]:
        base_filters = [User.id == user_id, User.deleted.is_(False)]
        if filters:
            base_filters.extend(filters)
        stmt = (
            select(User)
            .options(selectinload(User.company))
            .where(*base_filters)
        )
        return await self.db.scalar(stmt)

    async def get_all_users_by_company(self, company_id: int) -> List[User]:
        try:
            stmt = (
                select(User)
                .options(selectinload(User.company))
                .where(User.company_id == company_id, User.deleted == False)
            )
            result = await self.db.scalars(stmt)
            return list(result.all())
        except SQLAlchemyError as e:
            logger.error(f"Failed to get users by company_id={company_id}: {e}")
            await self.db.rollback()
            return []

    async def get_company_by_user_username(self, username: str) -> Optional[Company]:
        try:
            stmt = (
                select(User)
                .options(selectinload(User.company))
                .where(User.username == username, User.deleted == False)
            )
            user = await self.db.scalar(stmt)
            return user.company if user else None
        except SQLAlchemyError as e:
            logger.error(f"Failed to get company by username={username}: {e}")
            await self.db.rollback()
            return None

    async def get_company_by_user_id(self, user_id: int) -> Optional[Company]:
        try:
            stmt = (
                select(User)
                .options(selectinload(User.company))
                .where(User.id == user_id, User.deleted == False)
            )
            user = await self.db.scalar(stmt)
            return user.company if user else None
        except SQLAlchemyError as e:
            logger.error(f"Failed to get company by user_id={user_id}: {e}")
            await self.db.rollback()
            return None
