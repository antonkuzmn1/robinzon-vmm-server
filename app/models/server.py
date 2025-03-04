from sqlalchemy import Column, Integer, String, DateTime, func, Boolean, Text
from sqlalchemy.orm import relationship

from app.models import Base


class Server(Base):
    __tablename__ = 'servers'

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted = Column(Boolean, default=False)

    ip_address = Column(String(15), nullable=False, default='')
    name = Column(String(50), nullable=False, default='')
    specs = Column(Text, nullable=False, default='')
    description = Column(Text, nullable=False, default='')
    username = Column(String(50), nullable=False, default='')
    password = Column(String(50), nullable=False, default='')

    vms = relationship('VM', backref='server', cascade="all, delete-orphan")
