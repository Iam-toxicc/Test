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
        InlineKeyboardButton("
