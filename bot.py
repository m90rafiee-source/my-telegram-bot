from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)
import os

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 8106508897

user_reply_map = {}  # نگهداری وضعیت پاسخ

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("هرچی‌میخوای به صورت ناشناس به ممد بگو")

async def forward_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text

    username = f"@{user.username}" if user.username else user.full_name

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(" پاسخ", callback_data=f"user_{user.id}")]
    ])

    msg_text = f"🔔 پیام جدید از {user.full_name} ({username})\n\n📩 متن پیام:\n{text}"
    sent = await context.bot.send_message(chat_id=ADMIN_ID, text=msg_text, reply_markup=keyboard)

    user_reply_map[user.id] = sent.message_id

    user_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(" پاسخ به ممد", callback_data="reply_admin")]
    ])
    await update.message.reply_text("پیامتو بهش رسوندم", reply_markup=user_keyboard)

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data.startswith("user_"):
        target_id = int(query.data.split("_")[1])
        context.user_data["reply_to"] = target_id
        await query.message.reply_text(" پاسختو بنویس.")

    elif query.data == "reply_admin":
        context.user_data["reply_to"] = ADMIN_ID
        await query.message.reply_text("پیامتو برای ممد بنویس.")

async def handle_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text

    # اگر ادمین پاسخ می‌دهد
    if user.id == ADMIN_ID and "reply_to" in context.user_data:
        target_id = context.user_data["reply_to"]

        try:
            target_user = await context.bot.get_chat(target_id)
            target_username = f"@{target_user.username}" if target_user.username else target_user.full_name
        except:
            target_username = str(target_id)

        user_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(" پاسخ به ممد", callback_data="reply_admin")]
        ])

        await context.bot.send_message(
            chat_id=target_id,
            text=f"پاسخ ممد:\n{text}",
            reply_markup=user_keyboard
        )

        await update.message.reply_text(f"پاسخ به {target_username} ارسال شد:\n{text}")
        return

    # اگر پیام از کاربر است → ارسال به ادمین
    username = f"@{user.username}" if user.username else user.full_name

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(" پاسخ", callback_data=f"user_{user.id}")]
    ])

    msg_text = f"🔔 پیام جدید از {user.full_name} ({username})\n\n📩 متن پیام:\n{text}"
    sent = await context.bot.send_message(chat_id=ADMIN_ID, text=msg_text, reply_markup=keyboard)

    user_reply_map[user.id] = sent.message_id

    user_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(" پاسخ به ممد", callback_data="reply_admin")]
    ])

    await update.message.reply_text("پیامت به ممد ارسال شد", reply_markup=user_keyboard)

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_reply))

    # مهم: اجرای صحیح در نسخه 20.7
    app.run_polling(close_loop=False)

if __name__ == "__main__":
    main()
