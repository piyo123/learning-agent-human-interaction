# Learning Agent-Human Interaction

本リポジトリは AI エージェントが `Human-in-the-Loop` 時に人間とコミュニケーションする概念や手法を学習した履歴を残したものです。リポジトリの構成は次の通りです。

## 01. [MCP Elicitation](01-mcp-elicitation/)

Model Context Protocol (MCP) の [Elicitation](https://modelcontextprotocol.io/specification/2026-07-28/client/elicitation) の検証結果です。  
Elicitation は MCP サーバーが処理に必要な情報を、MCP クライアントを介してユーザーに問い合わせるための仕組みです。  
今回は Form Mode のみ検証しています。 MCP の Version 2026-07-28 を使用し、MCP Python SDK は version 2.3.0 を使用しています。  

MCP の プロトコルバージョンについては[こちら](https://github.com/modelcontextprotocol/python-sdk/blob/main/docs/protocol-versions.md)に解説があります。  
また MCP Python SDK の v1 系と v2 系の差異については[こちら](https://github.com/modelcontextprotocol/python-sdk/blob/main/docs/migration.md)で解説されています。

**Initial implementation: October 12, 2026*

## 02 以降

02 以降は次の内容について順次追加していく予定です。内容は変更の可能性があります。

- MCP Apps
- A2UI
- AG-UI
- 等
