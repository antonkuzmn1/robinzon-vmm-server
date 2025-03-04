from sqlalchemy import Column, Integer, String, DateTime, func, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.models import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(60), nullable=False)
    surname = Column(String(100), nullable=False)
    name = Column(String(100), nullable=False)
    middlename = Column(String(100), nullable=True)
    department = Column(String(100), nullable=True)
    remote_workplace = Column(String(20), nullable=True)
    local_workplace = Column(String(20), nullable=True)
    phone = Column(String(20), nullable=True)
    cellular = Column(String(20), nullable=True)
    post = Column(String(100), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted = Column(Boolean, default=False)

    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    company = relationship("Company", back_populates="users")