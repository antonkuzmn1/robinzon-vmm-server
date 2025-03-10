from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.group_repo import GroupRepository
from app.schemas.account import AccountOut
from app.schemas.group import GroupOut
from app.schemas.vm import VMOut
from app.services.base_service import BaseService


class GroupService(BaseService[GroupRepository]):
    def __init__(self, db: AsyncSession):
        super().__init__(GroupRepository(db), GroupOut)

    async def get_all_groups_by_account(self, current_account: AccountOut) -> list[GroupOut]:
        records = await self.repository.get_all_groups_by_account(current_account.id)
        return [GroupOut.model_validate(record) for record in records]

    async def get_all_groups_by_vm(self, current_vm: VMOut) -> list[GroupOut]:
        records = await self.repository.get_all_groups_by_vm(current_vm.id)
        return [GroupOut.model_validate(record) for record in records]

    async def get_all_accounts_by_group(self, current_group: GroupOut) -> list[AccountOut]:
        records = await self.repository.get_all_accounts_by_group(current_group.id)
        return [AccountOut.model_validate(record) for record in records]

    async def get_all_vms_by_group(self, current_group: GroupOut) -> list[VMOut]:
        records = await self.repository.get_all_vms_by_group(current_group.id)
        return [VMOut.model_validate(record) for record in records]

    async def add_account_to_group(self, group: GroupOut, account: AccountOut) -> Optional[GroupOut]:
        group = await self.repository.add_account_to_group(group.id, account.id)
        return GroupOut.model_validate(group) if group else None

    async def add_vm_to_group(self, group: GroupOut, vm: VMOut) -> Optional[GroupOut]:
        group = await self.repository.add_vm_to_group(group.id, vm.id)
        return GroupOut.model_validate(group) if group else None

    async def remove_account_from_group(self, group: GroupOut, account: AccountOut) -> Optional[GroupOut]:
        group = await self.repository.remove_account_from_group(group.id, account.id)
        return GroupOut.model_validate(group) if group else None

    async def remove_vm_from_group(self, group: GroupOut, vm: VMOut) -> Optional[GroupOut]:
        group = await self.repository.remove_vm_from_group(group.id, vm.id)
        return GroupOut.model_validate(group) if group else None