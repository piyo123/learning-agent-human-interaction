# 03 Multi Round-trip Declarative Resolver

## Takeout

### Server
```bash
INFO:     Started server process [9076]
INFO:     Waiting for application startup.
StreamableHTTP session manager started
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     127.0.0.1:59190 - "POST /mcp HTTP/1.1" 200 OK

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
** Resolver `ask_delivery_method` was called.


<<< MCP RESPONSE
result type: <class 'dict'>
result:
 {
  "inputRequests": {
    "__main__:ask_delivery_method": {
      "method": "elicitation/create",
      "params": {
        "message": "おだんご をご注文ですね。もう少し教えてください。",
        "mode": "form",
        "requestedSchema": {
          "properties": {
            "method": {
              "description": "テイクアウトですか？お届けですか？",
              "enum": [
                "takeout",
                "delivery"
              ],
              "title": "Method",
              "type": "string"
            }
          },
          "required": [
            "method"
          ],
          "type": "object"
        }
      }
    }
  },
  "requestState": "{\"v\":3,\"outcomes\":{},\"asked\":{\"__main__:ask_delivery_method\":\"kwGApWL_tSc-KJlL6qvgJA\"}}",
  "resultType": "input_required",
  "_meta": {
    "io.modelcontextprotocol/serverInfo": {
      "name": "elicitation-demo",
      "version": ""
    }
  }
}

******* resultType: input_required
INFO:     127.0.0.1:59190 - "POST /mcp HTTP/1.1" 200 OK

>>> MCP REQUEST
request_id: 3
params:
 {
  "inputResponses": {
    "__main__:ask_delivery_method": {
      "action": "accept",
      "content": {
        "method": "takeout"
      }
    }
  },
  "requestState": "{\"v\":3,\"outcomes\":{},\"asked\":{\"__main__:ask_delivery_method\":\"kwGApWL_tSc-KJlL6qvgJA\"}}",
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
** Resolver `ask_delivery_method` was called.

** Resolver `ask_takeout_details` was called.

** Resolver `ask_delivery_details` was called.


<<< MCP RESPONSE
result type: <class 'dict'>
result:
 {
  "inputRequests": {
    "__main__:ask_takeout_details": {
      "method": "elicitation/create",
      "params": {
        "message": "テイクアウトですね。もう少し教えてください。",
        "mode": "form",
        "requestedSchema": {
          "properties": {
            "want_a_wet_towel": {
              "description": "お手拭きはご利用ですか？",
              "title": "Want A Wet Towel",
              "type": "boolean"
            }
          },
          "required": [
            "want_a_wet_towel"
          ],
          "type": "object"
        }
      }
    }
  },
  "requestState": "{\"v\":3,\"outcomes\":{\"__main__:ask_delivery_method\":{\"action\":\"accept\",\"data\":{\"method\":\"takeout\"},\"q\":\"kwGApWL_tSc-KJlL6qvgJA\"}},\"asked\":{\"__main__:ask_takeout_details\":\"_sylzIcVoqFId41Q_HVzFw\"}}",
  "resultType": "input_required",
  "_meta": {
    "io.modelcontextprotocol/serverInfo": {
      "name": "elicitation-demo",
      "version": ""
    }
  }
}

******* resultType: input_required
INFO:     127.0.0.1:59193 - "POST /mcp HTTP/1.1" 200 OK

>>> MCP REQUEST
request_id: 4
params:
 {
  "inputResponses": {
    "__main__:ask_takeout_details": {
      "action": "accept",
      "content": {
        "want_a_wet_towel": true
      }
    }
  },
  "requestState": "{\"v\":3,\"outcomes\":{\"__main__:ask_delivery_method\":{\"action\":\"accept\",\"data\":{\"method\":\"takeout\"},\"q\":\"kwGApWL_tSc-KJlL6qvgJA\"}},\"asked\":{\"__main__:ask_takeout_details\":\"_sylzIcVoqFId41Q_HVzFw\"}}",
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
** Resolver `ask_delivery_method` was called.

** Resolver `ask_takeout_details` was called.

** Resolver `ask_delivery_details` was called.


** Tool `order_item` was executed.


<<< MCP RESPONSE
result type: <class 'dict'>
result:
 {
  "content": [
    {
      "text": "ご注文: おだんご\n受け取り方法: takeout\nおしぼりは必要か: True",
      "type": "text"
    }
  ],
  "isError": false,
  "resultType": "complete",
  "structuredContent": {
    "result": "ご注文: おだんご\n受け取り方法: takeout\nおしぼりは必要か: True"
  },
  "_meta": {
    "io.modelcontextprotocol/serverInfo": {
      "name": "elicitation-demo",
      "version": ""
    }
  }
}

******* resultType: complete
INFO:     127.0.0.1:59202 - "POST /mcp HTTP/1.1" 200 OK
INFO:     127.0.0.1:59202 - "POST /mcp HTTP/1.1" 200 OK
```

