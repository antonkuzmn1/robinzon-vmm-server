from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class AccountBase(BaseModel):
    username: str
    surname: str = ''
    name: str = ''
    middlename: str = ''
    department: str = ''
    phone: str = ''
    cellular: str = ''
    post: str = ''
    description: str = ''


class AccountCreate(AccountBase):
    password: str


class AccountUpdate(AccountBase):
    password: str = ''


class AccountOut(AccountBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        model_config = ConfigDict(from_attributes=True)
