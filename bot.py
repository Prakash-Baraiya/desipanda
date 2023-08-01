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
        file.download('temp.txt')
        with open('temp.txt', 'r') as f:
            text = f.read()
    elif file_extension == '.json':
        file.download('temp.json')
        with open('temp.json', 'r') as f:
            data = json.load(f)
        text = format_json(data)
    elif file_extension == '.html':
        file.download('temp.html')
        with open('temp.html', 'r') as f:
            text = format_html(f.read())
    elif file_extension == '.pdf':
        file.download('temp.pdf')
        with open('temp.pdf', 'rb') as f:
            text = format_pdf(f)
    else:
        update.message.reply_text("Unsupported file format. Please send a .txt, .json, .html, or .pdf file.")
        return

    if text:
        formatted_text = format_text(text)
        send_formatted_text(update, context, formatted_text)
    else:
        update.message.reply_text("The file is empty. Please send a non-empty file.")

def send_formatted_text(update, context, formatted_text):
    with open('formatted_text.txt', 'w') as f:
        f.write(formatted_text)
    with open('formatted_text.txt', 'rb') as f:
        context.bot.send_document(chat_id=update.effective_chat.id, document=InputFile(f), filename='formatted_text.txt')
    os.remove('formatted_text.txt')

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

def format_pdf(pdf_file):
    pdf_reader = PdfReader(pdf_file)
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
