
import telebot

# Bot tokeningiz kiritildi
TOKEN = "8840928379:AAEe_p1_xbPGcnSbvnRK_7n_oxbXSPMtM9k"
bot = telebot.TeleBot(TOKEN)

# Kinolar ro'yxati (Kino kodi va uning Telegram'dagi File IDsi)
kinolar = {
    "1": "BAACAgIAAxkBAAMFZm9yZ2F...W340vEAAgJTAAI"  # Test uchun vaqtincha kod
}

# /start buyrug'i kelganda javob berish
@bot.message_handler(commands=['start'])
def start_message(message):
    matn = (
        "👋 Salom! Kinolar botiga xush kelibsiz.\n\n"
        "🎬 Kino ko'rish uchun uning kodini yuboring (Masalan: 1)"
    )
    bot.send_message(message.chat.id, matn)

# Botga yuborilgan har qanday videoning File ID sini aniqlash
@bot.message_handler(content_types=['video'])
def get_video_id(message):
    video_id = message.video.file_id
    bot.send_message(
        message.chat.id, 
        f"✅ Kino qabul qilindi!\n\n"
        f"Sizga kerakli **File ID** kodi:\n\n"
        f"`{video_id}`\n\n"
        f"💡 Ushbu kodni nusxalab, bot.py ichidagi 'kinolar' ro'yxatiga qo'shib qo'ying.", 
        parse_mode="Markdown"
    )

# Foydalanuvchi matn yoki raqam yuborganida kinoni qidirish
@bot.message_handler(func=lambda message: True)
def send_kino(message):
    user_text = message.text.strip()
    
    if user_text in kinolar:
        bot.send_message(message.chat.id, f"🎬 {user_text}-kino topildi! Yuklanmoqda...")
        try:
            bot.send_video(message.chat.id, kinolar[user_text])
        except Exception as e:
            bot.send_message(message.chat.id, "❌ Kinoni yuborishda xatolik bo'ldi.")
    else:
        bot.send_message(message.chat.id, "⚠️ Afsuski, bunday kodli kino topilmadi.")

# Botni uzluksiz ishga tushirish
bot.infinity_polling()
