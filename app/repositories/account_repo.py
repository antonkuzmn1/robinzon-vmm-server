from typing import Optional, Sequence, cast

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Account
from app.models.group import m2m_group_account, Group
from app.repositories.base_repo import BaseRepository
from app.utils.logger import logger


class AccountRepository(BaseRepository[Account]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Account)

    async def get_all_accounts_by_group(self, group_id: int) -> Sequence[Account]:
        try:
            stmt = (
                select(Account)
                .options(selectinload(Account.groups))
                .join(m2m_group_account)
                .where(cast("ColumnElement[bool]", m2m_group_account.c.group_id == group_id))
            )
            result = await self.db.scalars(stmt)
            return result.all()
        except SQLAlchemyError as e:
            logger.error(f"Error fetching accounts by group: {e}")
            await self.db.rollback()
            return []

    async def get_all_groups_by_account(self, account_id: int) -> Sequence[Group]:
        try:
            stmt = (
                select(Account)
                .options(selectinload(Account.groups))
                .where(
                    Account.id == account_id,
                    Account.deleted.is_(False)
                )
            )
            account = await self.db.scalar(stmt)
            return account.groups if account else []
        except SQLAlchemyError as e:
            logger.error(f"Error fetching groups by account: {e}")
            await self.db.rollback()
            return []

    async def add_group_to_account(self, account_id: int, group_id: int) -> Optional[Account]:
        try:
            account = await self.get_by_id(account_id)
            group = await self.db.scalar(
                select(Group).where(Group.id == group_id)
            )

            if not account or not group or group in account.groups:
                return None

            account.groups.append(group)
            await self.db.commit()
            await self.db.refresh(account)
            return account
        except SQLAlchemyError as e:
            logger.error(f"Error adding group to account: {e}")
            await self.db.rollback()
            return None

    async def remove_group_from_account(self, account_id: int, group_id: int) -> Optional[Account]:
        try:
            account = await self.get_by_id(account_id)
            group = await self.db.scalar(
                select(Group).where(Group.id == group_id)
            )

            if not account or not group or group not in account.groups:
                return None

            account.groups.remove(group)
            await self.db.commit()
            await self.db.refresh(account)
            return account
        except SQLAlchemyError as e:
            logger.error(f"Error removing group from account: {e}")
            await self.db.rollback()
            return None
