from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

# توکن مستقیم (برای تست سریع)
TOKEN = "8497708935:AAFOVmONJ1AHxGcno95A2KiP6C7EXS4jCqg"
ADMIN_ID = 8106508897

user_reply_map = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("هرچی‌میخوای به صورت ناشناس به ممد بگو")

async def handle_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text

    if user.id == ADMIN_ID and "reply_to" in context.user_data:
        target_id = context.user_data["reply_to"]
        try:
            target_user = await context.bot.get_chat(target_id)
            target_username = f"@{target_user.username}" if target_user.username else target_user.full_name
        except:
            target_username = str(target_id)

        await context.bot.send_message(chat_id=target_id, text=f"پاسخ ممد:\n{text}")
        await update.message.reply_text(f"پاسخ به {target_username} ارسال شد:\n{text}")
        return

    username = f"@{user.username}" if user.username else user.full_name
    msg_text = f"🔔 پیام جدید از {user.full_name} ({username})\n\n📩 متن پیام:\n{text}"
    await context.bot.send_message(chat_id=ADMIN_ID, text=msg_text)

    await update.message.reply_text("پیامت به ممد ارسال شد")

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data.startswith("user_"):
        target_id = int(query.data.split("_")[1])
        context.user_data["reply_to"] = target_id
        await query.message.reply_text("پاسختو بنویس.")
    elif query.data == "reply_admin":
        context.user_data["reply_to"] = ADMIN_ID
        await query.message.reply_text("پیامتو برای ممد بنویس.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_reply))
    app.add_handler(CallbackQueryHandler(handle_button))

    app.run_polling()

if __name__ == "__main__":
    main()
