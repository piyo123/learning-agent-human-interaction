import json
from typing import Annotated, Literal
from pydantic import BaseModel, Field
from mcp.server.mcpserver import MCPServer, Elicit, Resolve

# Logging Middleware for MCP Server
async def log_mcp_messages(ctx, call_next):
    if ctx.method == "tools/call":
        print()
        print(">>> MCP REQUEST")
        print(f"request_id: {ctx.request_id}")
        print(f"params:\n {json.dumps(ctx.params, indent=2, ensure_ascii=False)}")

    result = await call_next(ctx)

    if ctx.method == "tools/call":
        print()
        print("<<< MCP RESPONSE")
        print(f"result type: {type(result)}")
        print(f"result:\n {json.dumps(result, indent=2, ensure_ascii=False)}")
        print()
        print(f"******* resultType: {result.get('resultType')}")

    return result

# MCP Server
mcp = MCPServer(
    "elicitation-demo",
    middleware=[log_mcp_messages],
)

# Elicitationでユーザーから受け取るデータ
# Data that this server will receive from a user when elicitation
class MyConfirmation(BaseModel):
    confirm: bool = Field(description="Do you want to continue?")
    
    quantity: int = Field(description="How many would you like?")
    
    flavor: Literal[
        "mitarashi",
        "anko",
        "kinako",
    ] = Field(description="Which flavor would you like?")

    note: str | None = Field(
        default=None,
        description="Any additional notes?"
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
        MyConfirmation,
        Resolve(ask_confirmation),
    ],
) -> str:

    print("\n** Tool `order_item` was executed.\n")
    print(f"Order data:\n")
    print(f"\tconfirmation: {confirmation.confirm}.\n")
    print(f"\tquantity: {confirmation.quantity}.\n")
    print(f"\tflavor: {confirmation.flavor}.\n")
    print(f"\tnote: {confirmation.note}.\n")
    
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