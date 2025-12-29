from mcp.client.session import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from typing import Any, Dict
from pydantic import AnyUrl
import json


class MCPClient:
    """MCP client to call tools, resources, and prompts."""

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
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.__aexit__(exc_type, exc_val, exc_tb)
        if self._http_client:
            await self._http_client.__aexit__(exc_type, exc_val, exc_tb)

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
