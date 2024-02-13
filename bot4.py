import os
from bs4 import BeautifulSoup
from telegram import Update, InputFile
from telegram.ext import Updater, MessageHandler, Filters

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot_token = '6488165968:AAFyogItsIQm2VEsk_GWRsZAXf3ZNij-t6s'

def convert_html_to_txt(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    txt_content = ""

    for row in soup.find_all('tr'):
        title = row.find('td').text.strip()
        link = row.find('a')['href']
        txt_content += f"{title}:{link}\n"

    return txt_content

def handle_document(update: Update, context):
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

# Set up the Telegram updater
updater = Updater(token=bot_token, use_context=True)
dispatcher = updater.dispatcher

# Register the document handler
dispatcher.add_handler(MessageHandler(Filters.document, handle_document))

# Start the bot
updater.start_polling()
updater.idle()
