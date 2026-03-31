from pyrogram import Client, filters
import pymysql
import random, string
import os

BOT_TOKEN = os.getenv("8735784393:AAEbpsRBta0mwaTSGAc5kQbNFBXBypANg0U")
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("a1c46c51a69779cc4e72eebf2432f86c")
CHANNEL_ID = int(os.getenv("-1003810735470"))

db = pymysql.connect(
    host=os.getenv("crbcs.in"),
    user=os.getenv("bvrqedsu_file_to_link_tg_bot"),
    password=os.getenv("9938195105@Maa"),
    database=os.getenv("bvrqedsu_file_to_link_tg_bot")
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
