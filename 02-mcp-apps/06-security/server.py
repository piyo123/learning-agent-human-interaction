from pathlib import Path
from mcp.server.apps import Apps
from mcp.server.mcpserver import MCPServer

# UI Resource を識別する URI
# Resource Identifier for UI Resource
RESOURCE_URI = "ui://hello/app.html"

# HTML、JS を読み込む
# Read HTML and javascript
base = Path(__file__).parent

html = (base / "app.html").read_text(encoding="utf-8")
js = (base / "app.bundle.js").read_text(encoding="utf-8")

html = html.replace(
    "<!-- APP_SCRIPT -->",
    f"<script>{js}</script>"
)

# MCP Apps Extension
apps = Apps()


# UI に関連付ける Tool
# Tool to be associated with UI
@apps.tool(
    resource_uri=RESOURCE_URI,
    description="Say hello to the user.",
)
def say_hello(name: str = "") -> str:
    if name:
        return f"Hello {name}!"
    
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
