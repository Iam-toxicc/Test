import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from pymongo import MongoClient
from datetime import datetime
import threading
import time

# 🔑 CONFIG
TOKEN = "8570863778:AAF48XmNGNzKWQym2AZRvyrvMtNk6E9XKAg"
ADMIN_IDS = [8388076792, 8238387029]
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

# 🔥 SAFE SEND (MAIN FIX)
def safe_send(chat_id, text, **kwargs):
    try:
        bot.send_message(chat_id, text, **kwargs)
        return True
    except Exception as e:
        if "blocked by the user" in str(e):
            try:
                bot.send_message(
                    LOGGER_ID,
                    f"""🚫 User Blocked Bot

🆔 {chat_id}"""
                )
            except:
                pass

            users_col.delete_one({"user_id": chat_id})

        return False

# 📢 LOGGER START
def log_user(user):
    safe_send(
        LOGGER_ID,
        f"""🚀 New User Started

👤 {user.first_name}
🆔 {user.id}
📛 @{user.username if user.username else 'No username'}"""
    )

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

    text = """🔥 *Interfaith Media Store*

💎 Premium & Trusted Service  
⚡ Instant Access | Fast Delivery  

━━━━━━━━━━━━━━━  
👇 *Select an option below*"""

    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("🛒 Seller", callback_data="seller"),
        InlineKeyboardButton("🤖 Media Bot", callback_data="media")
    )
    markup.add(
        InlineKeyboardButton("📦 Plans", callback_data="plans"),
        InlineKeyboardButton("📞 Support", callback_data="support")
    )

    if is_admin(message.from_user.id):
        markup.add(InlineKeyboardButton("👑 Admin Panel", callback_data="open_admin"))

    safe_send(
        message.chat.id,
        text,
        parse_mode="Markdown",
        reply_markup=markup
    )

# 🔘 CALLBACK
@bot.callback_query_handler(func=lambda call: True)
def callback(call):

    if is_spam(call.from_user.id):
        bot.answer_callback_query(call.id, "⏳ Slow down!")
        return

    # 🛒 SELLER
    if call.data == "seller":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📩 Contact Seller", url="https://t.me/Anyamembership"))
        markup.add(InlineKeyboardButton("🔙 Back", callback_data="back"))

        bot.edit_message_text(
            """🛒 *Trusted Seller*

Buy directly from a real & verified seller.

👇 Click below to contact""",
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
            """🤖 *Automated Media Bot*

Buy directly through our trusted bot system.

👉 @AnyaMembershipBot""",
            call.message.chat.id,
            call.message.message_id,
            parse_mode="Markdown",
            reply_markup=markup
        )

    # 📦 PLANS
    elif call.data == "plans":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📦 View Plans", url="https://t.me/PayalMembershipBot"))
        markup.add(InlineKeyboardButton("🔙 Back", callback_data="back"))

        bot.edit_message_text(
            """📦 *Plans & Purchase*

Visit our official bot to check all plans and buy instantly.

👇 Click below""",
            call.message.chat.id,
            call.message.message_id,
            parse_mode="Markdown",
            reply_markup=markup
        )

    # 📞 SUPPORT
    elif call.data == "support":
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
            "👑 *Admin Panel*",
            call.message.chat.id,
            call.message.message_id,
            parse_mode="Markdown",
            reply_markup=markup
        )

    # 📊 STATS
    elif call.data == "admin_stats":
        if not is_admin(call.from_user.id):
            return

        total = users_col.count_documents({})
        safe_send(call.message.chat.id, f"📊 Total Users: {total}")

    # 📢 BROADCAST
    elif call.data == "admin_broadcast":
        if not is_admin(call.from_user.id):
            return

        safe_send(call.message.chat.id, "✍️ Send message:")
        bot.register_next_step_handler(call.message, send_all)

    # 📅 REPORT
    elif call.data == "admin_report":
        if not is_admin(call.from_user.id):
            return

        total = users_col.count_documents({})
        today = datetime.now().strftime("%Y-%m-%d")
        new_users = users_col.count_documents({"join_date": today})

        safe_send(
            call.message.chat.id,
            f"📅 Report\n\n👥 Total: {total}\n🆕 Today: {new_users}"
        )

    # 🔙 BACK
    elif call.data == "back":
        start(call.message)

# 📢 Broadcast
def send_all(message):
    users = users_col.find()
    for user in users:
        safe_send(user["user_id"], message.text)

    safe_send(message.chat.id, "✅ Broadcast Sent")

# ⏰ DAILY REPORT
def daily_report():
    while True:
        total = users_col.count_documents({})
        today = datetime.now().strftime("%Y-%m-%d")
        new_users = users_col.count_documents({"join_date": today})

        safe_send(
            LOGGER_ID,
            f"📅 Daily Report\n\n👥 Total: {total}\n🆕 Today: {new_users}"
        )

        time.sleep(86400)

threading.Thread(target=daily_report).start()

bot.polling()
