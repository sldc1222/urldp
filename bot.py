import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Replace with your bot token
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a URL, and I'll upload the file for you!")

async def handle_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    try:
        # Download the file
        response = requests.get(url)
        if response.status_code == 200:
            # Save the file temporarily
            file_name = url.split("/")[-1]
            with open(file_name, "wb") as file:
                file.write(response.content)
            # Send the file to the user
            await update.message.reply_document(document=open(file_name, "rb"))
            # Clean up
            os.remove(file_name)
        else:
            await update.message.reply_text("Failed to download the file.")
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {e}")

if __name__ == "__main__":
    # Set up the bot
    application = Application.builder().token(BOT_TOKEN).build()
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_url))
    # Start the bot
    application.run_polling()
