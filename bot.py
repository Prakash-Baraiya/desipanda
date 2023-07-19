from telegram import Update, Bot, InputFile
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
import re
import json

TOKEN = '6309773140:AAFaxUDW3IQ9fHa8jkUCcCT2-3oYV5wikso'
bot = Bot(TOKEN)
updater = Updater(bot=bot)

def start(update: Update, context):
    update.message.reply_text('Hello! Send me a text, .txt, .html or .json file and I will extract all the links and names and format them as name:url. I will send you back the modified text as a .txt file.')

def handle_text(update: Update, context):
    text = update.message.text
    formatted_text = format_text(text)
    send_formatted_text(formatted_text, context)

def handle_document(update: Update, context):
    file = context.bot.getFile(update.message.document.file_id)
    file_name = update.message.document.file_name
    file_ext = os.path.splitext(file_name)[1]
    file.download(f'temp{file_ext}')
    with open(f'temp{file_ext}', 'r') as f:
        if file_ext == '.txt':
            text = f.read()
        elif file_ext == '.html':
            text = f.read()
        elif file_ext == '.json':
            data = json.load(f)
            text = json.dumps(data, indent=4)
    formatted_text = format_text(text)
    send_formatted_text(formatted_text, context)
    os.remove(f'temp{file_ext}')

def send_formatted_text(formatted_text, context):
    with open('formatted_text.txt', 'w') as f:
        f.write(formatted_text)
    with open('formatted_text.txt', 'rb') as f:
        context.bot.send_document(chat_id=update.effective_chat.id, document=InputFile(f), filename='formatted_text.txt')
    os.remove('formatted_text.txt')

def format_text(text):
    lines = text.split('\n')
    formatted_lines = []
    for i, line in enumerate(lines):
        if re.match(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', line):
            name_line = lines[i-1]
            formatted_line = f'{name_line}:{line}'
            formatted_lines.append(formatted_line)
        else:
            formatted_lines.append(line)
    return '\n'.join(formatted_lines)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(MessageHandler(Filters.text, handle_text))
updater.dispatcher.add_handler(MessageHandler(Filters.document.file_extension('.txt'), handle_document))
updater.dispatcher.add_handler(MessageHandler(Filters.document.file_extension('.html'), handle_document))
updater.dispatcher.add_handler(MessageHandler(Filters.document.file_extension('.json'), handle_document))

updater.start_polling()
updater.idle()
