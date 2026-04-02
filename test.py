import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8570863778:AAF48XmNGNzKWQym2AZRvyrvMtNk6E9XKAg"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    text = """👋 Welcome to Interfaith Media

If you want to buy official media of Interfaith, just DM now.

🔐 Trusted | ✅ Secure

📩 @AnyaMembership"""

    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton("Seller", callback_data="seller")
    btn2 = InlineKeyboardButton("Media Bot", callback_data="media")

    markup.add(btn1)
    markup.add(btn2)

    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "seller":
        bot.send_message(call.message.chat.id, "📩 Contact here: @AnyaMembership")
    
    elif call.data == "media":
        bot.send_message(call.message.chat.id, "🎬 Media Bot section coming soon...")

bot.polling()
