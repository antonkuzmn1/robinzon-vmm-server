from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.config_repo import ConfigRepository
from app.schemas.config import ConfigOut, ConfigCreate, ConfigUpdate


class ConfigService:
    def __init__(self, db: AsyncSession):
        repo = ConfigRepository(db)
        self.repository = repo
        self.schema_out = ConfigOut

    async def get_all(self) -> List[ConfigOut]:
        records = await self.repository.get_all()
        return [self.schema_out.model_validate(record) for record in records]

    async def get_by_key(self, key: str) -> Optional[ConfigOut]:
        record = await self.repository.get_by_key(key)
        if record:
            return self.schema_out.model_validate(record)
        return None

    async def create(self, config: ConfigCreate) -> ConfigOut:
        record = await self.repository.create(key=config.key, value=config.value)
        return self.schema_out.model_validate(record)

    async def update(self, key: str, config: ConfigUpdate) -> Optional[ConfigOut]:
        record = await self.repository.update(key=key, value=config.value)
        if record:
            return self.schema_out.model_validate(record)
        return None

    async def delete(self, key: str) -> Optional[ConfigOut]:
        record = await self.repository.delete(key=key)
        if record:
            return self.schema_out.model_validate(record)
        return None
