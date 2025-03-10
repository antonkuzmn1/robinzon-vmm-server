from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.log_repo import LogRepository
from app.schemas.log import LogOut


class ConfigService:
    def __init__(self, db: AsyncSession):
        repo = LogRepository(db)
        self.repository = repo
        self.schema_out = LogOut

    async def get_all(self) -> list[LogOut]:
        records = await self.repository.get_all()
        return [self.schema_out.model_validate(record) for record in records]

    async def get_by_id(self, item_id: int) -> Optional[LogOut]:
        record = await self.repository.get_by_id(item_id)
        if record:
            return self.schema_out.model_validate(record)
        return None

    async def create(self, before: dict, after: dict) -> Optional[LogOut]:
        record = await self.repository.create(before, after)
        return self.schema_out.model_validate(record)
