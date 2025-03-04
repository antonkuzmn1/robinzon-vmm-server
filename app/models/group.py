from sqlalchemy import Column, Integer, String, DateTime, func, Boolean, Text, Table, ForeignKey
from sqlalchemy.orm import relationship

from app.models import Base

m2m_group_account = Table(
    "m2m_group_account",
    Base.metadata,
    Column("group_id", ForeignKey("group.id"), primary_key=True),
    Column("account_id", ForeignKey("account.id"), primary_key=True),
)

m2m_group_vm = Table(
    "m2m_group_vm",
    Base.metadata,
    Column("group_id", ForeignKey("group.id"), primary_key=True),
    Column("vm_id", ForeignKey("vm.id"), primary_key=True),
)


class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted = Column(Boolean, default=False)

    name = Column(String(50), nullable=False)
    description = Column(Text, nullable=False, default='')

    accounts = relationship("Account", secondary=m2m_group_account, back_populates="groups")
    vms = relationship("VM", secondary=m2m_group_vm, back_populates="groups")
