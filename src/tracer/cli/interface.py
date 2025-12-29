from typing import Any, Dict, Optional
from .client import MCPClient
import asyncio
import json


class CommandInterface:
    """Interface class that wraps MCP tool calls for tracer functionality"""

    @staticmethod
    async def execute_sql_query(client: MCPClient, sql_query: str) -> Dict[str, Any]:
        """Executes advanced SQL queries and returns results in JSON format"""
        arguments = {"sql_query": sql_query}
        result = await client.call_tool("execute_sql_query", arguments)
        return result

    @staticmethod
    async def start_tracing(
        client: MCPClient, domain: str, directory: Optional[str] = None
    ) -> Dict[str, Any]:
        """Starts tracing for the specified domain and optional directory"""
        arguments = {"domain": domain}
        if directory is not None:
            arguments["directory"] = directory
        result = await client.call_tool("start_tracing", arguments)
        return result

    @staticmethod
    async def stop_tracing(
        client: MCPClient, domain: str, directory: Optional[str] = None
    ) -> Dict[str, Any]:
        """Stops tracing for the specified domain and optional directory"""
        arguments = {"domain": domain}
        if directory is not None:
            arguments["directory"] = directory
        result = await client.call_tool("stop_tracing", arguments)
        return result

    @staticmethod
    async def list_tracers(client: MCPClient) -> Dict[str, Any]:
        """Returns JSON formatted list of all active tracers and their configurations"""
        result = await client.call_tool("list_tracers", {})
        return result

    @staticmethod
    async def list_domains(client: MCPClient) -> Dict[str, Any]:
        """Returns JSON formatted list of all available tracing domains"""
        result = await client.call_tool("list_domains", {})
        return result

    @staticmethod
    async def clear_logs(client: MCPClient, domain: str) -> Dict[str, Any]:
        """Clears all logs for the specified domain"""
        arguments = {"domain": domain}
        result = await client.call_tool("clear_logs", arguments)
        return result

    @staticmethod
    async def reset_database(client: MCPClient) -> Dict[str, Any]:
        """Resets the database by dropping and recreating all tables"""
        result = await client.call_tool("reset_database", {})
        return result

    @staticmethod
    async def show_logs(client: MCPClient, domain: str) -> Dict[str, Any]:
        """Executes advanced SQL queries and returns results in JSON format"""
        arguments = {
            "sql_query": f"SELECT * FROM {domain} ORDER BY timestamp DESC LIMIT 10"
        }
        result = await client.call_tool("execute_sql_query", arguments)
        return result

    @staticmethod
    async def read_db_table(client: MCPClient, domain: str):
        """Reads database table contents using MCP resource"""
        uri = f"schema://{domain}"
        result = await client.read_resource(uri)
        formatted_table = json.loads(result)
        for item in formatted_table:
            print(f"URI: {item['uri']}")
            print(item["text"])
            print("*" * 20)
            await asyncio.sleep(0)  # Allow other coroutines to run
