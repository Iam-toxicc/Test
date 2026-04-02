import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from pymongo import MongoClient
from datetime import datetime
import time
import threading

# 🔑 CONFIG
TOKEN = "YOUR_BOT_TOKEN"
ADMIN_IDS = [123456789]
LOGGER_ID = -1001234567890
MONGO_URL = "YOUR_MONGO_URL"

bot = telebot.TeleBot(TOKEN)

# 🍃 MongoDB
client = MongoClient(MONGO_URL)
db = client["telegram_bot"]
users_col = db["users"]

# 👤 Add User
def add_user(user):
    users_col.update_one(
        {"user_id": user.id},
        {
            "$setOnInsert": {
                "user_id": user.id,
                "username": user.username,
                "join_date": datetime.now().strftime("%Y-%m-%d")
            }
        },
        upsert=True
    )

# 🔑 Admin Check
def is_admin(user_id):
    return user_id in ADMIN_IDS

# 📢 LOGGER: USER START
def log_user(user):
    text = f"""🚀 *New User Started*

👤 *Name:* {user.first_name}
🆔 *User ID:* `{user.id}`
📛 *Username:* @{user.username if user.username else 'No Username'}

━━━━━━━━━━━━━━━
📅 Joined Bot"""
    bot.send_message(LOGGER_ID, text, parse_mode="Markdown")

# 💳 LOGGER: PAYMENT
def log_payment(user, amount, utr, name):
    text = f"""🤖 *Auto-Deposit Alert*

👤 *User:* {user.first_name}
🆔 *ID:* `{user.id}`

💰 *Amount:* ₹{amount}
🆔 *UTR:* `{utr}`
🏦 *Name:* {name}

━━━━━━━━━━━━━━━
⚡ Payment Verified Successfully"""
    bot.send_message(LOGGER_ID, text, parse_mode="Markdown")

# 🛡️ Anti-Spam
user_last = {}
def is_spam(uid):
    now = time.time()
    if uid in user_last and now - user_last[uid] < 2:
        return True
    user_last[uid] = now
    return False

# 🚀 START
@bot.message_handler(commands=['start'])
def start(message):
    add_user(message.from_user)
    log_user(message.from_user)

    text = """🔥 *Interfaith Media Store*

💎 Premium & Trusted Service  
⚡ Instant Access | Fast Delivery  

━━━━━━━━━━━━━━━  
👇 *Choose an option below*"""

    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("🛒 Seller", callback_data="seller"),
        InlineKeyboardButton("🤖 Media", callback_data="media")
    )
    markup.add(
        InlineKeyboardButton("📦 Plans", callback_data="plans"),
        InlineKeyboardButton("💳 Buy", callback_data="buy")
    )
    markup.add(
        InlineKeyboardButton("📞 Support", callback_data="support")
    )

    if is_admin(message.from_user.id):
        markup.add(InlineKeyboardButton("👑 Admin Panel", callback_data="admin"))

    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=markup)

