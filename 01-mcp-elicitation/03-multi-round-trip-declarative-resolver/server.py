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
class MyDeliveryMethod(BaseModel):
    method: Literal["takeout", "delivery"] = Field(description="テイクアウトですか？お届けですか？") # How would you like to receive your order?

class MyTakeoutDetails(BaseModel):
    want_a_wet_towel: bool = Field(description="お手拭きはご利用ですか？") # Would you like a wet towel?

class MyDeliveryDetails(BaseModel):
    delivery_date: str = Field(description="いつお届けしましょうか？") # When would you like your order delivered?


# Resolver - Delivery Method
async def ask_delivery_method(item: str) -> Elicit[MyDeliveryMethod]:

    print("** Resolver `ask_delivery_method` was called.\n")
    
    return Elicit(
        f"{item} をご注文ですね。もう少し教えてください。",
        MyDeliveryMethod,
    )


# Resolver - Takeout Details
async def ask_takeout_details(
        delivery_method: Annotated[
            MyTakeoutDetails,
            Resolve(ask_delivery_method),
        ]
) -> Elicit[MyTakeoutDetails] | MyTakeoutDetails:

    print("** Resolver `ask_takeout_details` was called.\n")

    if delivery_method.method == "takeout":
        return Elicit(
            "テイクアウトですね。もう少し教えてください。",
            MyTakeoutDetails,
        )

    return MyTakeoutDetails(want_a_wet_towel=False)

# Resolver - Delivery Details
async def ask_delivery_details(
        delivery_method: Annotated[
            MyDeliveryDetails,
            Resolve(ask_delivery_method),
        ]
) -> Elicit[MyDeliveryDetails] | MyDeliveryDetails:

    print("** Resolver `ask_delivery_details` was called.\n")

    if delivery_method.method == "delivery":
        return Elicit(
            "お届けですね。もう少し教えてください。",
            MyDeliveryDetails,
        )

    return MyDeliveryDetails(delivery_date="")

# Resolver - OrderDetails
# async def ask_order_details(
#         delivery_method: Annotated[
#             MyDeliveryMethod,
#             Resolve(ask_delivery_method),
#         ],
# ) -> Elicit[MyTakeoutDetails] | Elicit[MyDeliveryDetails] | Elicit[MyDeliveryMethod]:

#     print("** Resolver `ask_order_details` was called.\n")

#     if delivery_method.method == "takeout":
#         return Elicit(
#             "テイクアウトですね。もう少し教えてください。",
#             MyTakeoutDetails,
#         )
#     elif delivery_method.method == "delivery":
#         return Elicit(
#             "お届けですね。もう少し教えてください。",
#             MyDeliveryDetails,
#         )
#     else:
#         return Elicit(
#             "申し訳ございません。よく分かりませんでした。",
#             MyDeliveryMethod,
#         )
    

# MCP Tool
@mcp.tool()
async def order_item(
    item: str,
    delivery_method: Annotated[
        MyDeliveryMethod,
        Resolve(ask_delivery_method),
    ],
    takeout_details: Annotated[
        MyTakeoutDetails,
        Resolve(ask_takeout_details),
    ],
    delivery_details: Annotated[
        MyDeliveryDetails,
        Resolve(ask_delivery_details),
    ],
) -> str:

    print("\n** Tool `order_item` was executed.\n")
    
    if delivery_method.method == "takeout":
        return (
            f"ご注文: {item}\n"
            f"受け取り方法: {delivery_method.method}\n"
            f"おしぼりは必要か: {takeout_details.want_a_wet_towel}"
        )

    return (
        f"ご注文: {item}\n"
        f"お受け取り方法: {delivery_method.method}\n"
        f"お届け日: {delivery_details.delivery_date}"
    )

# Streamable HTTPでMCP Serverを起動
# Start MCP Server with Streamable HTTP protocol
if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="127.0.0.1",
        port=8000,
    )