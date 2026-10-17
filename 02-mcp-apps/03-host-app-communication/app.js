import { App } from "@modelcontextprotocol/ext-apps";

const app = new App(
    { name: "Hello App", version: "1.0.0" },
    {},
    { autoResize: false }
);

const status = document.getElementById("status");
const resultElement = document.getElementById("result");


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

// Host に接続
// Connect to Host
async function main() {
    try {
        await app.connect();   // Use PostMessageTransport by default

        status.textContent = "Connected to Host";
        console.log("[App] Connected");
    } catch (error) {
        status.textContent = "Connection failed";
        console.error(error);
    }
}

main();
