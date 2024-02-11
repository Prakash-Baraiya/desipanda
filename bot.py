from telegram import Update, Bot, InputFile
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
from urllib.parse import urlparse
import re

TOKEN = '6488165968:AAFyogItsIQm2VEsk_GWRsZAXf3ZNij-t6s'
bot = Bot(TOKEN)
updater = Updater(bot=bot)

def start(update: Update, context):
    update.message.reply_text('Hello! Send me a text or .txt file, and I will transform the text as per your specified format. I will send you back the modified text as a .txt file.')

def handle_document(update: Update, context):
    file = context.bot.getFile(update.message.document.file_id)
    file.download('temp.txt')
    with open('temp.txt', 'r') as f:
        text = f.read()
    
    transformed_text = transform_text(text)
    
    with open('transformed_text.txt', 'w') as f:
        f.write(transformed_text)
    with open('transformed_text.txt', 'rb') as f:
        context.bot.send_document(chat_id=update.effective_chat.id, document=InputFile(f), filename='transformed_text.txt')

    os.remove('temp.txt')
    os.remove('transformed_text.txt')

def transform_text(text):
    lines = text.split('\n')
    transformed_lines = []
    current_name = ""
    
    for line in lines:
        url_parts = urlparse(line.strip())
        if url_parts.scheme and url_parts.netloc:  # Check if it's a valid URL
            url = line.strip()
            name = current_name if current_name else 'no name'
            transformed_line = f'{name} {url}'
            transformed_lines.append(transformed_line)
            current_name = ""  # Reset current_name for the next URL
        else:
            current_name = line.strip()  # Update current_name until a URL is encountered

    return '\n'.join(transformed_lines)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(MessageHandler(Filters.document, handle_document))

updater.start_polling()
updater.idle()
