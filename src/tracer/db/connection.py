from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tracer.config import DB_URL  # Get your path from config.py

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    # This creates the tables if they don't exist
    from tracer.db.models import Base

    Base.metadata.create_all(bind=engine)


def reset_db():
    """
    Delete all tables and recreate them
    WARNING: This will delete all data in the database!
    """
    from tracer.db.models import Base

    # Drop all tables
    Base.metadata.drop_all(bind=engine)

    # Recreate all tables
    Base.metadata.create_all(bind=engine)


def drop_db():
    """
    Drop all tables in the database
    WARNING: This will delete all data in the database!
    """
    from tracer.db.models import Base

    Base.metadata.drop_all(bind=engine)


if __name__ == "__main__":
    init_db()
