from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tracer.config import DB_URL, LogDomain  # Get your path from config.py

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


def clear_domain_table(domain: str) -> str:
    """Clear all data from a specific table for the given domain."""
    # Validate domain
    valid_domains = [d.value for d in LogDomain]
    if domain not in valid_domains:
        raise ValueError(
            f"Invalid domain '{domain}'. Valid domains are: {', '.join(valid_domains)}"
        )

    from sqlalchemy import MetaData, delete

    # Get metadata and reflect existing tables
    metadata = MetaData()
    metadata.reflect(bind=engine)

    # Check if table exists
    table_name = domain  # Domain value maps directly to table name
    if table_name not in metadata.tables:
        raise ValueError(f"Table '{table_name}' does not exist for domain '{domain}'")

    # Get the table and clear all data
    table = metadata.tables[table_name]

    with engine.connect() as connection:
        result = connection.execute(delete(table))
        connection.commit()
        rows_deleted = result.rowcount

    return f"Successfully cleared {rows_deleted} rows from table '{table_name}' for domain '{domain}'"
