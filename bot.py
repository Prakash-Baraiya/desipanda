from telegram import Update, Bot, InputFile
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
import re
import json
from bs4 import BeautifulSoup
from io import BytesIO
from PyPDF2 import PdfReader

TOKEN = '6488165968:AAFyogItsIQm2VEsk_GWRsZAXf3ZNij-t6s'
bot = Bot(TOKEN)
updater = Updater(bot=bot)

def start(update: Update, context):
    update.message.reply_text('Hello! Send me a text or .txt, .json, .html, or .pdf file and I will extract all the links and names and format them as name:url. I will send you back the modified text as a .txt file.')

def handle_text(update: Update, context):
    text = update.message.text
    formatted_text = format_text(text)
    send_formatted_text(update, context, formatted_text)

def handle_document(update: Update, context):
    file = context.bot.getFile(update.message.document.file_id)
    file_extension = os.path.splitext(file.file_path)[1].lower()

    if file_extension == '.txt':
        text = read_file_as_text(file)
    elif file_extension == '.json':
        text = read_file_as_text(file, encoding='utf-8')
        if text:
            try:
                data = json.loads(text)
                text = format_json(data)
            except json.JSONDecodeError:
                text = None
    elif file_extension == '.html':
        text = read_file_as_text(file, encoding='utf-8')
        if text:
            text = format_html(text)
    elif file_extension == '.pdf':
        text = read_pdf_as_text(file)
    else:
        update.message.reply_text("Unsupported file format. Please send a .txt, .json, .html, or .pdf file.")
        return

    if text:
        formatted_text = format_text(text)
        send_formatted_text(update, context, formatted_text)
    else:
        update.message.reply_text("The file is empty or cannot be read. Please send a valid non-empty file.")

def send_formatted_text(update, context, formatted_text):
    with open('formatted_text.txt', 'w', encoding='utf-8') as f:
        f.write(formatted_text)
    with open('formatted_text.txt', 'rb') as f:
        context.bot.send_document(chat_id=update.effective_chat.id, document=InputFile(f), filename='formatted_text.txt')
    os.remove('formatted_text.txt')

def read_file_as_text(file, encoding='utf-8'):
    with BytesIO() as temp_buffer:
        file.download(out=temp_buffer)
        temp_buffer.seek(0)
        return temp_buffer.read().decode(encoding)

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
            else:
                continue
        elif i > 0 and re.match(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', lines[i-1]):
            continue
        else:
            continue
    return '\n'.join(formatted_lines)

def format_json(data):
    formatted_text = ''
    for item in data:
        if isinstance(item, dict):
            name = item.get('name', '')
            url = item.get('url', '')
            formatted_line = f'{name}:{url}'
            formatted_text += formatted_line + '\n'
    return formatted_text

def format_html(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    links = soup.find_all('a')
    formatted_text = ''
    for link in links:
        name = link.text.strip()
        url = link['href'].strip()
        formatted_line = f'{name}:{url}'
        formatted_text += formatted_line + '\n'
    return formatted_text

def read_pdf_as_text(file):
    with BytesIO() as temp_buffer:
        file.download(out=temp_buffer)
        temp_buffer.seek(0)
        pdf_reader = PdfReader(temp_buffer)
        formatted_text = ''
        for page in pdf_reader.pages:
            text = page.extract_text()
            formatted_text += text + '\n'
        return formatted_text

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(MessageHandler(Filters.text, handle_text))
updater.dispatcher.add_handler(MessageHandler(Filters.document, handle_document))

updater.start_polling()
updater.idle()
