import os
import json
from bs4 import BeautifulSoup
from telegram import Update, InputFile
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot_token = '6488165968:AAFyogItsIQm2VEsk_GWRsZAXf3ZNij-t6s'

def flatten_json(data, parent_key='', sep=':'):
    txt_content = ""
    for key, value in data.items():
        new_key = f"{parent_key}{sep}{key}" if parent_key else key
        if isinstance(value, dict):
            txt_content += flatten_json(value, new_key, sep=sep)
        else:
            txt_content += f"{new_key}:{value}\n"
    return txt_content

def convert_json_to_txt(json_data):
    txt_content = flatten_json(json_data)
    return txt_content

def convert_html_to_txt(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    txt_content = ""

    for row in soup.find_all('tr'):
        title = row.find('td').text.strip()
        link = row.find('a')['href']
        txt_content += f"{title}:{link}\n"

    return txt_content

def start(update: Update, context):
    update.message.reply_text("WELCOME PRAKASH BARAIYA")

def handle_html(update: Update, context):
    # Ensure the 'downloads' directory exists
    download_dir = './downloads'
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    # Save the uploaded HTML document
    html_path = f"{download_dir}/{update.message.chat_id}_uploaded.html"
    update.message.document.get_file().download(html_path)

    # Load HTML from the uploaded file
    with open(html_path, 'r', encoding='utf-8') as html_file:
        html_content = html_file.read()

    # Convert HTML to text
    txt_content = convert_html_to_txt(html_content)

    # Save the text content to a file with UTF-8 encoding
    txt_path = f"{download_dir}/{update.message.chat_id}_final.txt"
    with open(txt_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(txt_content)

    # Send the text file to Telegram chat
    with open(txt_path, 'rb') as txt_file:
        context.bot.send_document(chat_id=update.message.chat_id, document=InputFile(txt_file))

def handle_json(update: Update, context):
    # Ensure the 'downloads' directory exists
    download_dir = './downloads'
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    # Save the uploaded JSON document
    json_path = f"{download_dir}/{update.message.chat_id}_uploaded.json"
    update.message.document.get_file().download(json_path)

    # Load JSON from the uploaded file
    with open(json_path) as json_file:
        data = json.load(json_file)

    # Convert JSON to text
    txt_content = convert_json_to_txt(data)

    # Save the text content to a file with UTF-8 encoding
    txt_path = f"{download_dir}/{update.message.chat_id}_final.txt"
    with open(txt_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(txt_content)

    # Send the text file to Telegram chat
    with open(txt_path, 'rb') as txt_file:
        context.bot.send_document(chat_id=update.message.chat_id, document=InputFile(txt_file))

# Set up the Telegram updater
updater = Updater(token=bot_token, use_context=True)
dispatcher = updater.dispatcher

# Register the start command handler
dispatcher.add_handler(CommandHandler("start", start))

# Register the handlers for specific file types
dispatcher.add_handler(MessageHandler(Filters.document.file_extension("html"), handle_html))
dispatcher.add_handler(MessageHandler(Filters.document.file_extension("json"), handle_json))

# Start the bot
updater.start_polling()
updater.idle()
