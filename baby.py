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
        {"$setOnInsert": {
            "user_id": user.id,
            "username": user.username,
            "join_date": datetime.now().strftime("%Y-%m-%d")
        }},
        upsert=True
    )

# 🔑 Admin Check
def is_admin(user_id):
    return user_id in ADMIN_IDS

# 🔥 SAFE SEND
def safe_send(chat_id, text, **kwargs):
    try:
        bot.send_message(chat_id, text, **kwargs)
    except Exception as e:
        if "blocked by the user" in str(e):
            try:
                bot.send_message(LOGGER_ID, f"🚫 User Blocked Bot\n🆔 {chat_id}")
            except:
                pass
            users_col.delete_one({"user_id": chat_id})

# 📢 LOGGER
def log_user(user):
    safe_send(
        LOGGER_ID,
        f"""🚀 New User Started

👤 {user.first_name}
🆔 {user.id}
📛 @{user.username if user.username else 'No username'}"""
    )

# 🛡️ Anti Spam
user_last = {}
def is_spam(uid):
    now = time.time()
    if uid in user_last and now - user_last[uid] < 2:
        return True
    user_last[uid] = now
    return False

# ⚡ ANIMATION
def animate(chat_id, msg_id):
    steps = ["⏳ Loading.", "⏳ Loading..", "⏳ Loading..."]
    for s in steps:
        try:
            bot.edit_message_text(s, chat_id, msg_id)
            time.sleep(0.25)
        except:
            pass

# 🎯 MAIN MENU
def main_menu(call):
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
        markup.add(InlineKeyboardButton("👑 Admin Panel", callback_data="admin"))

    bot.edit_message_text(
        """🔥 *Interfaith Media Store*

💎 Premium & Trusted Service  
⚡ Instant Access | Fast Delivery  

━━━━━━━━━━━━━━━  
👇 *Select an option below*""",
        call.message.chat.id,
        call.message.message_id,
        parse_mode="Markdown",
        reply_markup=markup
    )

# 🚀 START
@bot.message_handler(commands=['start'])
def start(message):
    add_user(message.from_user)
    threading.Thread(target=log_user, args=(message.from_user,)).start()

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
        markup.add(InlineKeyboardButton("👑 Admin Panel", callback_data="admin"))

    safe_send(
        message.chat.id,
        """🔥 *Interfaith Media Store*

💎 Premium & Trusted Service  
⚡ Instant Access | Fast Delivery  

━━━━━━━━━━━━━━━  
👇 *Select an option below*""",
        parse_mode="Markdown",
        reply_markup=markup
    )

# 🔘 CALLBACK
@bot.callback_query_handler(func=lambda call: True)
def callback(call):

    bot.answer_callback_query(call.id)

    if is_spam(call.from_user.id):
        return

    # 🛒 SELLER
    if call.data == "seller":
        animate(call.message.chat.id, call.message.message_id)

        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📩 Contact Seller", url="https://t.me/Anyamembership"))
        markup.add(InlineKeyboardButton("🔙 Back", callback_data="back"))

        bot.edit_message_text(
            """🛒 *Trusted Seller*

Buy directly from a real & verified seller.""",
            call.message.chat.id,
            call.message.message_id,
            parse_mode="Markdown",
            reply_markup=markup
        )

    # 🤖 MEDIA
    elif call.data == "media":
        animate(call.message.chat.id, call.message.message_id)

        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🤖 Open Bot", url="https://t.me/PayalMembershipBot"))
        markup.add(InlineKeyboardButton("🔙 Back", callback_data="back"))

        bot.edit_message_text(
            """🤖 *Automated Media Bot*

👉 @PayalMembershipBot""",
            call.message.chat.id,
            call.message.message_id,
            parse_mode="Markdown",
            reply_markup=markup
        )

    # 📦 PLANS
    elif call.data == "plans":
        animate(call.message.chat.id, call.message.message_id)

        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📦 View Plans", url="https://t.me/PayalMembershipBot?start=start"))
        markup.add(InlineKeyboardButton("🔙 Back", callback_data="back"))

        bot.edit_message_text(
            """📦 *Plans & Purchase*

Visit our official bot to check all plans.""",
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

    # 👑 ADMIN
    elif call.data == "admin":
        if not is_admin(call.from_user.id):
            return

        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("📊 Stats", callback_data="stats"),
            InlineKeyboardButton("📢 Broadcast", callback_data="broadcast")
        )
        markup.add(InlineKeyboardButton("🔙 Back", callback_data="back"))

        bot.edit_message_text(
            "👑 Admin Panel",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    # 📊 STATS
    elif call.data == "stats":
        total = users_col.count_documents({})
        safe_send(call.message.chat.id, f"📊 Users: {total}")

    # 📢 BROADCAST
    elif call.data == "broadcast":
        safe_send(call.message.chat.id, "Send message:")
        bot.register_next_step_handler(call.message, send_all)

    # 🔙 BACK
    elif call.data == "back":
        main_menu(call)

# 📢 BROADCAST
def send_all(message):
    for user in users_col.find():
        safe_send(user["user_id"], message.text)
    safe_send(message.chat.id, "✅ Done")

bot.polling()
