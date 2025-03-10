from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.version_repo import VersionRepository
from app.schemas.version import VersionOut
from app.services.base_service import BaseService


class VersionService(BaseService[VersionRepository]):
    def __init__(self, db: AsyncSession):
        super().__init__(VersionRepository(db), VersionOut)
