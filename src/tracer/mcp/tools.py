import json
from sqlalchemy import text
from tracer.db.connection import engine  # Import your engine


def execute_sql_query(sql: str) -> str:
    """
    Executes advanced SQL queries including aggregations, bucketing, and joins.
    Returns results in a structured JSON format for precise analysis.
    """
    try:
        with engine.connect() as connection:
            result = connection.execute(text(sql))

            if result.returns_rows:
                # Use result.mappings() for cleaner dict conversion in SQLAlchemy 2.0
                rows = [dict(row) for row in result.mappings()]

                if not rows:
                    return "Query executed successfully. No rows returned."

                # Returning JSON makes it easier for the LLM to parse
                return json.dumps(rows, indent=2, default=str)

            connection.commit()
            return f"Success. Rows affected: {result.rowcount}"

    except Exception as e:
        # Return the error so the LLM can try to fix its own SQL syntax
        return f"SQL Error: {str(e)}"
