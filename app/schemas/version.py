from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class VersionBase(BaseModel):
    title: str = ''
    text: str = ''


class VersionCreate(VersionBase):
    pass


class VersionUpdate(VersionBase):
    pass


class VersionOut(VersionBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        model_config = ConfigDict(from_attributes=True)
