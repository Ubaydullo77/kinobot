import telebot

# Yangi va to'liq tokeningiz shu yerga tushdi
TOKEN = "8840928379:AAEe_p1_xbPGcnSbvnRK_7n_oxbXSPMtM9k"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, "Salom! Kinobot muvaffaqiyatli ishga tushdi!")

# Botni tinimsiz ishlatish buyrug'i
bot.infinity_polling()
