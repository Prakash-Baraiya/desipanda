from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
import re

TOKEN = '6309773140:AAFaxUDW3IQ9fHa8jkUCcCT2-3oYV5wikso'
bot = Bot(TOKEN)
updater = Updater(bot=bot)

def start(update: Update, context):
    update.message.reply_text('Hello! Send me a text or .txt file and I will extract all the links and names and format them as name:url.')

def handle_text(update: Update, context):
    text = update.message.text
    formatted_text = format_text(text)
    update.message.reply_text(formatted_text)

def handle_document(update: Update, context):
    file = context.bot.getFile(update.message.document.file_id)
    file.download('temp.txt')
    with open('temp.txt', 'r') as f:
        text = f.read()
    formatted_text = format_text(text)
    update.message.reply_text(formatted_text)
    os.remove('temp.txt')

def format_text(text):
    lines = text.split('\n')
    formatted_lines = []
    for line in lines:
        parts = line.split()
        name = ''
        url = ''
        for i, part in enumerate(parts):
            if re.match(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', part):
                url = part
                for j in range(i-1, max(i-4, -1), -1):
                    if not parts[j].startswith('http'):
                        name = parts[j] + ' ' + name
                    else:
                        break
                break
        name = name.strip()
        if name and url:
            formatted_line = f'{name}:{url}'
            formatted_lines.append(formatted_line)
        else:
            formatted_lines.append(line)
    return '\n'.join(formatted_lines)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(MessageHandler(Filters.text, handle_text))
updater.dispatcher.add_handler(MessageHandler(Filters.document, handle_document))

updater.start_polling()
updater.idle()
