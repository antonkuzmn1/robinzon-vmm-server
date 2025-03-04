from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.schemas.company import CompanyOut


class AdminBase(BaseModel):
    username: str
    surname: str
    name: str
    middlename: Optional[str] = None
    department: Optional[str] = None
    phone: Optional[str] = None
    cellular: Optional[str] = None
    post: Optional[str] = None


class AdminCreate(AdminBase):
    password: str


class AdminUpdate(AdminBase):
    password: Optional[str] = None


class AdminOut(AdminBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    companies: list[CompanyOut] = []

    model_config = ConfigDict(from_attributes=True)