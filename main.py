from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_ID = 22250562
API_HASH = "07754d3bdc27193318ae5f6e6c8016af"
BOT_TOKEN = "7923824746:AAHckBCLY9_7NAdjRyHXi6BAWHAPVJ2BIkw"

CHANNEL_USERNAME = "@dumprjddisb"  # Channel to monitor
MINI_APP_URL = "https://praneeth-coder-2005.github.io/Mini-App-Stream/"  # Replace with your GitHub Pages Mini App

app = Client("video_stream_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.channel & filters.video)
async def video_handler(client, message):
    if message.chat.username != CHANNEL_USERNAME.replace("@", ""):
        return  # Ignore other channels

    file_id = message.video.file_id
    miniapp_link = f"{MINI_APP_URL}/?file_id={file_id}"

    await client.send_video(
        chat_id=CHANNEL_USERNAME,
        video=file_id,
        caption="🎬 Watch this video in Mini App!",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("▶️ Watch Now", url=miniapp_link)
        ]])
    )

app.run()
