import os
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

TOKEN = "8615885529:AAFOLVBQE3BDjKQgq_Tso9GdNx0aYDLl8yw"
SHAM_CASH_ACCOUNT = "64f19e094a546aca9b6f918da631b043"
SUPPORT_USERNAME = "@HHHH22121"

app = Flask(__name__)

@app.route('/')
def home():
    return "H Investment Bot is running!"

def run_flask():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💰 إيداع", callback_data='deposit')],
        [InlineKeyboardButton("💸 سحب", callback_data='withdraw')],
        [InlineKeyboardButton("📊 حسابي", callback_data='account')],
        [InlineKeyboardButton("📞 الدعم الفني", callback_data='support')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("مرحبا بك في بوت H للاستثمار 💰\n\nاختر من القائمة:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'deposit':
        keyboard = [
            [InlineKeyboardButton("شام كاش", callback_data='shamcash')],
            [InlineKeyboardButton("USDT TRC20", callback_data='usdt')],
            [InlineKeyboardButton("🔙 رجوع للقائمة", callback_data='back')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("اختر طريقة الإيداع:", reply_markup=reply_markup)
    
    elif query.data == 'shamcash':
        keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data='deposit')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            f"📱 **الإيداع عبر شام كاش**\n\n**رقم الحساب:**\n`{SHAM_CASH_ACCOUNT}`\n\n**خطوات الإيداع:**\n1. انسخ رقم الحساب وحول المبلغ\n2. صور إشعار التحويل\n3. أرسل الصورة هنا مع رقم العملية\n\n⚠️ **الحد الأدنى للإيداع: 10$**\n⏱️ التفعيل خلال 5-10 دقائق",
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    
    elif query.data == 'usdt':
        keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data='deposit')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "💵 **الإيداع USDT TRC20**\n\n**العنوان:**\n`Txxxxxxxxxxxxxxxxxxxxxxxxxx`\n\n1. حول على شبكة TRC20 فقط\n2. أرسل لقطة شاشة بعد التحويل\n3. اكتب رقم المحفظة اللي حولت منها\n\n⚠️ **الحد الأدنى: 10 USDT**",
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    
    elif query.data == 'back':
        keyboard = [
            [InlineKeyboardButton("💰 إيداع", callback_data='deposit')],
            [InlineKeyboardButton("💸 سحب", callback_data='withdraw')],
            [InlineKeyboardButton("📊 حسابي", callback_data='account')],
            [InlineKeyboardButton("📞 الدعم الفني", callback_data='support')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("مرحبا بك في بوت H للاستثمار 💰\n\nاختر من القائمة:", reply_markup=reply_markup)
    
    elif query.data == 'support':
        await query.edit_message_text(f"📞 **الدعم الفني**\n\nللاستفسار أو المساعدة تواصل مع:\n{SUPPORT_USERNAME}\n\nمتواجدين 24/7 لخدمتك", parse_mode='Markdown')
    
    elif query.data == 'account':
        await query.edit_message_text(f"📊 **معلومات حسابك**\n\nالرصيد: 0$\nالأرباح: 0$\nإجمالي الإيداع: 0$\n\nقم بالإيداع لبدء الاستثمار", parse_mode='Markdown')
    
    else:
        await query.edit_message_text("💸 قسم السحب تحت الصيانة حاليا\nراسل الدعم للمساعدة")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"✅ تم استلام إشعار الإيداع بنجاح\n\n⏱️ جاري مراجعة العملية والتفعيل خلال 5-10 دقائق\nلو تأخر راسل الدعم: {SUPPORT_USERNAME}")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("استخدم الأزرار أو اكتب /start لعرض القائمة")

def run_bot():
    try:
        print("Starting Telegram Bot...")
        application = Application.builder().token(TOKEN).build()
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CallbackQueryHandler(button_handler))
        application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
        print("Bot is now polling... Send /start")
        application.run_polling(drop_pending_updates=True)
    except Exception as e:
        print(f"BOT CRASHED! Reason: {e}")

if __name__ == '__main__':
    threading.Thread(target=run_flask).start()
    run_bot()
