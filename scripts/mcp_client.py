import asyncio
from mcp.client.session import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from typing import Any, Dict

from pydantic import AnyUrl
import json


class MinimalMCPClient:
    """Minimal MCP client to call tools, resources, and prompts."""

    def __init__(self, server_url: str):
        self.server_url = server_url
        self.session: ClientSession | None = None
        self._http_client = None

    async def __aenter__(self):
        self._http_client = streamablehttp_client(self.server_url)
        read_stream, write_stream, get_session_id = await self._http_client.__aenter__()

        self.session = ClientSession(read_stream, write_stream)
        await self.session.__aenter__()
        await self.session.initialize()

        # Optional: get session ID
        if get_session_id:
            session_id = get_session_id()
            if session_id:
                print(f"Connected. Session ID: {session_id}")

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.__aexit__(exc_type, exc_val, exc_tb)
        if self._http_client:
            await self._http_client.__aexit__(exc_type, exc_val, exc_tb)

    # ------------------- Tools -------------------
    async def list_tools(self) -> Any:
        if not self.session:
            raise RuntimeError("Not connected")
        tools_result = await self.session.list_tools()
        formatted_tools = []
        for t in tools_result.tools:
            formatted_tools.append(
                {
                    "name": t.name,
                    "description": (t.description or "").strip(),
                    "input": {
                        k: v.get("type")
                        for k, v in (
                            t.inputSchema.get("properties", {}) if t.inputSchema else {}
                        ).items()
                    },
                    "output": {
                        k: v.get("type")
                        for k, v in (
                            t.outputSchema.get("properties", {})
                            if t.outputSchema
                            else {}
                        ).items()
                    },
                }
            )
        data = json.dumps(formatted_tools, indent=2)  # pretty-print JSON
        return data

    async def call_tool(
        self, name: str, arguments: Dict[str, Any] | None = None
    ) -> Any:
        if not self.session:
            raise RuntimeError("Not connected")
        result = await self.session.call_tool(name, arguments)
        result = result.content[0].text  # get the text inside TextContent
        result = json.loads(result)  # parse JSON string
        result = json.dumps(result, indent=2)  # pretty-print JSON
        return result

    # ------------------- Prompts -------------------
    async def list_prompts(self) -> Any:
        if not self.session:
            raise RuntimeError("Not connected")
        return await self.session.list_prompts()

    async def get_prompt(
        self, name: str, arguments: Dict[str, str] | None = None
    ) -> Any:
        if not self.session:
            raise RuntimeError("Not connected")
        return await self.session.get_prompt(name, arguments)

    async def complete(
        self,
        ref: Any,
        argument: Dict[str, str],
        context_arguments: Dict[str, str] | None = None,
    ) -> Any:
        if not self.session:
            raise RuntimeError("Not connected")
        return await self.session.complete(ref, argument, context_arguments)

    # ------------------- Resources -------------------
    async def list_resources(self) -> str:
        if not self.session:
            raise RuntimeError("Not connected")

        resources_result = await self.session.list_resources()
        formatted_resources = []

        for r in resources_result.resources:
            formatted_resources.append(
                {
                    "name": r.name,
                    "uri": str(r.uri) if r.uri else None,
                    "description": (r.description or "").strip(),
                    "mimeType": r.mimeType,
                }
            )

        return json.dumps(formatted_resources, indent=2)

    async def read_resource(self, uri: AnyUrl) -> Any:
        if not self.session:
            raise RuntimeError("Not connected")
        resource = await self.session.read_resource(uri)
        formatted = []
        for c in getattr(resource, "contents", []):
            formatted.append(
                {
                    "uri": str(c.uri),
                    "mimeType": c.mimeType,
                    "text": c.text,
                }
            )
        return json.dumps(formatted, indent=2)

    async def subscribe_resource(self, uri: AnyUrl) -> Any:
        if not self.session:
            raise RuntimeError("Not connected")
        return await self.session.subscribe_resource(uri)

    async def unsubscribe_resource(self, uri: AnyUrl) -> Any:
        if not self.session:
            raise RuntimeError("Not connected")
        return await self.session.unsubscribe_resource(uri)


async def main():
    try:
        async with MinimalMCPClient("http://127.0.0.1:9999/mcp") as client:
            # List tools
            print("Listing tools...")
            tools = await client.list_tools()
            print("Tools:", tools)
            print("*" * 20)

            # Call a tool
            result = await client.call_tool(
                "execute_sql_query", {"sql_query": "SELECT * FROM file_system limit 4"}
            )
            print(result)
            print("*" * 20)

            result = await client.call_tool("list_tracers", {})
            print(result)
            print("*" * 20)
            result = await client.call_tool("list_domains", {})
            print(result)
            print("*" * 20)

            result = await client.call_tool(
                "start_tracing", {"domain": "file_system", "directory": "E:\test"}
            )
            print(result)
            print("*" * 20)

            result = await client.call_tool("initialize_database", {})
            print(result)
            print("*" * 20)

            # read a resource
            formatted_table = await client.read_resource(AnyUrl("schema://file_system"))
            formatted_table = json.loads(formatted_table)
            for item in formatted_table:
                print(f"URI: {item['uri']}")
                print(f"MIME: {item['mimeType']}")
                print("Text:")
                print(item["text"])
                print("*" * 20)
                await asyncio.sleep(0)  # Allow other coroutines to run

            # List resources
            print("Listing resources...")
            resources = await client.list_resources()
            print("Resources:", resources)

    except Exception as e:
        print(f"Error occurred: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
