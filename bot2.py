import re
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
TOKEN = '6488165968:AAFyogItsIQm2VEsk_GWRsZAXf3ZNij-t6s'

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome to your bot! Please upload a text file.')

def process_text_file(update: Update) -> None:
    text = update.message.text
    urls_and_names = extract_urls_and_names(text)
    output_text = format_output(urls_and_names)
    
    # Send the formatted output back to the user
    update.message.reply_text(output_text)

def extract_urls_and_names(text: str) -> list:
    # Use regex to find all URLs and corresponding names
    pattern = r'([^:\n]+)\s*:\s*(https?://[^\s]+)'
    matches = re.findall(pattern, text)
    return matches

def format_output(urls_and_names: list) -> str:
    formatted_output = ""
    for name, url in urls_and_names:
        formatted_output += f"{name}\n{url}\n"
    return formatted_output

def main() -> None:
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    # Add handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.TEXT & ~Filters.COMMAND, process_text_file))

    # Start the Bot
    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
