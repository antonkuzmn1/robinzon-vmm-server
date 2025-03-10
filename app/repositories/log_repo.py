from typing import Optional

from sqlalchemy import select, Sequence
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Log
from app.utils.logger import logger


class LogRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> list[Log]:
        try:
            result = await self.db.execute(select(Log))
            configs = list(result.scalars().all())
            return configs
        except SQLAlchemyError as e:
            logger.error(f"Failed to get all logs: {e}")
            await self.db.rollback()
            return []

    async def get_by_id(self, log_id: int) -> Optional[Log]:
        try:
            result = await self.db.execute(select(Log).filter(Log.id == log_id))
            config = result.scalars().first()
            return config
        except SQLAlchemyError as e:
            logger.error(f"Failed to get log by log_id={log_id}: {e}")
            await self.db.rollback()
            return None

    async def create(self, before: dict, after: dict) -> Optional[Log]:
        try:
            item = Log(before=before, after=after)
            self.db.add(item)
            await self.db.commit()
            await self.db.refresh(item)
            return item
        except SQLAlchemyError as e:
            logger.error(f"Failed to create log: {e}")
            await self.db.rollback()
            return None
