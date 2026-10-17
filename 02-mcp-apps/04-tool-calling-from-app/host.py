import uvicorn
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from mcp import Client
from mcp.client import advertise
from mcp.server.apps import APP_MIME_TYPE, EXTENSION_ID

from server import mcp # server.py


app = FastAPI()
base = Path(__file__).parent


class MyToolCallRequest(BaseModel):
    name: str
    arguments: dict = Field(default_factory=dict)

async def load_app():
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

        return { "html": html }

# Host Web Root
@app.get("/")
async def index():
    return FileResponse(base / "host.html")


# JavaScript to be loaded in Host page
@app.get("/host.bundle.js")
async def host_script():
    return FileResponse(
        base / "host.bundle.js",
        media_type="application/javascript"
    )


# Receive UI and tool result from MCP Server
@app.get("/payload")
async def payload():
    return await load_app()


# Endpoint of Tool Call
@app.post("/call-tool")
async def call_tool(request: MyToolCallRequest):
    
    # 学習のため許可するToolを限定する
    # 
    if request.name != "say_hello":
        raise HTTPException(
            status_code=403,
            detail="Tool not allowed"
        )

    async with Client(
        mcp,
        extensions=[
            advertise(
                EXTENSION_ID,
                {"mimeTypes": [APP_MIME_TYPE]},
            )
        ],
    ) as client:

        result = await client.call_tool(
            request.name,
            request.arguments
        )

        print(f"[Host Backend] Tool called: {request.name}")

        return result.model_dump(
            mode="json",
            by_alias=True,
            exclude_none=True
        )



# Main
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
