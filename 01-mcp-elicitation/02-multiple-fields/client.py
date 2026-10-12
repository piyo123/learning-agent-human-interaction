import asyncio
import json
from mcp import Client, types
from mcp.client import ClientRequestContext

# MCP サーバーから受け取った Elicitation JSON の属性に基づいて、ユーザーから回答を得る
# collect required information from a user based on requested eclicitation JSON schema
def get_field_value(
    field_name: str,
    field_schema: dict,
    is_required: bool,
):
    description = field_schema.get(
        "description",
        field_schema.get("title", field_name),
    )

    field_type = field_schema.get("type")

    # enum
    if "enum" in field_schema:
        return get_enum_value(
            description,
            field_schema["enum"],
            is_required,
        )

    # boolean
    if field_type == "boolean":
        return get_boolean_value(description, is_required)

    # integer
    if field_type == "integer":
        return get_integer_value(description, is_required)

    # number
    if field_type == "number":
        return get_number_value(description, is_required)

    # string
    if field_type == "string":
        return get_string_value(description, is_required)

    raise ValueError(
        f"Unsupported field type: {field_name} ({field_type})"
    )

# a helper function for get_field_value
def get_enum_value(
    description: str,
    choices: list,
    is_required: bool,
):
    print(description)

    for index, choice in enumerate(choices, start=1):
        print(f"  {index}. {choice}")

    while True:
        answer = input(
            f"Select [1-{len(choices)}]"
            f"{'' if is_required else ' (optional)'}: "
        ).strip()

        if not answer and not is_required:
            return None

        try:
            index = int(answer) - 1

            if 0 <= index < len(choices):
                return choices[index]

        except ValueError:
            pass

        print("Invalid selection.")

# a helper function for get_field_value
def get_boolean_value(
    description: str,
    is_required: bool,
):
    while True:
        answer = input(
            f"{description} [y/n]"
            f"{'' if is_required else ' (optional)'}: "
        ).strip().lower()

        if not answer and not is_required:
            return None

        if answer in ("y", "yes"):
            return True

        if answer in ("n", "no"):
            return False

        print("Please enter y or n.")

# a helper function for get_field_value
def get_integer_value(
    description: str,
    is_required: bool,
):
    while True:
        answer = input(
            f"{description}"
            f"{'' if is_required else ' (optional)'}: "
        ).strip()

        if not answer and not is_required:
            return None

        try:
            return int(answer)
        except ValueError:
            print("Please enter an integer.")

# a helper function for get_field_value
def get_number_value(
    description: str,
    is_required: bool,
):
    while True:
        answer = input(
            f"{description}"
            f"{'' if is_required else ' (optional)'}: "
        ).strip()

        if not answer and not is_required:
            return None

        try:
            return float(answer)
        except ValueError:
            print("Please enter a number.")

# a helper function for get_field_value
def get_string_value(
    description: str,
    is_required: bool,
):
    while True:
        answer = input(
            f"{description}"
            f"{'' if is_required else ' (optional)'}: "
        ).strip()

        if answer:
            return answer

        if not is_required:
            return None

        print("This field is required.")


async def handle_elicitation(
    context: ClientRequestContext,
    params: types.ElicitRequestParams,
) -> types.ElicitResult | types.ErrorData:

    if not isinstance(params, types.ElicitRequestFormParams):
        return types.ElicitResult(action="cancel")

    print()
    print("=========== REQUESTED SCHEMA ===========")
    print(json.dumps(params.requested_schema, indent=2, ensure_ascii=True))
    print("=========== REQUESTED SCHEMA ===========")
    print()
    print(f"MCP Server: {params.message}")

    schema = params.requested_schema
    properties = schema.get("properties", {})
    required_fields = set(schema.get("required", []))

    content = {}

    for field_name, field_schema in properties.items():
        try:
            value = get_field_value(
                field_name,
                field_schema,
                field_name in required_fields
            )
        except ValueError as e:
            print(e)
            return types.ElicitResult(action="cancel")

        if value is not None:
            content[field_name] = value

    return types.ElicitResult(
        action="accept",
        content=content,
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