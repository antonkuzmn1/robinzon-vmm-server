from sqlalchemy import Column, Integer, String, DateTime, func, Boolean
from sqlalchemy.orm import relationship

from app.models import Base
from app.models.admin import admin_company_association


class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False)
    description = Column(String(255), nullable=True, default=None)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted = Column(Boolean, default=False)

    admins = relationship("Admin", secondary=admin_company_association, back_populates="companies")
    users = relationship("app.models.user.User", back_populates="company")