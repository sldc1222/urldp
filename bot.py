import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.error import Forbidden

# Replace with your bot token
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        print("Received /start command")  # Debug statement
        await update.message.reply_text("Send me a URL, and I'll upload the file for you!")
    except Forbidden:
        print("The bot was blocked by the user.")

async def handle_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    print(f"Received URL: {url}")  # Debug statement
    try:
        # Download the file
        response = requests.get(url)
        print(f"Download status code: {response.status_code}")  # Debug statement
        if response.status_code == 200:
            # Save the file temporarily
            file_name = url.split("/")[-1]
            with open(file_name, "wb") as file:
                file.write(response.content)
            print(f"File saved as: {file_name}")  # Debug statement
            # Send the file to the user
            try:
                await update.message.reply_document(document=open(file_name, "rb"))
                print("File sent successfully")  # Debug statement
            except Forbidden:
                print("The bot was blocked by the user.")
            # Clean up
            os.remove(file_name)
        else:
            await update.message.reply_text("Failed to download the file.")
    except Exception as e:
        print(f"Error: {e}")  # Debug statement
        try:
            await update.message.reply_text(f"An error occurred: {e}")
        except Forbidden:
            print("The bot was blocked by the user.")

if __name__ == "__main__":
    print("Starting the bot...")  # Debug statement
    # Set up the bot
    application = Application.builder().token(BOT_TOKEN).build()
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_url))
    # Start the bot
    application.run_polling()
