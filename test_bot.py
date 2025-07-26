from pyrogram import Client, filters

api_id = 26345223
api_hash = "2d82aca171ac54b09a103cccb4ba5c7f"
bot_token = "8493485468:AAH-zubeee0MdIz2aNldj0v3dbPHH0wBfmM"

app = Client(
    "test_bot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token,
    parse_mode="html"  # Burada təyin olunur
)

@app.on_message(filters.command("start"))
async def start_handler(client, message):
    await message.reply(
        "<b>Salam!</b>\nBu bot işə düşdü.",
    )

@app.on_message(filters.command("yer"))
async def yer_handler(client, message):
    args = message.text.split(maxsplit=3)
    if len(args) < 4:
        await message.reply("İstifadə: /yer <lat> <lon> <ad>")
        return

    lat = args[1]
    lon = args[2]
    label = args[3]

    maps_url = f"https://www.google.com/maps?q=loc:{lat},{lon} ({label})"
    text = f"📍 <b>{label}</b>\n<a href='{maps_url}'>Xəritədə bax</a>"

    await message.reply(text)

app.run()
