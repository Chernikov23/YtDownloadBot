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
def echo_all(message):
    chat_id = message.chat.id
    if message.text.startswith('http'):
        # Сохраняем ссылку и предлагаем пользователю выбор
        user_choice[chat_id] = {'url': message.text}
        markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Аудио', 'Видео')
        msg = bot.reply_to(message, "Хочешь скачать аудио или видео?", reply_markup=markup)
        bot.register_next_step_handler(msg, process_choice)
    else:
        bot.reply_to(message, "Пожалуйста, отправь мне ссылку на YouTube.")

def process_choice(message):
    chat_id = message.chat.id
    choice = message.text
    user_choice[chat_id]['choice'] = choice

    if choice == 'Аудио':
        download_and_send_file(chat_id, audio=True)
    elif choice == 'Видео':
        download_and_send_file(chat_id, audio=False)
    else:
        bot.reply_to(message, "Пожалуйста, выбери Аудио или Видео.")

def download_and_send_file(chat_id, audio=True):
    url = user_choice[chat_id]['url']
    ydl_opts = {
        'format': 'bestaudio' if audio else 'best',
        'outtmpl': '/tmp/%(id)s.%(ext)s',
    }
    
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        filepath = ydl.prepare_filename(info_dict)
        # Отправляем файл
        if audio:
            bot.send_audio(chat_id, audio=open(filepath, 'rb'))
            print('Скачивание аудио завершено')
        else:
            bot.send_video(chat_id, video=open(filepath, 'rb'))
            print('Скачивание видео завершено')

bot.infinity_polling()
