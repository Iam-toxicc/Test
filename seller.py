import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8570863778:AAF48XmNGNzKWQym2AZRvyrvMtNk6E9XKAg"
bot = telebot.TeleBot(TOKEN)

# 🔹 START
@bot.message_handler(commands=['start'])
def start(message):
    text = """👋 Welcome to Interfaith Media

If you want to buy official media of Interfaith, just DM now.

🔐 Trusted | ✅ Secure

📩 @AnyaMembership"""

    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("Seller", callback_data="seller"),
        InlineKeyboardButton("Media Bot", callback_data="media")
    )

    bot.send_message(message.chat.id, text, reply_markup=markup)

# 🔹 CALLBACK
@bot.callback_query_handler(func=lambda call: True)
def callback(call):

    # 👉 SELLER BUTTON (INLINE)
    if call.data == "seller":
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("📩 Contact Seller", url="https://t.me/Anyamembership")
        )
        markup.add(
            InlineKeyboardButton("🔙 Back", callback_data="back")
        )

        bot.edit_message_text(
            """🛒 Seller

Wanna buy Media from a Trusted and Real Person? Then contact me.

👇 Click below:""",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    # 👉 MEDIA BUTTON
    elif call.data == "media":
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("🤖 Open Bot", url="https://t.me/PayalMembershipBot")
        )
        markup.add(
            InlineKeyboardButton("🔙 Back", callback_data="back")
        )

        bot.edit_message_text(
            """🤖 Media Bot

If you want to buy directly through our bot, then check out our trusted bot:

👉 @AnyaMembershipBot""",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    # 👉 BACK BUTTON
    elif call.data == "back":
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("Seller", callback_data="seller"),
            InlineKeyboardButton("Media Bot", callback_data="media")
        )

        bot.edit_message_text(
            """👋 Welcome to Interfaith Media

If you want to buy official media of Interfaith, just DM now.

🔐 Trusted | ✅ Secure

📩 @AnyaMembership""",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

bot.polling()
