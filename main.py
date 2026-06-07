import os
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ===== إعداداتك =====
TOKEN = "8615885529:AAFOLVBQE3BDjKQgq_Tso9GdNx0aYDLl8yw"
SHAM_CASH_NUMBER = "64f19e094a546aca9b6f918da631b043"
SUPPORT_USERNAME = "@HHHH22121"
# ==================

app = Flask(__name__)

@app.route('/')
def home():
    return "H Investment Bot is running!"

# ===== أوامر البوت =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💰 إيداع", callback_data='deposit')],
        [InlineKeyboardButton("📊 حسابي", callback_data='account')],
        [InlineKeyboardButton("💸 سحب", callback_data='withdraw')],
        [InlineKeyboardButton("📞 الدعم", callback_data='support')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('مرحباً بك في شركة آتش (H) للإستثمارات!\n\nاختر من القائمة:', reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'deposit':
        text = f"طرق الإيداع:\n\n💳 شام كاش:\n`{SHAM_CASH_NUMBER}`\n\nانسخ الرقم وحول عليه، ثم أرسل صورة التحويل للدعم."
        await query.edit_message_text(text=text, parse_mode='Markdown')
    elif query.data == 'support':
        text = f"للتواصل مع الدعم:\n{SUPPORT_USERNAME}"
        await query.edit_message_text(text=text)
    elif query.data == 'account':
        await query.edit_message_text(text="رصيدك الحالي: 0$\nالأرباح: 0$")
    elif query.data == 'withdraw':
        await query.edit_message_text(text="الحد الأدنى للسحب 10$. رصيدك غير كافي حالياً.")

def run_bot():
    print("Starting Telegram Bot...")
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    port = int(os.environ.get('PORT', 10000))
    print(f"Starting Flask on port {port}")
    app.run(host='0.0.0.0', port=port)
