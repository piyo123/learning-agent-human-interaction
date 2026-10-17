
import asyncio
from mcp import Client
from mcp.client import advertise
from mcp.server.apps import APP_MIME_TYPE, EXTENSION_ID

from server import mcp, RESOURCE_URI # server.py


async def main():
    async with Client(
        mcp,    # Communicate with MCP Server via In-Memory this time.
        extensions=[
            advertise(
                EXTENSION_ID,
                {"mimeTypes": [APP_MIME_TYPE]},
            )
        ],
    ) as client:

        # 1. Tool 一覧取得 / List tools available
        tools = await client.list_tools()
        for tool in tools.tools:
            print("Tool:", tool.name)
            print("Metadata:", tool.meta)

        # 2. UI Resource の取得 / Read a resource
        resource = await client.read_resource(RESOURCE_URI)
        print("Resource:", resource)

        # 3. Tool の実行 / Execute the tool
        result = await client.call_tool("say_hello", {})
        print("Result:", result.content)


if __name__ == "__main__":
    asyncio.run(main())
