from sqlalchemy import inspect
from tracer.db.models import FileLog

def _generate_schema_description(model) -> str:
    """Helper to extract table info from a SQLAlchemy model."""
    mapper = inspect(model)
    table_name = mapper.tables[0].name
    
    lines = [f"Table: {table_name}", "Columns:"]
    
    for column in mapper.attrs:
        # Get column name and its Python type
        col_name = column.key
        col_type = str(column.columns[0].type)
        
        # Check if it has a docstring or specific constraints
        nullable = " (Nullable)" if column.columns[0].nullable else ""
        lines.append(f"- {col_name}: {col_type}{nullable}")
        
    return "\n".join(lines)

def get_filesystem_schema() -> str:
    """Returns the live schema for the filesystem logs directly from the DB model."""
    return _generate_schema_description(FileLog)