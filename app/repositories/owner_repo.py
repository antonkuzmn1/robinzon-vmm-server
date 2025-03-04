from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Owner
from app.repositories.base_repo import BaseRepository


class OwnerRepository(BaseRepository[Owner]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Owner)