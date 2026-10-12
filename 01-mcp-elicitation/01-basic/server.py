from typing import Annotated
from pydantic import BaseModel, Field
from mcp.server.mcpserver import MCPServer, Elicit, Resolve

# Logging Middleware for MCP Server
async def log_mcp_messages(ctx, call_next):
    if ctx.method == "tools/call":
        print()
        print(">>> MCP REQUEST")
        print(f"request_id: {ctx.request_id}")
        print(f"params: {ctx.params}")

    result = await call_next(ctx)

    if ctx.method == "tools/call":
        print()
        print("<<< MCP RESPONSE")
        print(f"result type: {type(result)}")
        print(f"result: {result}")
        print(f"resultType: {result.get('resultType')}")

    return result

# MCP Server
mcp = MCPServer(
    "elicitation-demo",
    middleware=[log_mcp_messages],
)

# Elicitationでユーザーから受け取るデータ
# Data that this server will receive from a user when elicitation
class MyConfirmation(BaseModel):
    confirm: bool = Field(
        description="Do you want to continue?"
    )


# Resolver
async def ask_confirmation(item: str) -> Elicit[MyConfirmation]:
    print("\n** Resolver `ask_confirmation` was called.\n")
    #  ユーザーへの確認要求を生成/Create a confirmation request to a user
    return Elicit(
        f"Do you want to order '{item}'?",
        MyConfirmation,
    )


# MCP Tool
@mcp.tool()
async def order_item(
    item: str,
    confirmation: Annotated[
        # type of member "confirmation"
        MyConfirmation,
        # metadata of member "confirmation".
        # This tells the MCP server to use the specified resolver, `ask_confirmation`, 
        # to resolve the value of `confirmation` instead of taking it directly from the tool call arguments.
        Resolve(ask_confirmation),
    ],
) -> str:

    print("\n** Tool `order_item` was executed.\n")
    print(f"\n\t** Received confirmation: {confirmation.confirm}.\n")
    
    if not confirmation.confirm:
        return "Order cancelled."

    return f"Ordered: {item}"


# Streamable HTTPでMCP Serverを起動
# Start MCP Server with Streamable HTTP protocol
if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="127.0.0.1",
        port=8000,
    )