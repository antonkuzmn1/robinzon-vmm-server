from typing import Type, TypeVar, Generic, Optional, List

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.repositories.abstract_repo import AbstractRepository
from app.models import Base
from app.utils.logger import logger


T = TypeVar("T", bound=Base)


class BaseRepository(AbstractRepository[T], Generic[T]):
    def __init__(self, db: AsyncSession, model: Type[T]):
        self.db = db
        self.model = model

    async def get_by_username(self, username: str, *filters) -> Optional[T]:
        base_filters = [self.model.username == username, self.model.deleted.is_(False)]
        if filters:
            base_filters.extend(filters)
        stmt = select(self.model).where(*base_filters)
        return await self.db.scalar(stmt)

    async def get_all(self, *filters) -> List[T]:
        base_filters = [self.model.deleted.is_(False)]
        if filters:
            base_filters.extend(filters)
        stmt = select(self.model).where(*base_filters).distinct()
        result = await self.db.scalars(stmt)
        return list(result.all())

    async def get_by_id(self, item_id: int, *filters) -> Optional[T]:
        base_filters = [self.model.id == item_id, self.model.deleted.is_(False)]
        if filters:
            base_filters.extend(filters)
        stmt = select(self.model).where(*base_filters)
        return await self.db.scalar(stmt)

    async def create(self, item_data: dict) -> Optional[T]:
        logger.warning("BASE_REPO: Attempt to create something")
        item = self.model(**item_data)
        try:
            self.db.add(item)
            await self.db.commit()
            await self.db.refresh(item)
        except SQLAlchemyError as e:
            logger.error(f"Error creating item: {e}")
            await self.db.rollback()
            return None
        return item

    async def update(self, item_id: int, item_data: dict) -> Optional[T]:
        logger.warning("BASE_REPO: Attempt to update something")
        item = await self.get_by_id(item_id)
        if not item:
            return None

        for key, value in item_data.items():
            setattr(item, key, value)

        try:
            await self.db.commit()
            await self.db.refresh(item)
        except SQLAlchemyError as e:
            logger.error(f"Error updating item: {e}")
            await self.db.rollback()
            return None

        return item

    async def delete(self, item_id: int) -> Optional[T]:
        item = await self.get_by_id(item_id)
        if not item:
            return None

        item.deleted = True

        try:
            await self.db.commit()
            await self.db.refresh(item)
            return item
        except SQLAlchemyError as e:
            logger.error(f"Error deleting item: {e}")
            await self.db.rollback()
            return None