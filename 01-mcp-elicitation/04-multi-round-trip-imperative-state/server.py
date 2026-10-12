import json
from typing import Literal
from pydantic import BaseModel, Field
from mcp.server.mcpserver import MCPServer, Context
from mcp.types import (
    ElicitRequest,
    ElicitRequestFormParams,
    ElicitResult,
    InputRequiredResult
)

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


# Helper function to create Eliciation Request
def create_elicitation(
        message: str,
        model: type[BaseModel],
) -> ElicitRequest:

    return ElicitRequest(
        params=ElicitRequestFormParams(
            message=message,
            requested_schema=model.model_json_schema(),
        )
    )


# MCP Tool
@mcp.tool()
async def order_item(
    item: str,
    ctx: Context,
) -> str | InputRequiredResult:

    state = (
        json.loads(ctx.request_state)
        if ctx.request_state
        else {"round": 0}
    )

    responses = ctx.input_responses or {}

    print(f"** round = {state['round']}")
    print(f"** responses = {responses}")

    # --------------------------------
    # Round 0
    # 受取方法を尋ねる
    # Ask Delivery Method
    # --------------------------------

    if state["round"] == 0:

        return InputRequiredResult(
            input_requests={
                "delivery_method": create_elicitation(
                    f"{item} をご注文ですね。もう少し教えてください。",
                    MyDeliveryMethod,
                )
            },
            request_state=json.dumps({
                "round": 1,
            }),
        )

    # --------------------------------
    # Round 1
    # 受取方法に応じて次の質問を変える
    # Decide next question by delivery medhod
    # --------------------------------

    if state["round"] == 1 and "delivery_method" in responses:

        answer = responses["delivery_method"]

        if not isinstance(answer, ElicitResult):
            return "注文をキャンセルしました。"

        if answer.action != "accept" or not answer.content:
            return "注文をキャンセルしました。"

        method = answer.content["method"]

        print(f"** selected method = {method}")

        if method == "takeout":

            return InputRequiredResult(
                input_requests={
                    "takeout_details": create_elicitation(
                        "テイクアウトですね。もう少し教えてください。",
                        MyTakeoutDetails,
                    )
                },
                request_state=json.dumps({
                    "round": 2,
                    "method": "takeout",
                }),
            )

        if method == "delivery":

            return InputRequiredResult(
                input_requests={
                    "delivery_details": create_elicitation(
                        "お届けですね。もう少し教えてください。",
                        MyDeliveryDetails,
                    )
                },
                request_state=json.dumps({
                    "round": 2,
                    "method": "delivery",
                }),
            )

    # --------------------------------
    # Round 2
    # 最終結果を返す
    # Return final output
    # --------------------------------

    if state["round"] == 2:

        method = state["method"]

        if method == "takeout" and "takeout_details" in responses:

            answer = responses["takeout_details"]

            if isinstance(answer, ElicitResult) and answer.action == "accept" and answer.content:

                want_a_wet_towel = answer.content[
                    "want_a_wet_towel"
                ]

                return (
                    f"注文商品: {item}\n"
                    f"受取方法: テイクアウト\n"
                    f"お手拭き: {want_a_wet_towel}"
                )

        if method == "delivery" and "delivery_details" in responses:
        
            answer = responses["delivery_details"]

            if isinstance(answer, ElicitResult) and answer.action == "accept" and answer.content:

                delivery_date = answer.content[
                    "delivery_date"
                ]

                return (
                    f"注文商品: {item}\n"
                    f"受取方法: お届け\n"
                    f"お届け日: {delivery_date}"
                )

    return "注文を完了できませんでした。"


# Streamable HTTPでMCP Serverを起動
# Start MCP Server with Streamable HTTP protocol
if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="127.0.0.1",
        port=8000,
    )