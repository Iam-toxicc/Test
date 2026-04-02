import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from pymongo import MongoClient
from datetime import datetime
import threading
import time

# 🔑 CONFIG
TOKEN = "YOUR_BOT_TOKEN"
ADMIN_IDS = [8388076792, 8238387029]  # 👈 multiple admins
LOGGER_ID = -1003879081687
MONGO_URL = "mongodb+srv://shourya6055_db_user:Ngt1JdbWoFXhJ9RX@toxic.lsnylyq.mongodb.net/?appName=Toxic"

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

# 📢 Logger
def log_user(user):
    text = f"""🚀 New User Started Bot

👤 {user.first_name}
🆔 {user.id}
📛 @{user.username if user.username else 'No username'}
"""
    bot.send_message(LOGGER_ID, text)

def log_click(call, action):
    user = call.from_user
    text = f"""📊 Button Click

👤 {user.first_name}
🆔 {user.id}
🔘 {action}
"""
    bot.send_message(LOGGER_ID, text)

# 🛡️ Anti Spam
user_last_click = {}
def is_spam(user_id):
    now = time.time()
    if user_id in user_last_click:
        if now - user_last_click[user_id] < 2:
            return True
    user_last_click[user_id] = now
    return False

# 🚀 START
@bot.message_handler(commands=['start'])
def start(message):
    add_user(message.from_user)
    log_user(message.from_user)

    text = """🔥 Interfaith Media Store

💎 Premium & Trusted Service  
⚡ Fast Delivery  

👇 Choose an option below"""

    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("🛒 Seller", callback_data="seller"),
        InlineKeyboardButton("🤖 Media Bot", callback_data="media")
    )
    markup.add(
        InlineKeyboardButton("📦 Plans", callback_data="plans"),
        InlineKeyboardButton("📞 Support", callback_data="support")
    )

    # 👑 Admin Button
    if is_admin(message.from_user.id):
        markup.add(InlineKeyboardButton("👑 Admin Panel", callback_data="open_admin"))

    bot.send_message(message.chat.id, text, reply_markup=markup)

# 🔘 CALLBACK
@bot.callback_query_handler(func=lambda call: True)
def callback(call):

    if is_spam(call.from_user.id):
        bot.answer_callback_query(call.id, "⏳ Slow down!")
        return

    # 🛒 SELLER
    if call.data == "seller":
        log_click(call, "Seller")

        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("📩 Contact Seller", url="https://t.me/Anyamembership")
        )
        markup.add(InlineKeyboardButton("🔙 Back", callback_data="back"))

        bot.edit_message_text(
            """🛒 Seller

Wanna buy Media from a Trusted and Real Person? Then contact me.

👇 Click below:""",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    # 🤖 MEDIA
    elif call.data == "media":
        log_click(call, "Media")

        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("🤖 Open Bot", url="https://t.me/PayalMembershipBot")
        )
        markup.add(InlineKeyboardButton("🔙 Back", callback_data="back"))

        bot.edit_message_text(
            """🤖 Media Bot

If you want to buy directly through our bot, then check out our trusted bot:

👉 @AnyaMembershipBot""",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    # 📦 PLANS
    elif call.data == "plans":
        log_click(call, "Plans")

        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🔙 Back", callback_data="back"))

        bot.edit_message_text(
            "📦 Plans:\n\nBasic - ₹99\nPremium - ₹199",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    # 📞 SUPPORT
    elif call.data == "support":
        log_click(call, "Support")

        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🔙 Back", callback_data="back"))

        bot.edit_message_text(
            "📞 Support: @AnyaMembership",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    # 👑 ADMIN PANEL
    elif call.data == "open_admin":
        if not is_admin(call.from_user.id):
            return

        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("📊 Stats", callback_data="admin_stats"),
            InlineKeyboardButton("📢 Broadcast", callback_data="admin_broadcast")
        )
        markup.add(
            InlineKeyboardButton("📅 Report", callback_data="admin_report"),
            InlineKeyboardButton("🔙 Back", callback_data="back")
        )

        bot.edit_message_text(
            "👑 Admin Panel",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    # 📊 ADMIN STATS
    elif call.data == "admin_stats":
        if not is_admin(call.from_user.id):
            return

        total = users_col.count_documents({})
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, f"📊 Total Users: {total}")

    # 📢 ADMIN BROADCAST
    elif call.data == "admin_broadcast":
        if not is_admin(call.from_user.id):
            return

        bot.send_message(call.message.chat.id, "✍️ Send message:")
        bot.register_next_step_handler(call.message, send_all)

    # 📅 ADMIN REPORT
    elif call.data == "admin_report":
        if not is_admin(call.from_user.id):
            return

        total = users_col.count_documents({})
        today = datetime.now().strftime("%Y-%m-%d")
        new_users = users_col.count_documents({"join_date": today})

        bot.send_message(
            call.message.chat.id,
            f"""📅 Report

👥 Total Users: {total}
🆕 New Today: {new_users}"""
        )

    # 🔙 BACK
    elif call.data == "back":
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("🛒 Seller", callback_data="seller"),
            InlineKeyboardButton("🤖 Media Bot", callback_data="media")
        )
        markup.add(
            InlineKeyboardButton("📦 Plans", callback_data="plans"),
            InlineKeyboardButton("📞 Support", callback_data="support")
        )

        if is_admin(call.from_user.id):
            markup.add(InlineKeyboardButton("👑 Admin Panel", callback_data="open_admin"))

        bot.edit_message_text(
            """🔥 Interfaith Media Store

💎 Premium & Trusted Service  
⚡ Fast Delivery  

👇 Choose an option below""",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

# 📢 Broadcast Function
def send_all(message):
    users = users_col.find()
    success, failed = 0, 0

    for user in users:
        try:
            bot.send_message(user["user_id"], message.text)
            success += 1
        except:
            failed += 1

    bot.send_message(message.chat.id, f"✅ {success} Sent\n❌ {failed} Failed")

# ⏰ DAILY REPORT AUTO
def daily_report():
    while True:
        total = users_col.count_documents({})
        today = datetime.now().strftime("%Y-%m-%d")
        new_users = users_col.count_documents({"join_date": today})

        bot.send_message(
            LOGGER_ID,
            f"""📅 Daily Report

👥 Total Users: {total}
🆕 New Today: {new_users}"""
        )

        time.sleep(86400)

threading.Thread(target=daily_report).start()

# ▶️ RUN
bot.polling()
