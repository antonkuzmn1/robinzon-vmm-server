from typing import Optional, List

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Config
from app.utils.logger import logger


class ConfigRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> List[Config]:
        try:
            result = await self.db.execute(select(Config))
            configs = result.scalars().all()
            return configs
        except SQLAlchemyError as e:
            logger.error(f"Failed to get all configs: {e}")
            await self.db.rollback()
            return []

    async def get_by_key(self, key: str) -> Optional[Config]:
        try:
            result = await self.db.execute(select(Config).filter(Config.key == key))
            config = result.scalars().first()
            return config
        except SQLAlchemyError as e:
            logger.error(f"Failed to get config by key={key}: {e}")
            await self.db.rollback()
            return None

    async def create(self, key: str, value: str) -> Optional[Config]:
        try:
            item = Config(key=key, value=value)
            self.db.add(item)
            await self.db.commit()
            await self.db.refresh(item)
            return item
        except SQLAlchemyError as e:
            logger.error(f"Failed to create config key={key}: {e}")
            await self.db.rollback()
            return None

    async def update(self, key: str, value: str) -> Optional[Config]:
        try:
            item = await self.get_by_key(key)
            if not item:
                return None

            item.value = value
            await self.db.commit()
            await self.db.refresh(item)
            return item
        except SQLAlchemyError as e:
            logger.error(f"Failed to update config key={key}: {e}")
            await self.db.rollback()
            return None

    async def delete(self, key: str) -> Optional[Config]:
        try:
            item = await self.get_by_key(key)
            if not item:
                return None

            await self.db.delete(item)
            await self.db.commit()
            await self.db.refresh(item)
            return item
        except SQLAlchemyError as e:
            logger.error(f"Failed to delete config key={key}: {e}")
            await self.db.rollback()
            return None
