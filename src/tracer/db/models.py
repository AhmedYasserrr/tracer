from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime


class Base(DeclarativeBase):
    pass


class FileLog(Base):
    __tablename__ = "file_system"

    id = Column(Integer, primary_key=True)
    event = Column(String, nullable=False)
    name = Column(String, nullable=False)
    is_directory = Column(Boolean, default=False)
    full_path = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