### Client
```bash
=========== ↓REQUESTED SCHEMA↓ ===========
{
  "properties": {
    "method": {
      "description": "\u30c6\u30a4\u30af\u30a2\u30a6\u30c8\u3067\u3059\u304b\uff1f\u304a\u5c4a\u3051\u3067\u3059\u304b\uff1f",
      "enum": [
        "takeout",
        "delivery"
      ],
      "title": "Method",
      "type": "string"
    }
  },
  "required": [
    "method"
  ],
  "type": "object"
}
=========== ↑REQUESTED SCHEMA↑ ===========

MCP Server: おだんご をご注文ですね。もう少し教えてください。
テイクアウトですか？お届けですか？
  1. takeout
  2. delivery
Select [1-2]: 1

=========== ↓REQUESTED SCHEMA↓ ===========
{
  "properties": {
    "want_a_wet_towel": {
      "description": "\u304a\u624b\u62ed\u304d\u306f\u3054\u5229\u7528\u3067\u3059\u304b\uff1f",
      "title": "Want A Wet Towel",
      "type": "boolean"
    }
  },
  "required": [
    "want_a_wet_towel"
  ],
  "type": "object"
}
=========== ↑REQUESTED SCHEMA↑ ===========

MCP Server: テイクアウトですね。もう少し教えてください。
お手拭きはご利用ですか？ [y/n]: y

Tool result:
meta={'io.modelcontextprotocol/serverInfo': {'name': 'elicitation-demo', 'version': ''}} content=[TextContent(type='text', text='ご注文: おだんご\n受け取り方法: takeout\nおしぼりは必要か: True', annotations=None, meta=None)] structured_content={'result': 'ご注文: おだんご\n受け取り方法: takeout\nおしぼりは必要か: True'} is_error=False result_type='complete'

注文内容:
ご注文: おだんご
受け取り方法: takeout
おしぼりは必要か: True
```

## Delivery

