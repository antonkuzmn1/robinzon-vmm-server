from sqlalchemy import Column, Integer, DateTime, func, JSON

from app.models import Base


class Log(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True, index=True)
    before = Column(JSON, nullable=False)
    after = Column(JSON, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
