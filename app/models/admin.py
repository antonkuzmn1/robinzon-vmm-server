from sqlalchemy import Column, Integer, String, DateTime, func, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship

from app.models import Base

admin_company_association = Table(
    "admin_company_association",
    Base.metadata,
    Column("admin_id", ForeignKey("admins.id"), primary_key=True),
    Column("company_id", ForeignKey("companies.id"), primary_key=True),
)


class Admin(Base):
    __tablename__ = 'admins'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    hashed_password = Column(String(60), nullable=False)
    surname = Column(String(100), nullable=False)
    name = Column(String(100), nullable=False)
    middlename = Column(String(100), nullable=True)
    department = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)
    cellular = Column(String(20), nullable=True)
    post = Column(String(100), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted = Column(Boolean, default=False)

    companies = relationship("Company", secondary=admin_company_association, back_populates="admins")
