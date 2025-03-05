from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Version
from app.repositories.base_repo import BaseRepository


class VersionRepository(BaseRepository[Version]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Version)