# 🔘 CALLBACK
@bot.callback_query_handler(func=lambda call: True)
def callback(call):

    if is_spam(call.from_user.id):
        bot.answer_callback_query(call.id, "⏳ Slow down!")
        return

    # 🛒 SELLER
    if call.data == "seller":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📩 Contact", url="https://t.me/Anyamembership"))
        markup.add(InlineKeyboardButton("🔙 Back", callback_data="back"))

        bot.edit_message_text(
            "🛒 *Trusted Seller*\n\nContact directly for manual purchase.",
            call.message.chat.id,
            call.message.message_id,
            parse_mode="Markdown",
            reply_markup=markup
        )

    # 🤖 MEDIA
    elif call.data == "media":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🤖 Open Bot", url="https://t.me/PayalMembershipBot"))
        markup.add(InlineKeyboardButton("🔙 Back", callback_data="back"))

        bot.edit_message_text(
            "🤖 *Automated Media Bot*\n\nBuy directly via bot.",
            call.message.chat.id,
            call.message.message_id,
            parse_mode="Markdown",
            reply_markup=markup
        )

    # 📦 PLANS
    elif call.data == "plans":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🔙 Back", callback_data="back"))

        bot.edit_message_text(
            """✨ *Available Categories:*

• 👨‍👩‍👧‍👦 𝐈𝐍𝐓𝐄𝐑𝐅𝐀𝐈𝐓𝐇 𝐌𝐄𝐃𝐈𝐀 - ₹223  
• 🖇️ 𝐀𝐋𝐋 𝐏𝐀𝐈𝐃 𝐋𝐈𝐍𝐊𝐒 - ₹199  
• 👅 𝐀𝐍#𝐋 𝐅𝐔#𝐊 - ₹149  
• 💋 𝐀𝐂𝐓𝐑𝐄𝐒𝐒 𝐅#𝐂𝐊 - ₹129  
• 🥵 𝐇𝐈𝐍𝐃𝐈 𝐀𝐃𝐔𝐋𝐓 𝐌𝐎𝐕𝐈𝐄𝐒 - ₹139  
• 🇮🇳 𝐈𝐍𝐃𝐈𝐀𝐍 𝐁𝐋..𝐉𝐎𝐁 - ₹119  

━━━━━━━━━━━━━━━  

🎬 HD Quality  
⚡ Fast Delivery  
🔒 Secure""",
            call.message.chat.id,
            call.message.message_id,
            parse_mode="Markdown",
            reply_markup=markup
        )

    # 💳 BUY
    elif call.data == "buy":
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("🇮🇳 UPI", callback_data="upi"),
            InlineKeyboardButton("🪙 Crypto", callback_data="crypto")
        )
        markup.add(InlineKeyboardButton("🔙 Back", callback_data="back"))

        bot.edit_message_text(
            "💳 *Payment Options*\n\nChoose method 👇",
            call.message.chat.id,
            call.message.message_id,
            parse_mode="Markdown",
            reply_markup=markup
        )

    # 🇮🇳 UPI (DEMO + LOGGER TEST)
    elif call.data == "upi":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🔙 Back", callback_data="buy"))

        bot.edit_message_text(
            "🇮🇳 *UPI Payment*\n\nSend UTR after payment.",
            call.message.chat.id,
            call.message.message_id,
            parse_mode="Markdown",
            reply_markup=markup
        )

    # 🪙 CRYPTO
    elif call.data == "crypto":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🔙 Back", callback_data="buy"))

        bot.edit_message_text(
            "🪙 *Crypto Payment*\n\nSend screenshot after payment.",
            call.message.chat.id,
            call.message.message_id,
            parse_mode="Markdown",
            reply_markup=markup
        )

    # 📞 SUPPORT
    elif call.data == "support":
        bot.answer_callback_query(call.id, "Contact: @AnyaMembership")

    # 👑 ADMIN PANEL
    elif call.data == "admin":
        if not is_admin(call.from_user.id): return

        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("📊 Stats", callback_data="stats"),
            InlineKeyboardButton("📢 Broadcast", callback_data="broadcast")
        )
        markup.add(InlineKeyboardButton("🔙 Back", callback_data="back"))

        bot.edit_message_text(
            "👑 *Admin Panel*",
            call.message.chat.id,
            call.message.message_id,
            parse_mode="Markdown",
            reply_markup=markup
        )

    # 📊 STATS
    elif call.data == "stats":
        total = users_col.count_documents({})
        bot.send_message(call.message.chat.id, f"📊 Users: {total}")

    # 📢 BROADCAST
    elif call.data == "broadcast":
        bot.send_message(call.message.chat.id, "Send message:")
        bot.register_next_step_handler(call.message, send_all)

    # 🔙 BACK
    elif call.data == "back":
        start(call.message)

# 📢 BROADCAST FUNC
def send_all(message):
    for user in users_col.find():
        try:
            bot.send_message(user["user_id"], message.text)
        except:
            pass
    bot.send_message(message.chat.id, "✅ Done")

# ▶️ RUN
bot.polling()
