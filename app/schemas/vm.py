from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class VMBase(BaseModel):
    name: str = ''
    cpu: int = 0
    ram: int = 0
    ssd: int = 0
    hdd: int = 0
    state: bool = False
    description: str = ''
    ip_address: str = ''
    username: str = ''
    password: str = ''


class VMOut(VMBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        model_config = ConfigDict(from_attributes=True)
