# Learning Agent-Human Interaction

本リポジトリは AI エージェントが `Human-in-the-Loop` 時に人間とコミュニケーションする概念や手法を学習した履歴を残したものです。リポジトリの構成は次の通りです。

## 01. [MCP Elicitation](01-mcp-elicitation/)

Model Context Protocol (MCP) の [Elicitation](https://modelcontextprotocol.io/specification/2026-07-28/client/elicitation) の検証結果です。  
Elicitation は MCP サーバーが処理に必要な情報を、MCP クライアントを介してユーザーに問い合わせるための仕組みです。  
今回は Form Mode のみ検証しています。 MCP の Version 2026-07-28 を使用し、MCP Python SDK は version 2.3.0 を使用しています。  

MCP の プロトコルバージョンについては[こちら](https://github.com/modelcontextprotocol/python-sdk/blob/main/docs/protocol-versions.md)に解説があります。  
また MCP Python SDK の v1 系と v2 系の差異については[こちら](https://github.com/modelcontextprotocol/python-sdk/blob/main/docs/migration.md)で解説されています。

*Initial implementation: October 12, 2026*

## 02. [MCP Apps](02-mcp-apps/)

[MCP Apps](https://apps.extensions.modelcontextprotocol.io/api/) は、MCP Server が提供する対話的な画面を、対応する Host の中に表示するための [MCP 拡張](https://modelcontextprotocol.io/extensions/overview)です。Tool が返すデータをテキストで読むだけでなく、グラフや表で確認したり、フォームやボタンを操作したりできるようになります。例えば、検索結果を一覧から選択する画面や、条件を入力して結果を更新する画面を、会話の流れの中で利用できます。  

本章では MCP Apps の基本的な動作を確認してみました。

*Initial implementation: October 17, 2026*

## 03. 以降

02 以降は次の内容について順次追加していく予定です。内容は変更の可能性があります。

- A2UI
- AG-UI
- 等


https://github.com/user-attachments/assets/fffde68e-72a4-4c9a-af3d-f430d8a2244c

