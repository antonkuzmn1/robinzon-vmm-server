from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Account
from app.models.group import m2m_group_account
from app.repositories.account_repo import AccountRepository
from app.schemas.account import AccountCreate, AccountOut, AccountUpdate
from app.schemas.group import GroupOut
from app.services.auth_service import AuthService
from app.services.base_service import BaseService
from app.utils.logger import logger


class AccountService(BaseService[AccountRepository]):
    def __init__(self, db: AsyncSession, auth_service: AuthService):
        super().__init__(AccountRepository(db), AccountOut)
        self.auth_service = auth_service

    async def create(self, item_data: AccountCreate) -> Optional[AccountOut]:
        logger.warning("ACCOUNT_SERVICE: Attempt to create account")

        item_data_dict = item_data.model_dump(exclude={"password"})
        item_data_dict["hashed_password"] = self.auth_service.hash_password(item_data.password)

        return await super().create(item_data_dict)

    async def update(self, item_id: int, item_data: AccountUpdate) -> Optional[AccountOut]:
        logger.warning("ACCOUNT_SERVICE: Attempt to update account")
        item = await self.repository.get_by_id(item_id)
        if not item:
            logger.warning(f"Attempt to update non-existent account: {item_id}")
            return None

        updated_item = item_data.model_dump(exclude_unset=True)
        if "password" in updated_item and updated_item["password"]:
            updated_item["hashed_password"] = self.auth_service.hash_password(updated_item["password"])
            del updated_item["password"]

        return await super().update(item_id, updated_item)

    async def get_all_accounts_by_account(self, current_account: AccountOut) -> list[AccountOut]:
        group_ids = [group.id for group in current_account.groups]
        if not group_ids:
            return []
        filters = [
            m2m_group_account.c.group_id.in_(group_ids),
            m2m_group_account.c.account_id == Account.id,
        ]
        return await super().get_all(*filters)

    async def get_account_by_id_by_account(self, item_id: int, current_account: AccountOut) -> Optional[AccountOut]:
        group_ids = [group.id for group in current_account.groups]
        if not group_ids:
            return None
        filters = [
            m2m_group_account.c.group_id.in_(group_ids),
            m2m_group_account.c.account_id == Account.id,
        ]
        return await super().get_by_id(item_id, *filters)

    async def get_all_accounts_by_group(self, current_group: GroupOut) -> list[AccountOut]:
        records = await self.repository.get_all_accounts_by_group(current_group.id)
        return [AccountOut.model_validate(record) for record in records]

    async def get_account_by_id_by_group(self, item_id: int, current_group: GroupOut) -> Optional[AccountOut]:
        filters = [
            m2m_group_account.c.group_id == current_group.id,
            m2m_group_account.c.account_id == Account.id,
        ]
        return await super().get_by_id(item_id, *filters)

    async def get_all_groups_by_account(self, current_account: AccountOut) -> list[GroupOut]:
        records = await self.repository.get_all_groups_by_account(current_account.id)
        return [GroupOut.model_validate(record) for record in records]

    async def add_group_to_account(self, account_id: int, group_id: int) -> Optional[AccountOut]:
        account = await self.repository.add_group_to_account(account_id, group_id)
        return AccountOut.model_validate(account) if account else None

    async def remove_group_from_account(self, account_id: int, group_id: int) -> Optional[AccountOut]:
        account = await self.repository.remove_group_from_account(account_id, group_id)
        return AccountOut.model_validate(account) if account else None

    async def authenticate_account(self, username: str, password: str) -> Optional[AccountOut]:
        account = await self.repository.get_by_username(username)
        if not account or not self.auth_service.verify_password(password, account.hashed_password):
            logger.warning(f"Failed to authenticate account: {username}")
            return None
        return AccountOut.model_validate(account) if account else None

    async def create_account_token(self, account: AccountOut) -> Optional[str]:
        if not account:
            return None
        token_data: dict = AccountOut.model_dump(account)
        return await self.auth_service.create_access_token(token_data)
