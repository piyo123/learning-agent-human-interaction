
import asyncio
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from html import escape
from mcp import Client
from mcp.client import advertise
from mcp.server.apps import APP_MIME_TYPE, EXTENSION_ID

from server import mcp # server.py

app = FastAPI()

async def load_app():
    # MCP Client をインメモリ接続
    # Communicate with MCP Server via In-Memory this time.
    async with Client(
        mcp,
        extensions=[
            advertise(
                EXTENSION_ID,
                {"mimeTypes": [APP_MIME_TYPE]},
            )
        ],
    ) as client:

        # 1. Tool 一覧取得 / List tools available
        tools = await client.list_tools()
        tool = next(t for t in tools.tools if t.name == "say_hello")
        print("Tool:", tool.name)
        print("Metadata:", tool.meta)

        # 2. Tool に関連付けられた UI Resource URIを取得 / Retrieve UI Resource URI associated with the tool
        resource_uri = tool.meta["ui"]["resourceUri"]
        print("UI Resource URI:", resource_uri)

        # 3. UI Resource から HTML を取得 / Read HTML from the UI Resource
        resource = await client.read_resource(resource_uri)
        html = resource.contents[0].text
        print("Resource:", resource)

        # 4. Toolを実行 / Execute the tool
        result = await client.call_tool("say_hello", {})
        result_text = result.content[0].text

        return html, result_text


@app.get("/", response_class=HTMLResponse)
async def index():
    app_html, tool_result = await load_app()

    page = f"""
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <title>My MCP Host</title>
    </head>
    <body>
        <h1>My MCP Host</h1>

        <h2>MCP App UI</h2>
        <iframe
            sandbox=""
            srcdoc="{escape(app_html, quote=True)}"
            width="600"
            height="200">
        </iframe>

        <h2>Tool Result</h2>
        <pre>{escape(tool_result)}</pre>
    </body>
    </html>
    """

    return page

# Main
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
