import telebot
import yt_dlp
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

CHANNEL_ID = '@iGoViral'  # Replace with your channel's ID

# Check if the user is a member of the channel
def is_member(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        return False

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Send me a video link, and I'll download it for you!")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    user_id = message.from_user.id

    if not is_member(user_id):
        bot.reply_to(message, "Please join our channel first: @iGoViral")
        return

    url = message.text.strip()
    ydl_opts = {'format': 'bestvideo+bestaudio/best', 'outtmpl': 'video.%(ext)s'}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        with open(filename, "rb") as video:
            bot.send_video(message.chat.id, video)
        os.remove(filename)
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")

bot.polling()