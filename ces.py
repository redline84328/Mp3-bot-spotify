from pyrogram import Client, filters
import yt_dlp
import requests
import os
import re
from bs4 import BeautifulSoup

API_ID = 26345223
API_HASH = "2d82aca171ac54b09a103cccb4ba5c7f"
BOT_TOKEN = "7971690119:AAHFfd4lD5LBw-bFI0SQbQ2_6YwdIbexg9E"

app = Client("spotify_mp3_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Mahnı yükləmə funksiyası (YouTube MP3)
def download_mp3(query):
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'cookiefile': 'downloads/cookies.txt',  # YouTube cookie faylı
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=True)
            entries = info.get('entries')
            if not entries:
                return None
            filename = ydl.prepare_filename(entries[0])
            return filename.replace(".webm", ".mp3").replace(".m4a", ".mp3")
    except Exception as e:
        print(f"Xəta: {e}")
        return None

# Spotify linkindən mahnı adını çıxarma
def extract_title_from_spotify(spotify_url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(spotify_url, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")
        title = soup.title.string
        title = title.replace(" - song and lyrics by", "").strip()
        return title
    except:
        return None

# Başlanğıc mesajı
@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("🎵 Spotify linki və ya mahnı adını göndər, MP3 şəklində yollayım!")

# İstifadəçi mesajı (Spotify link və ya ad)
@app.on_message(filters.text & ~filters.command("start"))
async def handle_message(client, message):
    user_input = message.text.strip()
    await message.reply("🔍 Axtarılır...")

    if "open.spotify.com/track" in user_input:
        query = extract_title_from_spotify(user_input)
        if not query:
            await message.reply("❌ Spotify linki tanınmadı.")
            return
    else:
        query = user_input

    filename = download_mp3(query)
    if not filename or not os.path.exists(filename):
        await message.reply("❌ Mahnı tapılmadı və ya yüklənə bilmədi.")
        return

    await message.reply_audio(audio=filename, caption=f"✅ MP3 Hazır: {query}")
    os.remove(filename)

app.run()
