from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tracer.config import DB_URL # Get your path from config.py

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    # This creates the tables if they don't exist
    from tracer.db.models import Base
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()