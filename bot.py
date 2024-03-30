from yt_dlp import YoutubeDL
import telebot
from telebot import types

TOKEN = 'TOKEN'
bot = telebot.TeleBot(TOKEN)

user_choice = {}

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Пришли мне ссылку на видео YouTube, и я помогу тебе скачать его аудио или видео.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    if message.text.startswith('http'):
        url = message.text
        send_download_link(chat_id, url)
    else:
        bot.reply_to(message, "Пожалуйста, отправь мне ссылку на YouTube.")

def send_download_link(chat_id, video_url):
    # Используем yt-dlp для получения прямой ссылки на скачивание
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=False)
        if 'url' in info_dict:
            download_url = info_dict['url']
            bot.send_message(chat_id, f"Ссылка для скачивания: {download_url}")
        else:
            bot.send_message(chat_id, "Не удалось получить ссылку для скачивания.")

bot.infinity_polling()
