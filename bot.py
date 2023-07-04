import os
import requests
from bs4 import BeautifulSoup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TOKEN = '6309773140:AAFaxUDW3IQ9fHa8jkUCcCT2-3oYV5wikso'  # Replace with your Telegram bot token
HTML_FILE_NAME = 'uploaded_file.html'
CONVERTED_FILE_NAME = 'converted_links.txt'

def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Welcome! Please send me an HTML file to convert links to name:link format."
    )

def handle_html_file(update, context):
    file_id = update.message.document.file_id
    file = context.bot.get_file(file_id)
    file.download(HTML_FILE_NAME)
    context.bot.send_message(chat_id=update.effective_chat.id, text="HTML file received. Converting links...")

    convert_html_links_to_text(HTML_FILE_NAME, CONVERTED_FILE_NAME)

    with open(CONVERTED_FILE_NAME, 'rb') as converted_file:
        context.bot.send_document(chat_id=update.effective_chat.id, document=converted_file)

    os.remove(HTML_FILE_NAME)
    os.remove(CONVERTED_FILE_NAME)

def convert_html_links_to_text(html_file_path, output_file_path):
    with open(html_file_path, 'r', encoding='utf-8') as html_file:
        html_content = html_file.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    anchor_tags = soup.find_all('a')

    converted_links = []
    for anchor in anchor_tags:
        link_name = anchor.text.strip()
        link_url = anchor['href']
        converted_links.append(f"{link_name}:{link_url}")

    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write('\n'.join(converted_links))

    print(f"Conversion complete. Output file saved as {output_file_path}")

def main():
    updater = Updater(token='YOUR_TOKEN', use_context=True, port=int(os.environ.get('PORT', 5000)))

    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    html_file_handler = MessageHandler(Filters.document.file_extension('html'), handle_html_file)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(html_file_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()


