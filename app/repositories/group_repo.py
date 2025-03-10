from typing import Optional, Sequence, cast

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Account, VM
from app.models.group import m2m_group_account, Group, m2m_group_vm
from app.repositories.base_repo import BaseRepository
from app.utils.logger import logger


class GroupRepository(BaseRepository[Group]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Group)

    async def get_all_groups_by_account(self, account_id: int) -> list[Group]:
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

    async def get_all_groups_by_vm(self, vm_id: int) -> list[Group]:
        try:
            stmt = (
                select(VM)
                .options(selectinload(VM.groups))
                .where(
                    VM.id == vm_id,
                    Account.deleted.is_(False)
                )
            )
            vm = await self.db.scalar(stmt)
            return vm.groups if vm else []
        except SQLAlchemyError as e:
            logger.error(f"Error fetching groups by vm: {e}")
            await self.db.rollback()
            return []

    async def get_all_accounts_by_group(self, group_id: int) -> list[Account]:
        try:
            stmt = (
                select(Account)
                .options(selectinload(Account.groups))
                .join(m2m_group_account)
                .where(cast("ColumnElement[bool]", m2m_group_account.c.group_id == group_id))
            )
            result = await self.db.scalars(stmt)
            return list(result.all())
        except SQLAlchemyError as e:
            logger.error(f"Error fetching accounts by group: {e}")
            await self.db.rollback()
            return []

    async def get_all_vms_by_group(self, group_id: int) -> list[VM]:
        try:
            stmt = (
                select(VM)
                .options(selectinload(VM.groups))
                .join(m2m_group_vm)
                .where(cast("ColumnElement[bool]", m2m_group_vm.c.group_id == group_id))
            )
            result = await self.db.scalars(stmt)
            return list(result.all())
        except SQLAlchemyError as e:
            logger.error(f"Error fetching vms by group: {e}")
            await self.db.rollback()
            return []

    async def add_account_to_group(self, group_id: int, account_id: int) -> Optional[Group]:
        try:
            group = await self.get_by_id(group_id)
            account = await self.db.scalar(
                select(Account).where(Account.id == account_id)
            )

            if not group or not account or account in group.accounts:
                return None

            group.accounts.append(account)
            await self.db.commit()
            await self.db.refresh(group)
            return group
        except SQLAlchemyError as e:
            logger.error(f"Error adding account to group: {e}")
            await self.db.rollback()
            return None

    async def add_vm_to_group(self, group_id: int, vm_id: int) -> Optional[Group]:
        try:
            group = await self.get_by_id(group_id)
            vm = await self.db.scalar(
                select(VM).where(VM.id == vm_id)
            )

            if not group or not vm or vm in group.vms:
                return None

            group.vms.append(vm)
            await self.db.commit()
            await self.db.refresh(group)
            return group
        except SQLAlchemyError as e:
            logger.error(f"Error adding vm to group: {e}")
            await self.db.rollback()
            return None

    async def remove_account_from_group(self, group_id: int, account_id: int) -> Optional[Group]:
        try:
            group = await self.get_by_id(group_id)
            account = await self.db.scalar(
                select(Account).where(Account.id == account_id)
            )

            if not group or not account or account not in group.accounts:
                return None

            group.accounts.remove(account)
            await self.db.commit()
            await self.db.refresh(group)
            return group
        except SQLAlchemyError as e:
            logger.error(f"Error removing account from group: {e}")
            await self.db.rollback()
            return None

    async def remove_vm_from_group(self, group_id: int, vm_id: int) -> Optional[Group]:
        try:
            group = await self.get_by_id(group_id)
            vm = await self.db.scalar(
                select(VM).where(VM.id == vm_id)
            )

            if not group or not vm or vm not in group.vms:
                return None

            group.vms.remove(vm)
            await self.db.commit()
            await self.db.refresh(group)
            return group
        except SQLAlchemyError as e:
            logger.error(f"Error removing vm from group: {e}")
            await self.db.rollback()
            return None
