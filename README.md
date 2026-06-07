import telebot
import os

BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# Bu funksiya siz yuborgan videoni ushlab, uning ID-sini aniqlaydi
@bot.message_handler(content_types=['video'])
def get_video_id(message):
    video_id = message.video.file_id
    
    # ID kodini sizga xabar qilib qaytaradi
    bot.send_message(
        message.chat.id, 
        f"Kino qabul qilindi! ✅\n\n"
        f"Mana uning File ID kodi (shuni nusxalab olasiz):\n\n"
        f"`{video_id}`", 
        parse_mode="Markdown"
    )

bot.polling(none_stop=True)

