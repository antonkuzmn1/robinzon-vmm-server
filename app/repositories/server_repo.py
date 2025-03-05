from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Server
from app.repositories.base_repo import BaseRepository


class ServerRepository(BaseRepository[Server]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Server)
