import {
    AppBridge,
    PostMessageTransport
} from "@modelcontextprotocol/ext-apps/app-bridge";


async function main() {
    console.log("[Host] Main started");

    // FastAPI 経由で MCP Tool Result と UI Resource を取得
    // Retrieve MCP Tool Result and UI Resource via FastAPI
    const response = await fetch("/payload"); 

    console.log("[Host] Payload response:", response.status);
    if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
    }

    const { html, toolResult } = await response.json();
    console.log("[Host] Original toolResult:", JSON.stringify(toolResult, null, 2));

    // Sandbox Proxy 用 の iframe を取得
    // Get iframe element for Sandbox Proxy
    const iframe = document.getElementById("app-frame");

    iframe.sandbox = "allow-scripts allow-same-origin";

    // Sandbox Proxy 経由で MCP App と通信する Host 側の Bridge
    // Host-side Bridge for communicating with MCP App via Sandbox Proxy
    const bridge = new AppBridge(
        null,   // MCP Client は渡さず、Python 側で MCP 通信を処理する。
                // No MCP Client is provided; Python handles MCP communication.
                // "MCP client connected to the server, or null. When provided, connect will automatically set up forwarding of MCP requests/notifications between the View and the server. When null, you must register handlers manually using the oncalltool, onlistresources, etc. setters."
                // https://apps.extensions.modelcontextprotocol.io/api/classes/app-bridge.AppBridge.html
        { name: "My Host", version: "1.0.0" },
        { serverTools: {} }      // add MCP UI Host Capability
    );

    // Sandbox Proxy との Transport
    // Transport to Sandbox Proxy
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

    // Transport 経由で Host から Sandbox Proxy へ送信する JSON-RPC を記録
    // Log JSON-RPC messages sent from Host to Sandbox Proxy via Transport
    transport.send = async (message, options) => {

        // HTML全文がログに表示されるのを防ぐ
        // Omit the HTML content from the log
        const logMessage =
            message.method === "ui/notifications/sandbox-resource-ready"
                ? {
                    ...message,
                    params: {
                        ...message.params,
                        html: "[MCP App HTML omitted]"
                    }
                }
                : message;

        console.log(
            "[JSON-RPC Host -> Sandbox]",
            JSON.stringify(logMessage, null, 2)
        );

        return originalSend(message, options);
    };
    // **********************************************************
    
    console.log("[Host] Origin:", window.origin);
    console.log("[Host] Location:", window.location.href);

    // Sandbox Proxy からの JSON-RPC メッセージを観察
    // Observe JSON-RPC messages from Sandbox Proxy
    window.addEventListener("message", (event) => {

        // 送信元の Window と Origin を検証
        // Verify source Window and Origin
        if (
            event.source !== iframe.contentWindow ||
            event.origin !== "http://localhost:8081"
        ) {
            return;
        }

        // JSON-RPC 観察用ログ
        // JSON-RPC observation
        if (event.data?.jsonrpc === "2.0") {
            console.log(
                "[JSON-RPC Sandbox -> Host]",
                JSON.stringify(event.data, null, 2)
            );

            console.log(
                "[Security] Message origin:",
                event.origin
            );

            console.log(
                "[Security] Source is Sandbox iframe:",
                event.source === iframe.contentWindow
            );
        }
    });


    // Sandbox Proxy の準備完了通知を処理
    // Handle Sandbox Proxy ready notification
    bridge.addEventListener("sandboxready", async () => {
        console.log("[Host] Sandbox Proxy is ready");

        // MCP App の HTML と Inner iframe の Sandbox 設定を送信
        // Send MCP App HTML and inner iframe sandbox configuration
        await bridge.sendSandboxResourceReady({
            html: html,
            sandbox: "allow-scripts"
        });

        console.log("[Host] Resource sent to Sandbox");
    });

    // Sandbox Proxy 経由で MCP App の初期化完了通知を受信
    // Handle MCP App initialization notification via Sandbox Proxy
    bridge.oninitialized = async () => {
        console.log("[Host] App initialized");
        bridge.sendToolInput({ arguments: {} });
        
    };

    // MCP App からの Tool 呼び出し要求を処理
    // Handle Tool call requests from MCP App
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

    // ホスト側 Bridge を Transport に接続
    // Connect Host-side Bridge to Transport
    const connectPromise = bridge.connect(transport);
    console.log("[Host] Bridge connection started");

    // iframe に Sandbox Proxy を表示
    // Set source of iframe to sandbox proxy
    iframe.src = "http://localhost:8081/sandbox.html";
    console.log("[Host] Sandbox iframe URL assigned");

    // 接続待機
    // Wait until connection is established
    await connectPromise;
    console.log("[Host] Bridge connected");
}

main().catch(console.error);
