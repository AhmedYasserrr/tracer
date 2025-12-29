from mcp.server.fastmcp import FastMCP
from tracer.server import tools
from tracer.server import resources
from tracer.config import LogDomain

# Create the MCP server
mcp = FastMCP(
    "Streamable HTTP Demo",
    host="127.0.0.1",
    port=9999,
)

# --- Register Tools ---
mcp.tool()(tools.execute_sql_query)
mcp.tool()(tools.start_tracing)
mcp.tool()(tools.stop_tracing)
mcp.tool()(tools.list_tracers)
mcp.tool()(tools.list_domains)
mcp.tool()(tools.clear_logs)
mcp.tool()(tools.initialize_database)
mcp.tool()(tools.reset_database)
mcp.tool()(tools.drop_database)

# --- Register Resources ---
mcp.resource(f"schema://{LogDomain.FS}")(resources.get_filesystem_schema)


def main():
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()
