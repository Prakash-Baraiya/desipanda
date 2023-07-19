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
    file.download('temp')
    with open('temp', 'r') as f:
        text = f.read()
    if update.message.document.mime_type == 'text/html':
        formatted_text = format_html(text)
    elif update.message.document.mime_type == 'application/json':
        formatted_text = format_json(text)
    else:
        formatted_text = format_text(text)
    send_formatted_text(formatted_text, context)
    os.remove('temp')

def send_formatted_text(formatted_text, context):
    with open('formatted_text.txt', 'w') as f:
        f.write(formatted_text)
    with open('formatted_text.txt', 'rb') as f:
        context.bot.send_document(chat_id=update.effective_chat.id, document=InputFile(f), filename='formatted_text.txt')
    os.remove('formatted_text.txt')

def format_html(text):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(text, 'html.parser')
    links = soup.find_all('a')
    formatted_lines = []
    for link in links:
        name = link.text
        url = link.get('href')
        if url and re.match(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', url):
            formatted_line = f'{name}:{url}'
            formatted_lines.append(formatted_line)
    return '\n'.join(formatted_lines)

def format_json(text):
    data = json.loads(text)
    formatted_lines = []
    for key, value in data.items():
        if isinstance(value, str) and re.match(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', value):
            formatted_line = f'{key}:{value}'
            formatted_lines.append(formatted_line)
    return '\n'.join(formatted_lines)

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
updater.dispatcher.add_handler(MessageHandler(Filters.document, handle_document))

updater.start_polling()
updater.idle()
