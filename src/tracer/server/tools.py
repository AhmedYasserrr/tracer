import json
from sqlalchemy import text
from tracer.db.connection import engine, reset_db, drop_db, init_db
from tracer.tracer_core import TracerCore
from tracer.config import LogDomain


def execute_sql_query(sql_query: str) -> str:
    """Executes advanced SQL queries and returns results in JSON format."""
    try:
        with engine.connect() as connection:
            result = connection.execute(text(sql_query))

            if result.returns_rows:
                # Use result.mappings() for cleaner dict conversion in SQLAlchemy 2.0
                rows = [dict(row) for row in result.mappings()]

                if not rows:
                    return json.dumps(
                        {
                            "status": "success",
                            "message": "Query executed successfully. No rows returned.",
                            "data": [],
                        }
                    )

                # Returning JSON makes it easier for the LLM to parse
                return json.dumps(
                    {"status": "success", "data": rows}, indent=2, default=str
                )

            connection.commit()
            return json.dumps(
                {"status": "success", "message": f"Rows affected: {result.rowcount}"}
            )

    except Exception as e:
        # Return the error so the LLM can try to fix its own SQL syntax
        return json.dumps({"status": "error", "message": f"SQL Error: {str(e)}"})


def start_tracing(domain: str, directory: str = None) -> str:
    """Starts tracing for the specified domain and optional directory."""
    try:
        # Validate domain
        valid_domains = [d.value for d in LogDomain]
        if domain not in valid_domains:
            return json.dumps(
                {
                    "status": "error",
                    "message": f"Invalid domain '{domain}'. Valid domains are: {', '.join(valid_domains)}",
                }
            )

        # TracerCore will handle validation and return success message
        result = TracerCore.start_tracing(domain, directory)
        return json.dumps({"status": "success", "message": result})

    except Exception as e:
        return json.dumps(
            {"status": "error", "message": f"Error starting tracing: {str(e)}"}
        )


def stop_tracing(domain: str, directory: str = None) -> str:
    """Stops tracing for the specified domain and optional directory."""
    try:
        # Validate domain
        valid_domains = [d.value for d in LogDomain]
        if domain not in valid_domains:
            return json.dumps(
                {
                    "status": "error",
                    "message": f"Invalid domain '{domain}'. Valid domains are: {', '.join(valid_domains)}",
                }
            )

        # TracerCore will handle validation and return success message
        result = TracerCore.stop_tracing(domain, directory)
        return json.dumps({"status": "success", "message": result})

    except Exception as e:
        return json.dumps(
            {"status": "error", "message": f"Error stopping tracing: {str(e)}"}
        )


def list_tracers() -> str:
    """Returns JSON formatted list of all active tracers and their configurations."""
    try:
        # Use the new list_tracers method from TracerCore
        active_tracers_info = TracerCore.list_tracers()

        if not active_tracers_info:
            return json.dumps({"status": "success", "data": []})

        return json.dumps({"status": "success", "data": active_tracers_info}, indent=2)

    except Exception as e:
        return json.dumps(
            {"status": "error", "message": f"Error getting tracer status: {str(e)}"}
        )


def list_domains() -> str:
    """Returns JSON formatted list of all available tracing domains."""
    try:
        domains = [
            {
                "name": domain.value,
                "description": f"Tracing for {domain.value} activities",
            }
            for domain in LogDomain
        ]
        return json.dumps({"status": "success", "data": domains}, indent=2)
    except Exception as e:
        return json.dumps(
            {"status": "error", "message": f"Error listing domains: {str(e)}"}
        )


def clear_logs(domain: str) -> str:
    """Clears all logs for the specified domain."""
    try:
        # Validate domain
        valid_domains = [d.value for d in LogDomain]
        if domain not in valid_domains:
            return json.dumps(
                {
                    "status": "error",
                    "message": f"Invalid domain '{domain}'. Valid domains are: {', '.join(valid_domains)}",
                }
            )

        # TracerCore will handle validation and return success message
        result = TracerCore.clear_logs(domain)
        return json.dumps({"status": "success", "message": result})

    except Exception as e:
        return json.dumps(
            {"status": "error", "message": f"Error clearing logs: {str(e)}"}
        )


def initialize_database() -> str:
    """Initializes the database by creating all required tables."""
    try:
        init_db()
        return json.dumps(
            {
                "status": "success",
                "message": "Successfully initialized database and created all tables",
            }
        )
    except Exception as e:
        return json.dumps(
            {"status": "error", "message": f"Error initializing database: {str(e)}"}
        )


def reset_database() -> str:
    """Resets the database by dropping and recreating all tables."""
    try:
        reset_db()
        return json.dumps(
            {
                "status": "success",
                "message": "Successfully reset database - all tables dropped and recreated",
            }
        )
    except Exception as e:
        return json.dumps(
            {"status": "error", "message": f"Error resetting database: {str(e)}"}
        )


def drop_database() -> str:
    """Drops all tables in the database."""
    try:
        drop_db()
        return json.dumps(
            {"status": "success", "message": "Successfully dropped all database tables"}
        )
    except Exception as e:
        return json.dumps(
            {"status": "error", "message": f"Error dropping database: {str(e)}"}
        )
