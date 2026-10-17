
from pathlib import Path
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

BASE_DIR = Path(__file__).parent


@app.get("/sandbox.html", response_class=HTMLResponse)
async def sandbox():
    return (BASE_DIR / "sandbox.html").read_text(
        encoding="utf-8"
    )


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8081
    )
