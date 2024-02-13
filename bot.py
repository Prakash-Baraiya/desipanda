import os
import json
from bs4 import BeautifulSoup
from telegram import Update, InputFile
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot_token = '6488165968:AAFyogItsIQm2VEsk_GWRsZAXf3ZNij-t6s'

def convert_json_to_txt(json_data):
    txt_content = ""
    for language, revisions in json_data.items():
        for revision, url in revisions.items():
            txt_content += f"{revision}:{url}\n"
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

def handle_document(update: Update, context):
    # Ensure the 'downloads' directory exists
    download_dir = './downloads'
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    # Save the uploaded document
    file_path = f"{download_dir}/{update.message.chat_id}_uploaded"
    update.message.document.get_file().download(file_path)

    # Load content from the uploaded file based on the content type
    with open(file_path, 'rb') as file:
        content_type = update.message.document.mime_type

        if content_type == 'application/json':
            # Handle JSON
            data = json.load(file)
            txt_content = convert_json_to_txt(data)
        elif content_type == 'text/html':
            # Handle HTML
            html_content = file.read().decode('utf-8')
            txt_content = convert_html_to_txt(html_content)
        else:
            # Unsupported file format
            context.bot.send_message(chat_id=update.message.chat_id, text="Unsupported file format.")
            return

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

# Register the document handler
dispatcher.add_handler(MessageHandler(Filters.document, handle_document))

# Start the bot
updater.start_polling()
updater.idle()
