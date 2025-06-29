from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
import httpx
import os

# Your Telegram Bot Token
BOT_TOKEN = os.getenv("BOT_TOKEN", "7923824746:AAHckBCLY9_7NAdjRyHXi6BAWHAPVJ2BIkw")

app = FastAPI()

@app.get("/stream")
async def stream_video(file_id: str):
    if not file_id:
        raise HTTPException(status_code=400, detail="file_id required")

    # Step 1: Get file_path from Telegram
    async with httpx.AsyncClient() as client:
        file_info = await client.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}")
        data = file_info.json()
        if not data.get("ok"):
            raise HTTPException(status_code=404, detail="Invalid file_id")

        file_path = data["result"]["file_path"]

        # Step 2: Stream file from Telegram CDN
        tg_file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
        tg_stream = await client.get(tg_file_url, stream=True)

        if tg_stream.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to fetch video stream")

        return StreamingResponse(
            tg_stream.aiter_bytes(),
            media_type="video/mp4",
            headers={
                "Accept-Ranges": "bytes",
                "Access-Control-Allow-Origin": "*"
            }
        )
