from pyrogram import Client, filters
import pymysql
import random, string
import os

# ✅ Environment variables read correctly
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

db = pymysql.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    database=os.getenv("DB_NAME")
)
cursor = db.cursor()

app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def generate_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

@app.on_message(filters.private & filters.media)
async def save_file(client, message):
    sent = await message.copy(CHANNEL_ID)
    unique_id = generate_id()

    cursor.execute(
        "INSERT INTO files (id, channel_id, message_id) VALUES (%s, %s, %s)",
        (unique_id, CHANNEL_ID, sent.id)
    )
    db.commit()

    link = f"https://t.me/crbcsfiletolinkcreatorbot?start={unique_id}"
    await message.reply(f"🔗 Your Link:\n{link}")

@app.on_message(filters.command("start"))
async def start(client, message):
    if len(message.command) > 1:
        key = message.command[1]

        cursor.execute("SELECT channel_id, message_id FROM files WHERE id=%s", (key,))
        data = cursor.fetchone()

        if data:
            await client.copy_message(
                chat_id=message.chat.id,
                from_chat_id=data[0],
                message_id=data[1]
            )
        else:
            await message.reply("❌ File not found")
    else:
        await message.reply("📤 Send file to get link")

app.run()
