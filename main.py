import os
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# ===== التوكن الجديد حقك هنا =====
TOKEN = "8890618751:AAFQfzGsGZr_3UCs_Wbw9hsypeoestN_x0U"
# =============================

# ===== بياناتك =====
SHAM_CASH_ACCOUNT = "64f19e094a546aca9b6f918da631b043"
SUPPORT_USERNAME = "@HHHH22121"
# ==================

# سيرفر وهمي عشان Render المجاني
app = Flask(__name__)

@app.route('/')
def home():
    return "H Investment Bot is running!"

def run_flask():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

# ===== أوامر البوت =====

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💰 إيداع", callback_data='deposit')],
        [InlineKeyboardButton("💸 سحب", callback_data='withdraw')],
        [InlineKeyboardButton("📊 حسابي", callback_data='account')],
        [InlineKeyboardButton("📞 الدعم الفني", callback_data='support')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "مرحبا بك في بوت H للاستثمار 💰\n\nاختر من القائمة:",
        reply_markup=reply_markup
    )

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
        await query.edit_message_text(
            "اختر طريقة الإيداع:",
            reply_markup=reply_markup
        )
    
    elif query.data == 'shamcash':
        keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data='deposit')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            f"📱 **الإيداع عبر شام كاش**\n\n"
            f"**رقم الحساب:**\n`{SHAM_CASH_ACCOUNT}`\n\n"
            f"**خطوات الإيداع:**\n"
            f"1. انسخ رقم الحساب وحول المبلغ\n"
            f"2. صور إشعار التحويل\n"
            f"3. أرسل الصورة هنا مع رقم العملية\n\n"
            f"⚠️ **الحد الأدنى للإيداع: 10$**\n"
            f"⏱️ التفعيل خلال 5-10 دقائق",
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    
    elif query.data == 'usdt':
        keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data='deposit')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "💵 **الإيداع USDT TRC20**\n\n"
            "**العنوان:**\n`Txxxxxxxxxxxxxxxxxxxxxxxxxx`\n\n"
            "1. حول على شبكة TRC20 فقط\n"
            "2. أرسل لقطة شاشة بعد التحويل\n"
            "3. اكتب رقم المحفظة اللي حولت منها\n\n"
            "⚠️ **الحد الأدنى: 10 USDT**",
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
        await query.edit_message_text(
            "مرحبا بك في بوت H للاستثمار 💰\n\nاختر من القائمة:",
            reply_markup=reply_markup
        )
    
    elif query.data == 'withdraw':
        await query.edit_message_text("💸 قسم السحب تحت الصيانة حاليا\nراسل الدعم للمساعدة")
    
    elif query.data == 'account':
        await query.edit_message_text(
            f"📊 **معلومات حسابك**\n\n"
            f"الرصيد: 0$\n"
            f"الأرباح: 0$\n"
            f"إجمالي الإيداع: 0$\n\n"
            f"قم بالإيداع لبدء الاستثمار",
            parse_mode='Markdown'
        )
    
    elif query.data == 'support':
        await query.edit_message_text(
            f"📞 **الدعم الفني**\n\n"
            f"للاستفسار أو المساعدة تواصل مع:\n{SUPPORT_USERNAME}\n\n"
            f"متواجدين 24/7 لخدمتك",
            parse_mode='Markdown'
        )

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ تم استلام إشعار الإيداع بنجاح\n\n"
        "⏱️ جاري مراجعة العملية والتفعيل خلال 5-10 دقائق\n"
        f"لو تأخر راسل الدعم: {SUPPORT_USERNAME}"
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("استخدم الأزرار أو اكتب /start لعرض القائمة")

def run_bot():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    application.run_polling()

if __name__ == '__main__':
    threading.Thread(target=run_flask).start()
    run_bot()
