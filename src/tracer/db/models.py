from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, BigInteger
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


class NetworkLog(Base):
    __tablename__ = "network"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    download = Column(Float, nullable=True)  # Download speed in Mbps
    upload = Column(Float, nullable=True)  # Upload speed in Mbps
    ping_ms = Column(Float, nullable=True)  # Ping latency in milliseconds
    packet_loss = Column(Float, nullable=True)  # Packet loss percentage
    bytes_sent = Column(BigInteger, nullable=True)  # Total bytes sent
    bytes_recv = Column(BigInteger, nullable=True)  # Total bytes received
    public_ip = Column(String, nullable=True)  # Public IP address
