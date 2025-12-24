from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime

class Base(DeclarativeBase):
    pass

class FileLog(Base):
    __tablename__ = "file_system"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    file_path = Column(String)
    action = Column(String)