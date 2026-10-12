import asyncio
from mcp import Client, types
from mcp.client import ClientRequestContext


async def handle_elicitation(
    context: ClientRequestContext,
    params: types.ElicitRequestParams,
) -> types.ElicitResult | types.ErrorData:

    # Form mode
    if isinstance(params, types.ElicitRequestFormParams):
        print()
        print(f"MCP Server: {params.message}")

        answer = input("Continue? [y/n]: ").strip().lower()

        return types.ElicitResult(
            action="accept",
            content={
                "confirm": answer == "y",
            },
        )

    # 今回はURL modeを使わない
    # Use only Form Mode this time for my understanding purpose
    return types.ElicitResult(
        action="cancel",
    )


async def main():
    async with Client(
        "http://127.0.0.1:8000/mcp",
        elicitation_callback=handle_elicitation,
        mode="auto",
    ) as client:

        result = await client.call_tool(
            "order_item",
            {
                "item": "おだんご",
            },
        )

        print()
        print("Tool result:")
        print(result)


if __name__ == "__main__":
    asyncio.run(main())