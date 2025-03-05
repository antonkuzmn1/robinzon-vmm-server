from typing import Optional, Sequence, cast

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Account, VM
from app.models.group import Group, m2m_group_vm
from app.repositories.base_repo import BaseRepository
from app.utils.logger import logger


class VMRepository(BaseRepository[VM]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, VM)

    async def get_all_vms_by_group(self, group_id: int) -> Sequence[VM]:
        try:
            stmt = (
                select(VM)
                .options(selectinload(VM.groups))
                .join(m2m_group_vm)
                .where(cast("ColumnElement[bool]", m2m_group_vm.c.group_id == group_id))
            )
            result = await self.db.scalars(stmt)
            return result.all()
        except SQLAlchemyError as e:
            logger.error(f"Error fetching vms by group: {e}")
            await self.db.rollback()
            return []

    async def get_all_groups_by_vm(self, vm_id: int) -> Sequence[Group]:
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

    async def add_group_to_vm(self, vm_id: int, group_id: int) -> Optional[VM]:
        try:
            vm = await self.get_by_id(vm_id)
            group = await self.db.scalar(
                select(Group).where(Group.id == group_id)
            )

            if not vm or not group or group in vm.groups:
                return None

            vm.groups.append(group)
            await self.db.commit()
            await self.db.refresh(vm)
            return vm
        except SQLAlchemyError as e:
            logger.error(f"Error adding group to vm: {e}")
            await self.db.rollback()
            return None

    async def remove_group_from_vm(self, vm_id: int, group_id: int) -> Optional[VM]:
        try:
            vm = await self.get_by_id(vm_id)
            group = await self.db.scalar(
                select(Group).where(Group.id == group_id)
            )

            if not vm or not group or group not in vm.groups:
                return None

            vm.groups.remove(group)
            await self.db.commit()
            await self.db.refresh(vm)
            return vm
        except SQLAlchemyError as e:
            logger.error(f"Error removing group from vm: {e}")
            await self.db.rollback()
            return None
