# 04 Multi Round-trip Imperative State Management

## Takeout

### Server
```bash
INFO:     Started server process [9332]
INFO:     Waiting for application startup.
StreamableHTTP session manager started
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     127.0.0.1:51740 - "POST /mcp HTTP/1.1" 200 OK

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
** round = 0
** responses = {}

<<< MCP RESPONSE
result type: <class 'dict'>
result:
 {
  "inputRequests": {
    "delivery_method": {
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
  "requestState": "{\"round\": 1}",
  "resultType": "input_required",
  "_meta": {
    "io.modelcontextprotocol/serverInfo": {
      "name": "elicitation-demo",
      "version": ""
    }
  }
}

******* resultType: input_required
INFO:     127.0.0.1:51740 - "POST /mcp HTTP/1.1" 200 OK

>>> MCP REQUEST
request_id: 3
params:
 {
  "inputResponses": {
    "delivery_method": {
      "action": "accept",
      "content": {
        "method": "takeout"
      }
    }
  },
  "requestState": "{\"round\": 1}",
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
** round = 1
** responses = {'delivery_method': ElicitResult(meta=None, action='accept', content={'method': 'takeout'})}
** selected method = takeout

<<< MCP RESPONSE
result type: <class 'dict'>
result:
 {
  "inputRequests": {
    "takeout_details": {
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
  "requestState": "{\"round\": 2, \"method\": \"takeout\"}",
  "resultType": "input_required",
  "_meta": {
    "io.modelcontextprotocol/serverInfo": {
      "name": "elicitation-demo",
      "version": ""
    }
  }
}

******* resultType: input_required
INFO:     127.0.0.1:51740 - "POST /mcp HTTP/1.1" 200 OK

>>> MCP REQUEST
request_id: 4
params:
 {
  "inputResponses": {
    "takeout_details": {
      "action": "accept",
      "content": {
        "want_a_wet_towel": true
      }
    }
  },
  "requestState": "{\"round\": 2, \"method\": \"takeout\"}",
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
** round = 2
** responses = {'takeout_details': ElicitResult(meta=None, action='accept', content={'want_a_wet_towel': True})}

<<< MCP RESPONSE
result type: <class 'dict'>
result:
 {
  "content": [
    {
      "text": "注文商品: おだんご\n受取方法: テイクアウト\nお手拭き: True",
      "type": "text"
    }
  ],
  "isError": false,
  "resultType": "complete",
  "structuredContent": {
    "result": "注文商品: おだんご\n受取方法: テイクアウト\nお手拭き: True"
  },
  "_meta": {
    "io.modelcontextprotocol/serverInfo": {
      "name": "elicitation-demo",
      "version": ""
    }
  }
}

******* resultType: complete
INFO:     127.0.0.1:51741 - "POST /mcp HTTP/1.1" 200 OK
INFO:     127.0.0.1:51741 - "POST /mcp HTTP/1.1" 200 OK
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
meta={'io.modelcontextprotocol/serverInfo': {'name': 'elicitation-demo', 'version': ''}} content=[TextContent(type='text', text='注文商品: おだんご\n受取方法: テイクアウト\nお手拭き: True', annotations=None, meta=None)] structured_content={'result': '注文商品: おだんご\n受取方法: テイクアウト\nお手拭き: True'} is_error=False result_type='complete'

注文内容:
注文商品: おだんご
受取方法: テイクアウト
お手拭き: True
```

## Delivery

### Server
```bash
INFO:     Started server process [5144]
INFO:     Waiting for application startup.
StreamableHTTP session manager started
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     127.0.0.1:61192 - "POST /mcp HTTP/1.1" 200 OK

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
** round = 0
** responses = {}

<<< MCP RESPONSE
result type: <class 'dict'>
result:
 {
  "inputRequests": {
    "delivery_method": {
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
  "requestState": "{\"round\": 1}",
  "resultType": "input_required",
  "_meta": {
    "io.modelcontextprotocol/serverInfo": {
      "name": "elicitation-demo",
      "version": ""
    }
  }
}

******* resultType: input_required
INFO:     127.0.0.1:61192 - "POST /mcp HTTP/1.1" 200 OK

>>> MCP REQUEST
request_id: 3
params:
 {
  "inputResponses": {
    "delivery_method": {
      "action": "accept",
      "content": {
        "method": "delivery"
      }
    }
  },
  "requestState": "{\"round\": 1}",
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
** round = 1
** responses = {'delivery_method': ElicitResult(meta=None, action='accept', content={'method': 'delivery'})}
** selected method = delivery

<<< MCP RESPONSE
result type: <class 'dict'>
result:
 {
  "inputRequests": {
    "delivery_details": {
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
  "requestState": "{\"round\": 2, \"method\": \"delivery\"}",
  "resultType": "input_required",
  "_meta": {
    "io.modelcontextprotocol/serverInfo": {
      "name": "elicitation-demo",
      "version": ""
    }
  }
}

******* resultType: input_required
INFO:     127.0.0.1:61192 - "POST /mcp HTTP/1.1" 200 OK

>>> MCP REQUEST
request_id: 4
params:
 {
  "inputResponses": {
    "delivery_details": {
      "action": "accept",
      "content": {
        "delivery_date": "明日ぐらいで。"
      }
    }
  },
  "requestState": "{\"round\": 2, \"method\": \"delivery\"}",
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
** round = 2
** responses = {'delivery_details': ElicitResult(meta=None, action='accept', content={'delivery_date': '明日ぐらいで。'})}

<<< MCP RESPONSE
result type: <class 'dict'>
result:
 {
  "content": [
    {
      "text": "注文商品: おだんご\n受取方法: お届け\nお届け日: 明日ぐらいで。",
      "type": "text"
    }
  ],
  "isError": false,
  "resultType": "complete",
  "structuredContent": {
    "result": "注文商品: おだんご\n受取方法: お届け\nお届け日: 明日ぐらいで。"
  },
  "_meta": {
    "io.modelcontextprotocol/serverInfo": {
      "name": "elicitation-demo",
      "version": ""
    }
  }
}

******* resultType: complete
INFO:     127.0.0.1:61198 - "POST /mcp HTTP/1.1" 200 OK
INFO:     127.0.0.1:61198 - "POST /mcp HTTP/1.1" 200 OK
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
いつお届けしましょうか？: 明日ぐらいで。

Tool result:
meta={'io.modelcontextprotocol/serverInfo': {'name': 'elicitation-demo', 'version': ''}} content=[TextContent(type='text', text='注文商品: おだんご\n受取方法: お届け\nお届け日: 明日ぐらいで。', annotations=None, meta=None)] structured_content={'result': '注文商品: おだんご\n受取方法: お届け\nお届け日: 明日ぐらいで。'} is_error=False result_type='complete'

注文内容:
注文商品: おだんご
受取方法: お届け
お届け日: 明日ぐらいで。
```
