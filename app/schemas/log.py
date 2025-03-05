from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class LogBase(BaseModel):
    before: dict
    after: dict


class LogCreate(LogBase):
    pass


class LogUpdate(LogBase):
    pass


class LogOut(LogBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        model_config = ConfigDict(from_attributes=True)
