from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class OwnerBase(BaseModel):
    username: str


class OwnerCreate(OwnerBase):
    password: str


class OwnerUpdate(OwnerBase):
    password: Optional[str] = None


class OwnerOut(OwnerBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)