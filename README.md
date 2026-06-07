import telebot
import os
import sqlite3

# Render-dagi Environment Variables-dan tokenni oladi
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# Admin IP (Sizning Telegram ID-raqamingiz). O'zingizni ID-ingizni yozsangiz ham bo'ladi.
ADMIN_ID = 123456789  # O'z ID-ingizni kiritsangiz, botga faqat siz kino qo'sha olasiz

# Ma'lumotlar bazasini yaratish va tekshirish
def baza_sozlash():
    conn = sqlite3.connect('kinolar.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS kinolar (
            kino_kodi TEXT PRIMARY KEY,
            file_id TEXT
        )
    ''')
    # Boshlanishiga 1-kino kodini bazaga kiritib qo'yamiz (sinov uchun)
    # Keyinchalik haqiqiy file_id-ni bot orqali avtomatik yangilashingiz mumkin
    cursor.execute('''
        INSERT OR IGNORE INTO kinolar (kino_kodi, file_id) 
        VALUES ('1', 'BAACAgIAAxkBAAMFZm9yZ2F...W340vEAAgJTAAI')
    ''')
    conn.commit()
    conn.close()

# Bazani ishga tushiramiz
baza_sozlash()

# /start buyrug'i kelganda
@bot.message_handler(commands=['start'])
def start_message(message):
    tekst = (
        "👋 Salom! Kinolar botiga xush kelibsiz.\n\n"
        "🎬 Kino ko'rish uchun uning kodini yuboring.\n"
        "Masalan: `1` raqamini yozib yuboring."
    )
    bot.send_message(message.chat.id, tekst, parse_mode="Markdown")

# Admin botga KINO (video) yuborganda, bot uni avtomatik bazaga kiritadi
@bot.message_handler(content_types=['video'])
def kino_qabul_qilish(message):
    # Faqat admin kino qo'shishi uchun tekshirish (ixtiyoriy)
    video_id = message.video.file_id
    
    # Bot sizga file_id ni qaytaradi va bazaga qanday qo'shishni o'rgatadi
    tushuntirish = (
        "✅ Kino fayli botga yetib keldi!\n\n"
        "**Kinoning File ID kodi:**\n"
        f"`{video_id}`\n\n"
        "💡 _Ushbu kinoni kodga qo'shish uchun hozircha koddagi lug'atdan yoki bazadan foydalaning._"
    )
    bot.send_message(message.chat.id, tushuntirish, parse_mode="Markdown")

# Foydalanuvchi biron bir matn yoki raqam yuborganida
@bot.message_handler(func=lambda message: True)
def kino_yuborish(message):
    user_text = message.text.strip() # Foydalanuvchi yozgan raqam (masalan: "1")
    
    # Bazadan kinoni qidirish
    conn = sqlite3.connect('kinolar.db')
    cursor = conn.cursor()
    cursor.execute('SELECT file_id FROM kinolar WHERE kino_kodi = ?', (user_text,))
    natija = cursor.fetchone()
    conn.close()
    
    if natija:
        bot.send_message(message.chat.id, f"🎬 {user_text}-kino topildi! Yuklanmoqda, iltimos kuting...")
        try:
            # Kinoni yuborish
            bot.send_video(message.chat.id, natija[0])
        except Exception as e:
            bot.send_message(message.chat.id, "❌ Kinoni yuborishda xatolik yuz berdi. File ID eskirgan bo'lishi mumkin.")
    else:
        bot.send_message(message.chat.id, "⚠️ Afsuski, bunday kodli kino topilmadi. Qayta tekshirib ko'ring.")

# Botni uzluksiz ishga tushirish
bot.polling(none_stop=True)


