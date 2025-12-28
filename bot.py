import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

ADMIN_IDS = [7611851809]  # your Telegram ID

message_map = {}

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text

    # If admin replies
    if user.id in ADMIN_IDS and update.message.reply_to_message:
        replied_msg_id = update.message.reply_to_message.message_id
        if replied_msg_id in message_map:
            await context.bot.send_message(
                chat_id=message_map[replied_msg_id],
                text=text
            )
        return

    # Normal user → send to admin
    for admin in ADMIN_IDS:
        sent = await context.bot.send_message(
            chat_id=admin,
            text=f"📩 SUPPORT\n\nName: {user.first_name}\nUser ID: {user.id}\n\n{text}"
        )
        message_map[sent.message_id] = user.id

    await update.message.reply_text("✅ Message sent to support.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()