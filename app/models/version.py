from sqlalchemy import Column, Integer, String, DateTime, func, Boolean, Text

from app.models import Base


class Version(Base):
    __tablename__ = 'versions'

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted = Column(Boolean, default=False)

    title = Column(String(255), nullable=False, default='')
    text = Column(Text, nullable=False, default='')
