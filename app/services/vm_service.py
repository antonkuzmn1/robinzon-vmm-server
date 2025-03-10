from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.vm_repo import VMRepository
from app.schemas.group import GroupOut
from app.schemas.vm import VMOut
from app.services.base_service import BaseService


class VMService(BaseService[VMRepository]):
    def __init__(self, db: AsyncSession):
        super().__init__(VMRepository(db), VMOut)

    async def get_all_vms_by_group(self, current_group: GroupOut) -> list[VMOut]:
        records = await self.repository.get_all_vms_by_group(current_group.id)
        return [VMOut.model_validate(record) for record in records]

    async def get_all_groups_by_vm(self, current_vm: VMOut) -> list[GroupOut]:
        records = await self.repository.get_all_groups_by_vm(current_vm.id)
        return [GroupOut.model_validate(record) for record in records]

    async def add_group_to_vm(self, group: GroupOut, vm: VMOut) -> Optional[VMOut]:
        vm = await self.repository.add_group_to_vm(group.id, vm.id)
        return VMOut.model_validate(vm) if vm else None

    async def remove_group_from_vm(self, group: GroupOut, vm: VMOut) -> Optional[VMOut]:
        vm = await self.repository.remove_group_from_vm(group.id, vm.id)
        return VMOut.model_validate(vm) if vm else None
