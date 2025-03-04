from sqlalchemy import Column, Integer, String, DateTime, func, Boolean, Text
from sqlalchemy.orm import relationship

from app.models import Base
from app.models.group import m2m_group_account


class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted = Column(Boolean, default=False)

    username = Column(String(50), unique=True, nullable=False)
    hashed_password = Column(String(60), nullable=False)
    surname = Column(String(100), nullable=False, default='')
    name = Column(String(100), nullable=False, default='')
    middlename = Column(String(100), nullable=False, default='')
    department = Column(String(100), nullable=False, default='')
    phone = Column(String(20), nullable=False, default='')
    cellular = Column(String(20), nullable=False, default='')
    post = Column(String(100), nullable=False, default='')
    description = Column(Text, nullable=False, default='')

    groups = relationship("Group", secondary=m2m_group_account, back_populates="accounts")
