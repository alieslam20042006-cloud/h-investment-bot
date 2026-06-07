import telebot
import sqlite3
import threading
from telebot import types
from datetime import datetime, timedelta

# ===== إعدادات البوت =====
BOT_TOKEN = '8890618751:AAFQfzGsGZr_3UCs_Wbw9hsypeoestN_x0U'
ADMIN_ID = 5148582990

# ===== بيانات الإيداع - شام كاش فقط =====
BANK_NAME = "شام كاش"
ACCOUNT_NAME = "HHHH22"
ACCOUNT_NUMBER = "64f19e094a546aca9b6f918da631b043"

# ===== إعدادات السحب =====
MIN_WITHDRAW = 100.0

# ===== خطط الاستثمار =====
INVESTMENT_PLANS = {
    'gold': {'name': '🥇 الذهب', 'rate': 0.35, 'min': 100},
    'realestate': {'name': '🏢 العقارات', 'rate': 0.40, 'min': 150},
    'trade': {'name': '📈 التجارة', 'rate': 0.30, 'min': 100}
}

BANK_MESSAGE_INVEST = f"""
💳 للإيداع والاستثمار حول على الحساب:

🏦 **حوالة شام كاش - سوريا**
اسم الحساب: {ACCOUNT_NAME}
رقم الحساب: `{ACCOUNT_NUMBER}`

⚠️ بعد التحويل:
1. أرسل صورة الإيصال هنا
2. اكتب معها: استثمار + المبلغ
مثال: استثمار 100

التفعيل خلال ساعة عمل.
"""

print("1. جاري تشغيل البوت...")
bot = telebot.TeleBot(BOT_TOKEN)
db_lock = threading.Lock()

def init_db():
    with db_lock:
        conn = sqlite3.connect('bot_data.db')
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            balance REAL DEFAULT 0.0
        )''')
        cur.execute('''CREATE TABLE IF NOT EXISTS investments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            plan TEXT,
            amount REAL,
            start_date TEXT,
            last_profit_date TEXT
        )''')
        conn.commit()
        conn.close()

init_db()
print("2. تم الاتصال بتليجرام بنجاح")
print("3. تم تجهيز قاعدة البيانات")

def get_user(user_id):
    with db_lock:
        conn = sqlite3.connect('bot_data.db')
        cur = conn.cursor()
        cur.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
        cur.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
        user = cur.fetchone()
        conn.close()
        return user

def update_user(user_id, query, params=()):
    with db_lock:
        conn = sqlite3.connect('bot_data.db')
        cur = conn.cursor()
        cur.execute(query, params)
        conn.commit()
        conn.close()

def calculate_profits(user_id):
    with db_lock:
        conn = sqlite3