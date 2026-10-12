## STDIO

### Server
```bash
INFO:     Started server process [9912]
INFO:     Waiting for application startup.
StreamableHTTP session manager started
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     127.0.0.1:54843 - "POST /mcp HTTP/1.1" 200 OK

>>> MCP REQUEST
request_id: 2
params:
 {
  "name": "order_item",
  "arguments": {
    "item": "おだんご"
  },
  "_meta": {
    "io.modelcontextprotocol/protocolVersion": "2026-07-28",
    "io.modelcontextprotocol/clientInfo": {
      "name": "mcp",
      "version": "0.1.0"
    },
    "io.modelcontextprotocol/clientCapabilities": {
      "elicitation": {
        "form": {},
        "url": {}
      }
    }
  }
}

** Resolver `ask_confirmation` was called.


<<< MCP RESPONSE
result type: <class 'dict'>
result:
 {
  "inputRequests": {
    "__main__:ask_confirmation": {
      "method": "elicitation/create",
      "params": {
        "message": "Do you want to order 'おだんご'?",
        "mode": "form",
        "requestedSchema": {
          "properties": {
            "confirm": {
              "description": "Do you want to continue?",
              "title": "Confirm",
              "type": "boolean"
            },
            "quantity": {
              "description": "How many would you like?",
              "title": "Quantity",
              "type": "integer"
            },
            "flavor": {
              "description": "Which flavor would you like?",
              "enum": [
                "mitarashi",
                "anko",
                "kinako"
              ],
              "title": "Flavor",
              "type": "string"
            },
            "note": {
              "description": "Any additional notes?",
              "title": "Note",
              "type": "string"
            }
          },
          "required": [
            "confirm",
            "quantity",
            "flavor"
          ],
          "type": "object"
        }
      }
    }
  },
  "requestState": "{\"v\":3,\"outcomes\":{},\"asked\":{\"__main__:ask_confirmation\":\"ZtfOIc1gyGozo81OSnTuTQ\"}}",
  "resultType": "input_required",
  "_meta": {
    "io.modelcontextprotocol/serverInfo": {
      "name": "elicitation-demo",
      "version": ""
    }
  }
}

******* resultType: input_required
INFO:     127.0.0.1:54843 - "POST /mcp HTTP/1.1" 200 OK

>>> MCP REQUEST
request_id: 3
params:
 {
  "inputResponses": {
    "__main__:ask_confirmation": {
      "action": "accept",
      "content": {
        "confirm": true,
        "quantity": 6,
        "flavor": "anko",
        "note": "おまけしてくださいな"
      }
    }
  },
  "requestState": "{\"v\":3,\"outcomes\":{},\"asked\":{\"__main__:ask_confirmation\":\"ZtfOIc1gyGozo81OSnTuTQ\"}}",
  "name": "order_item",
  "arguments": {
    "item": "おだんご"
  },
  "_meta": {
    "io.modelcontextprotocol/protocolVersion": "2026-07-28",
    "io.modelcontextprotocol/clientInfo": {
      "name": "mcp",
      "version": "0.1.0"
    },
    "io.modelcontextprotocol/clientCapabilities": {
      "elicitation": {
        "form": {},
        "url": {}
      }
    }
  }
}

** Resolver `ask_confirmation` was called.


** Tool `order_item` was executed.

Order data:

        confirmation: True.

        quantity: 6.

        flavor: anko.

        note: おまけしてくださいな.


<<< MCP RESPONSE
result type: <class 'dict'>
result:
 {
  "content": [
    {
      "text": "Ordered: おだんご",
      "type": "text"
    }
  ],
  "isError": false,
  "resultType": "complete",
  "structuredContent": {
    "result": "Ordered: おだんご"
  },
  "_meta": {
    "io.modelcontextprotocol/serverInfo": {
      "name": "elicitation-demo",
      "version": ""
    }
  }
}

******* resultType: complete
INFO:     127.0.0.1:54857 - "POST /mcp HTTP/1.1" 200 OK
INFO:     127.0.0.1:54857 - "POST /mcp HTTP/1.1" 200 OK
```

### Client
```bash

=========== REQUESTED SCHEMA ===========
{
  "properties": {
    "confirm": {
      "description": "Do you want to continue?",
      "title": "Confirm",
      "type": "boolean"
    },
    "quantity": {
      "description": "How many would you like?",
      "title": "Quantity",
      "type": "integer"
    },
    "flavor": {
      "description": "Which flavor would you like?",
      "enum": [
        "mitarashi",
        "anko",
        "kinako"
      ],
      "title": "Flavor",
      "type": "string"
    },
    "note": {
      "description": "Any additional notes?",
      "title": "Note",
      "type": "string"
    }
  },
  "required": [
    "confirm",
    "quantity",
    "flavor"
  ],
  "type": "object"
}
=========== REQUESTED SCHEMA ===========

MCP Server: Do you want to order 'おだんご'?
Do you want to continue? [y/n]: y
How many would you like?: 6
Which flavor would you like?
  1. mitarashi
  2. anko
  3. kinako
Select [1-3]: 2
Any additional notes? (optional): おまけしてくださいな

Tool result:
meta={'io.modelcontextprotocol/serverInfo': {'name': 'elicitation-demo', 'version': ''}} content=[TextContent(type='text', text='Ordered: おだんご', annotations=None, meta=None)] structured_content={'result': 'Ordered: おだんご'} is_error=False result_type='complete'
```