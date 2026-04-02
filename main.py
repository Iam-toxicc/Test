import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8570863778:AAF48XmNGNzKWQym2AZRvyrvMtNk6E9XKAg"
bot = telebot.TeleBot(TOKEN)

# 🔹 START COMMAND
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

# 🔹 CALLBACK HANDLER
@bot.callback_query_handler(func=lambda call: True)
def callback(call):

    # 👉 SELLER BUTTON
    if call.data == "seller":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "📩 Contact here: @AnyaMembership")

    # 👉 MEDIA BUTTON (INLINE EDIT)
    elif call.data == "media":
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("🤖 Open Bot", url="https://t.me/PayalMembershipBot"),
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
