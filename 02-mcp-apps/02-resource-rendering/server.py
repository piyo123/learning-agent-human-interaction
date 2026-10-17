from pathlib import Path
from mcp.server.apps import Apps
from mcp.server.mcpserver import MCPServer

# UI Resource を識別する URI
# Resource Identifier for UI Resource
RESOURCE_URI = "ui://hello/app.html"

# HTMLを読み込む
# Read HTML
html = Path(__file__).with_name("app.html").read_text(encoding="utf-8")

# MCP Apps Extension
apps = Apps()


# UI に関連付ける Tool
# Tool to be associated with UI
@apps.tool(
    resource_uri=RESOURCE_URI,
    description="Say hello to the user.",
)
def say_hello() -> str:
    return "Hello from MCP Server!"


# HTMLをUI Resourceとして登録
# Register HTML as UI Resource
apps.add_html_resource(
    RESOURCE_URI,
    html,
    title="Hello MCP App",
)

# MCP Serverを作成
# Create MCP Server
mcp = MCPServer(
    "hello-mcp-app",
    extensions=[apps],
)
