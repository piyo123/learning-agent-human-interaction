## Behavior overview

```text
① tools/call #1
   arguments:
     item = "おだんご"
        ↓
② Resolve(ask_confirmation)
        ↓
③ Elicit(...)
        ↓
④ MCP Server
   result_type = "input_required"
        ↓
⑤ Client
   elicitation_callback
        ↓
⑥ Human
   y
        ↓
⑦ tools/call #2
   arguments:
     item = "おだんご"
   inputResponses:
     confirm = True
   requestState:
     ...
        ↓
⑧ Resolve(ask_confirmation)
        ↓
⑨ confirmation 解決
        ↓
⑩ order_item() 実行
        ↓
⑪ result_type = "complete"
```

## Log (YES)

### Server
```bash
INFO:     Started server process [13304]
INFO:     Waiting for application startup.
StreamableHTTP session manager started
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     127.0.0.1:52201 - "POST /mcp HTTP/1.1" 200 OK

>>> MCP REQUEST
request_id: 2
params: {'name': 'order_item', 'arguments': {'item': 'おだんご'}, '_meta': {'io.modelcontextprotocol/protocolVersion': '2026-07-28', 'io.modelcontextprotocol/clientInfo': {'name': 'mcp', 'version': '0.1.0'}, 'io.modelcontextprotocol/clientCapabilities': {'elicitation': {'form': {}, 'url': {}}}}}

** Resolver `ask_confirmation` was called.


<<< MCP RESPONSE
result type: <class 'dict'>
result: {'inputRequests': {'__main__:ask_confirmation': {'method': 'elicitation/create', 'params': {'message': "Do you want to order 'おだんご'?", 'mode': 'form', 'requestedSchema': {'properties': {'confirm': {'description': 'Do you want to continue?', 'title': 'Confirm', 'type': 'boolean'}}, 'required': ['confirm'], 'type': 'object'}}}}, 'requestState': '{"v":3,"outcomes":{},"asked":{"__main__:ask_confirmation":"KuTvCaqbAtgDFE5hKVcjJg"}}', 'resultType': 'input_required', '_meta': {'io.modelcontextprotocol/serverInfo': {'name': 'elicitation-demo', 'version': ''}}}
resultType: input_required
INFO:     127.0.0.1:52201 - "POST /mcp HTTP/1.1" 200 OK

>>> MCP REQUEST
request_id: 3
params: {'inputResponses': {'__main__:ask_confirmation': {'action': 'accept', 'content': {'confirm': True}}}, 'requestState': '{"v":3,"outcomes":{},"asked":{"__main__:ask_confirmation":"KuTvCaqbAtgDFE5hKVcjJg"}}', 'name': 'order_item', 'arguments': {'item': 'おだんご'}, '_meta': {'io.modelcontextprotocol/protocolVersion': '2026-07-28', 'io.modelcontextprotocol/clientInfo': {'name': 'mcp', 'version': '0.1.0'}, 'io.modelcontextprotocol/clientCapabilities': {'elicitation': {'form': {}, 'url': {}}}}}

** Resolver `ask_confirmation` was called.


** Tool `order_item` was executed.


        ** Received confirmation: True.


<<< MCP RESPONSE
result type: <class 'dict'>
result: {'content': [{'text': 'Ordered: おだんご', 'type': 'text'}], 'isError': False, 'resultType': 'complete', 'structuredContent': {'result': 'Ordered: おだんご'}, '_meta': {'io.modelcontextprotocol/serverInfo': {'name': 'elicitation-demo', 'version': ''}}}
resultType: complete
INFO:     127.0.0.1:52250 - "POST /mcp HTTP/1.1" 200 OK
INFO:     127.0.0.1:52250 - "POST /mcp HTTP/1.1" 200 OK
```

### Client
```bash
MCP Server: Do you want to order 'おだんご'?
Continue? [y/n]: y

Tool result:
meta={'io.modelcontextprotocol/serverInfo': {'name': 'elicitation-demo', 'version': ''}} content=[TextContent(type='text', text='Ordered: おだんご', annotations=None, meta=None)] structured_content={'result': 'Ordered: おだんご'} is_error=False result_type='complete'
```

## Log (NO)

### Server
```bash
INFO:     Started server process [11860]
INFO:     Waiting for application startup.
StreamableHTTP session manager started
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     127.0.0.1:59035 - "POST /mcp HTTP/1.1" 200 OK

>>> MCP REQUEST
request_id: 2
params: {'name': 'order_item', 'arguments': {'item': 'おだんご'}, '_meta': {'io.modelcontextprotocol/protocolVersion': '2026-07-28', 'io.modelcontextprotocol/clientInfo': {'name': 'mcp', 'version': '0.1.0'}, 'io.modelcontextprotocol/clientCapabilities': {'elicitation': {'form': {}, 'url': {}}}}}

** Resolver `ask_confirmation` was called.


<<< MCP RESPONSE
result type: <class 'dict'>
result: {'inputRequests': {'__main__:ask_confirmation': {'method': 'elicitation/create', 'params': {'message': "Do you want to order 'おだんご'?", 'mode': 'form', 'requestedSchema': {'properties': {'confirm': {'description': 'Do you want to continue?', 'title': 'Confirm', 'type': 'boolean'}}, 'required': ['confirm'], 'type': 'object'}}}}, 'requestState': '{"v":3,"outcomes":{},"asked":{"__main__:ask_confirmation":"KuTvCaqbAtgDFE5hKVcjJg"}}', 'resultType': 'input_required', '_meta': {'io.modelcontextprotocol/serverInfo': {'name': 'elicitation-demo', 'version': ''}}}
resultType: input_required
INFO:     127.0.0.1:59035 - "POST /mcp HTTP/1.1" 200 OK

>>> MCP REQUEST
request_id: 3
params: {'inputResponses': {'__main__:ask_confirmation': {'action': 'accept', 'content': {'confirm': False}}}, 'requestState': '{"v":3,"outcomes":{},"asked":{"__main__:ask_confirmation":"KuTvCaqbAtgDFE5hKVcjJg"}}', 'name': 'order_item', 'arguments': {'item': 'おだんご'}, '_meta': {'io.modelcontextprotocol/protocolVersion': '2026-07-28', 'io.modelcontextprotocol/clientInfo': {'name': 'mcp', 'version': '0.1.0'}, 'io.modelcontextprotocol/clientCapabilities': {'elicitation': {'form': {}, 'url': {}}}}}

** Resolver `ask_confirmation` was called.


** Tool `order_item` was executed.


        ** Received confirmation: False.


<<< MCP RESPONSE
result type: <class 'dict'>
result: {'content': [{'text': 'Order cancelled.', 'type': 'text'}], 'isError': False, 'resultType': 'complete', 'structuredContent': {'result': 'Order cancelled.'}, '_meta': {'io.modelcontextprotocol/serverInfo': {'name': 'elicitation-demo', 'version': ''}}}
resultType: complete
INFO:     127.0.0.1:59035 - "POST /mcp HTTP/1.1" 200 OK
INFO:     127.0.0.1:59035 - "POST /mcp HTTP/1.1" 200 OK
```

### Client
```bash
MCP Server: Do you want to order 'おだんご'?
Continue? [y/n]: n

Tool result:
meta={'io.modelcontextprotocol/serverInfo': {'name': 'elicitation-demo', 'version': ''}} content=[TextContent(type='text', text='Order cancelled.', annotations=None, meta=None)] structured_content={'result': 'Order cancelled.'} is_error=False result_type='complete'
```