### Server
```bash
INFO:     Started server process [5508]
INFO:     Waiting for application startup.
StreamableHTTP session manager started
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     127.0.0.1:55560 - "POST /mcp HTTP/1.1" 200 OK

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
** Resolver `ask_delivery_method` was called.


<<< MCP RESPONSE
result type: <class 'dict'>
result:
 {
  "inputRequests": {
    "__main__:ask_delivery_method": {
      "method": "elicitation/create",
      "params": {
        "message": "おだんご をご注文ですね。もう少し教えてください。",
        "mode": "form",
        "requestedSchema": {
          "properties": {
            "method": {
              "description": "テイクアウトですか？お届けですか？",
              "enum": [
                "takeout",
                "delivery"
              ],
              "title": "Method",
              "type": "string"
            }
          },
          "required": [
            "method"
          ],
          "type": "object"
        }
      }
    }
  },
  "requestState": "{\"v\":3,\"outcomes\":{},\"asked\":{\"__main__:ask_delivery_method\":\"kwGApWL_tSc-KJlL6qvgJA\"}}",
  "resultType": "input_required",
  "_meta": {
    "io.modelcontextprotocol/serverInfo": {
      "name": "elicitation-demo",
      "version": ""
    }
  }
}

******* resultType: input_required
INFO:     127.0.0.1:55560 - "POST /mcp HTTP/1.1" 200 OK

>>> MCP REQUEST
request_id: 3
params:
 {
  "inputResponses": {
    "__main__:ask_delivery_method": {
      "action": "accept",
      "content": {
        "method": "delivery"
      }
    }
  },
  "requestState": "{\"v\":3,\"outcomes\":{},\"asked\":{\"__main__:ask_delivery_method\":\"kwGApWL_tSc-KJlL6qvgJA\"}}",
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
** Resolver `ask_delivery_method` was called.

** Resolver `ask_takeout_details` was called.

** Resolver `ask_delivery_details` was called.


<<< MCP RESPONSE
result type: <class 'dict'>
result:
 {
  "inputRequests": {
    "__main__:ask_delivery_details": {
      "method": "elicitation/create",
      "params": {
        "message": "お届けですね。もう少し教えてください。",
        "mode": "form",
        "requestedSchema": {
          "properties": {
            "delivery_date": {
              "description": "いつお届けしましょうか？",
              "title": "Delivery Date",
              "type": "string"
            }
          },
          "required": [
            "delivery_date"
          ],
          "type": "object"
        }
      }
    }
  },
  "requestState": "{\"v\":3,\"outcomes\":{\"__main__:ask_delivery_method\":{\"action\":\"accept\",\"data\":{\"method\":\"delivery\"},\"q\":\"kwGApWL_tSc-KJlL6qvgJA\"}},\"asked\":{\"__main__:ask_delivery_details\":\"CJJiSDpWD5HaQZkUg3e35w\"}}",
  "resultType": "input_required",
  "_meta": {
    "io.modelcontextprotocol/serverInfo": {
      "name": "elicitation-demo",
      "version": ""
    }
  }
}

******* resultType: input_required
INFO:     127.0.0.1:55560 - "POST /mcp HTTP/1.1" 200 OK

>>> MCP REQUEST
request_id: 4
params:
 {
  "inputResponses": {
    "__main__:ask_delivery_details": {
      "action": "accept",
      "content": {
        "delivery_date": "2026/10/11でお願いします。"
      }
    }
  },
  "requestState": "{\"v\":3,\"outcomes\":{\"__main__:ask_delivery_method\":{\"action\":\"accept\",\"data\":{\"method\":\"delivery\"},\"q\":\"kwGApWL_tSc-KJlL6qvgJA\"}},\"asked\":{\"__main__:ask_delivery_details\":\"CJJiSDpWD5HaQZkUg3e35w\"}}",
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
** Resolver `ask_delivery_method` was called.

** Resolver `ask_takeout_details` was called.

** Resolver `ask_delivery_details` was called.


** Tool `order_item` was executed.


<<< MCP RESPONSE
result type: <class 'dict'>
result:
 {
  "content": [
    {
      "text": "ご注文: おだんご\nお受け取り方法: delivery\nお届け日: 2026/10/11でお願いします。",
      "type": "text"
    }
  ],
  "isError": false,
  "resultType": "complete",
  "structuredContent": {
    "result": "ご注文: おだんご\nお受け取り方法: delivery\nお届け日: 2026/10/11でお願いします。"
  },
  "_meta": {
    "io.modelcontextprotocol/serverInfo": {
      "name": "elicitation-demo",
      "version": ""
    }
  }
}

******* resultType: complete
INFO:     127.0.0.1:55575 - "POST /mcp HTTP/1.1" 200 OK
INFO:     127.0.0.1:55575 - "POST /mcp HTTP/1.1" 200 OK
```

### Client
```bash
=========== ↓REQUESTED SCHEMA↓ ===========
{
  "properties": {
    "method": {
      "description": "\u30c6\u30a4\u30af\u30a2\u30a6\u30c8\u3067\u3059\u304b\uff1f\u304a\u5c4a\u3051\u3067\u3059\u304b\uff1f",
      "enum": [
        "takeout",
        "delivery"
      ],
      "title": "Method",
      "type": "string"
    }
  },
  "required": [
    "method"
  ],
  "type": "object"
}
=========== ↑REQUESTED SCHEMA↑ ===========

MCP Server: おだんご をご注文ですね。もう少し教えてください。
テイクアウトですか？お届けですか？
  1. takeout
  2. delivery
Select [1-2]: 2

=========== ↓REQUESTED SCHEMA↓ ===========
{
  "properties": {
    "delivery_date": {
      "description": "\u3044\u3064\u304a\u5c4a\u3051\u3057\u307e\u3057\u3087\u3046\u304b\uff1f",
      "title": "Delivery Date",
      "type": "string"
    }
  },
  "required": [
    "delivery_date"
  ],
  "type": "object"
}
=========== ↑REQUESTED SCHEMA↑ ===========

MCP Server: お届けですね。もう少し教えてください。
いつお届けしましょうか？: 2026/10/11でお願いします。

Tool result:
meta={'io.modelcontextprotocol/serverInfo': {'name': 'elicitation-demo', 'version': ''}} content=[TextContent(type='text', text='ご注文: おだんご\nお受け取り方法: delivery\nお届け日: 2026/10/11でお願いします。', annotations=None, meta=None)] structured_content={'result': 'ご注文: おだんご\nお受け取り方法: delivery\nお届け日: 2026/10/11でお願いします。'} is_error=False result_type='complete'

注文内容:
ご注文: おだんご
お受け取り方法: delivery
お届け日: 2026/10/11でお願いします。
```