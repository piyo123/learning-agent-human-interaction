import { App } from "@modelcontextprotocol/ext-apps";

const app = new App(
    { name: "Hello App", version: "1.0.0" },
    {},
    { autoResize: false }
);

const status = document.getElementById("status");
const resultElement = document.getElementById("result");
const nameInput = document.getElementById("name");
const button = document.getElementById("call-tool");


app.ontoolinput = (params) => {
    console.log("[App] Tool input:", params);
};


// Host から Tool 結果を受信
// Receive tool result from Host
app.ontoolresult = (result) => {
    console.log("[App] Tool result:", result);

    const text = result.content?.find(
        item => item.type === "text"
    )?.text;

    resultElement.textContent = text ?? "No result";
};


// ボタンクリック時に MCP Server の Tool を呼び出す
// Call tool on MCP Server when clicking button
button.addEventListener("click", async (event) => {

    const name = nameInput.value.trim();

    if (!name) {
        return;
    }

    button.disabled = true;
    resultElement.textContent = "Calling Tool...";

    try {
        // ユーザー入力を引数に MCP Server の Tool を呼び出す
        // Call MCP Server Tool with user input.
        const result = await app.callServerTool({
            name: "say_hello",
            arguments: {
                name: name
            }
        });

        console.log("[App] Tool call response:", result);

        if (result.isError) {
            throw new Error("MCP Tool returned an error");
        }

        const text = result.content?.find(
            item => item.type === "text"
        )?.text;

        // 実行結果が分かりやすいように Tool Resultを送信する前に1秒待機する。
        // Wait for 1 second to observe the UI state.
        await new Promise(resolve => setTimeout(resolve, 1000));

        resultElement.textContent = text ?? "No result";

    } catch (error) {
        console.error("[App] Tool call failed:", error);
        resultElement.textContent = "Tool call failed";

    } finally {
        button.disabled = false;
    }
});



// Host に接続
// Connect to Host
async function main() {
    try {
        await app.connect();   // Use PostMessageTransport by default

        status.textContent = "Connected to Host";
        button.disabled = false;
        console.log("[App] Connected");
    } catch (error) {
        status.textContent = "Connection failed";
        console.error(error);
    }
}

main();
