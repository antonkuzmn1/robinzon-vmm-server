from sqlalchemy import Column, Integer, String, DateTime, func, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.models import Base
from app.models.group import m2m_group_vm


class VM(Base):
    __tablename__ = 'vms'

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted = Column(Boolean, default=False)

    name = Column(String(50), nullable=False, default='')
    cpu = Column(Integer, nullable=False, default=0)
    ram = Column(Integer, nullable=False, default=0)
    ssd = Column(Integer, nullable=False, default=0)
    hdd = Column(Integer, nullable=False, default=0)
    state = Column(Boolean, nullable=False, default=False)

    description = Column(Text, nullable=False, default='')
    ip_address = Column(String(15), nullable=False, default='')
    username = Column(String(50), nullable=False, default='')
    password = Column(String(50), nullable=False, default='')

    server_id = Column(Integer, ForeignKey('servers.id'), nullable=False)
    groups = relationship("Group", secondary=m2m_group_vm, back_populates="vms")
