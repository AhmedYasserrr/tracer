from mcp.server.fastmcp import FastMCP
from tracer.mcp import tools
from tracer.mcp import resources
from tracer.config import LogDomain

# Create the MCP server
mcp = FastMCP(
    "Streamable HTTP Demo",
    host="127.0.0.1",
    port=8080,
)

# --- Register Tools ---
mcp.tool()(tools.execute_sql_query)

# --- Register Resources ---
mcp.resource(f"schema://{LogDomain.FS}")(resources.get_filesystem_schema)

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
