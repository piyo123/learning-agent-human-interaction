import {
    AppBridge,
    PostMessageTransport
} from "@modelcontextprotocol/ext-apps/app-bridge";

async function main() {
    console.log("[Host] Main started");

    // FastAPI 経由で MCP からデータを取得
    // Receive data from MCP Server via FastAPI
    const response = await fetch("/payload"); 

    console.log("[Host] Payload response:", response.status);
    if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
    }

    const { html, toolResult } = await response.json();
    console.log("[Host] Original toolResult:", JSON.stringify(toolResult, null, 2));

    // iframe を取得
    // Get iframe element
    const iframe = document.getElementById("app-frame");

    // Host 側の Bridge
    // Host-side Bridge to MCP App 
    const bridge = new AppBridge(
        null,   // MCP Client は渡さず、Python 側で MCP 通信を処理する。
                // No MCP Client is provided; Python handles MCP communication.
                // "MCP client connected to the server, or null. When provided, connect will automatically set up forwarding of MCP requests/notifications between the View and the server. When null, you must register handlers manually using the oncalltool, onlistresources, etc. setters."
                // https://apps.extensions.modelcontextprotocol.io/api/classes/app-bridge.AppBridge.html
        { name: "My Host", version: "1.0.0" },
        { serverTools: {} }      // add MCP UI Host Capability
    );

    // iframe App との Transport
    // Transport to iframe App
    const transport = new PostMessageTransport(
        iframe.contentWindow,
        iframe.contentWindow
    );

    // **********************************************************
    // JSON-RPC 観察目的のコード
    // Code for JSON-RPC observation purpose

    // transport.send() の保存
    // save original transport.send() function
    const originalSend = transport.send.bind(transport);

    // Host から iframe App への送信を記録
    // Record data sending from Host to iframe App
    transport.send = async (message, options) => {
        console.log(
            "[JSON-RPC Host -> App]",
            JSON.stringify(message, null, 2)
        );

        return originalSend(message, options);
    };

    // iframe App から Host への受信を記録
    // Record data receiving from iframe App to Host
    window.addEventListener("message", (event) => {
        if (
            event.source === iframe.contentWindow &&
            event.data?.jsonrpc === "2.0"
        ) {
            console.log(
                "[JSON-RPC App -> Host]",
                JSON.stringify(event.data, null, 2)
            );
        }
    });
    // **********************************************************

    // ホスト側 Bridge を Transport に接続
    // Connect Host-side Bridge to Transport
    const connectPromise = bridge.connect(transport);
    console.log("[Host] Bridge connection started");

    // MCP から取得した HTML を表示
    // Display HTML that iframe receives from MCP Server
    iframe.srcdoc = html;
    console.log("[Host] iframe srcdoc assigned");

    // 接続待機
    // Wait until connection is established
    await connectPromise;
    console.log("[Host] Bridge connected");

    // iframe App 側の初期化完了を待つ
    // Wait for completion of iframe App initialization
    bridge.oninitialized = async () => {
        console.log("[Host] App initialized");
        bridge.sendToolInput({ arguments: {} });
        
    };

    // Tool が呼びだされた時のイベントハンドラー
    // Handle an event when tool is called
    bridge.oncalltool = async (params) => {
        console.log("[Host] Tool call request:", params);

        const response = await fetch("/call-tool", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(params)
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const result = await response.json();

        console.log("[Host] Tool call response:", result);

        return result;
    };

}

main().catch(console.error);
