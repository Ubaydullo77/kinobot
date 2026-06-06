import telebot

# Bot kaliti
TOKEN = "AAEe_p1_xbPGcNSbvnRK_7n_oxbXSPMtM9k"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, "Salom! Kinobot muvaffaqiyatli ishga tushdi!")

# Botni tinimsiz ishlatish buyrug'i
bot.infinity_polling()

