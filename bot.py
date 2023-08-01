from telegram import Update, Bot, InputFile
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
import re

TOKEN = '6488165968:AAFyogItsIQm2VEsk_GWRsZAXf3ZNij-t6s'
bot = Bot(TOKEN)
updater = Updater(bot=bot)

def start(update: Update, context):
    update.message.reply_text('Hello! Send me a text or .txt file and I will extract all the links and names and format them as name:url. I will send you back the modified text as a .txt file.')

def handle_text(update: Update, context):
    text = update.message.text
    text = remove_special_characters(text)
    formatted_text = format_text(text)
    with open('formatted_text.txt', 'w') as f:
        f.write(formatted_text)
    with open('formatted_text.txt', 'rb') as f:
        context.bot.send_document(chat_id=update.effective_chat.id, document=InputFile(f), filename='formatted_text.txt')
    os.remove('formatted_text.txt')

def handle_document(update: Update, context):
    file = context.bot.getFile(update.message.document.file_id)
    file.download('temp.txt')
    with open('temp.txt', 'r') as f:
        text = f.read()
    text = remove_special_characters(text)
    formatted_text = format_text(text)
    with open('formatted_text.txt', 'w') as f:
        f.write(formatted_text)
    with open('formatted_text.txt', 'rb') as f:
        context.bot.send_document(chat_id=update.effective_chat.id, document=InputFile(f), filename='formatted_text.txt')
    os.remove('temp.txt')
    os.remove('formatted_text.txt')

def remove_special_characters(text):
    # Remove {} and CPVOD.testbook from the text
    text = re.sub(r'\{.*?\}', '', text)
    text = text.replace('CPVOD.testbook', '')
    # Remove special characters and double quotes
    text = re.sub(r'[^\w\s]', '', text)
    text = text.replace('"', '')
    return text

def format_text(text):
    lines = text.split('\n')
    formatted_lines = []
    allowed_extensions = ['.m3u8', '.pdf', '.mpd', '.mp4', '.mkv', '.flv', '.rar', '.zip']
    for i, line in enumerate(lines):
        if re.match(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', line):
            if any(line.endswith(ext) for ext in allowed_extensions):
                name_line = lines[i-1]
                formatted_line = f'{name_line}:{line}'
                formatted_lines.append(formatted_line)

    return '\n'.join(formatted_lines)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(MessageHandler(Filters.text, handle_text))
updater.dispatcher.add_handler(MessageHandler(Filters.document, handle_document))

updater.start_polling()
updater.idle()
