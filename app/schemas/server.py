from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ServerBase(BaseModel):
    ip_address: str = ''
    name: str = ''
    specs: str = ''
    description: str = ''
    username: str = ''
    password: str = ''


class ServerCreate(ServerBase):
    pass


class ServerUpdate(ServerBase):
    pass


class ServerOut(ServerBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        model_config = ConfigDict(from_attributes=True)
