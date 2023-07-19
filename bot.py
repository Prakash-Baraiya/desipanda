from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from bs4 import BeautifulSoup
import json

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hi! Please send me an HTML, TXT or JSON file from your storage.', reply_markup=ForceReply(selective=True))

def handle_document(update: Update, context: CallbackContext) -> None:
    file = context.bot.getFile(update.message.document.file_id)
    file_name = update.message.document.file_name
    file_extension = file_name.split('.')[-1]
    if file_extension not in ['html', 'txt', 'json']:
        update.message.reply_text('Invalid file type. Please send an HTML, TXT or JSON file.')
        return
    file_content = file.download_as_bytearray().decode('utf-8')
    output = ''
    if file_extension == 'html':
        soup = BeautifulSoup(file_content, 'html.parser')
        for link in soup.find_all('a'):
            name = link.text.strip()
            url = link.get('href')
            if name and url:
                output += f'{name}: {url}\n'
    elif file_extension == 'txt':
        lines = file_content.split('\n')
        for line in lines:
            parts = line.split(':')
            if len(parts) == 2:
                name, url = parts
                output += f'{name.strip()}: {url.strip()}\n'
    elif file_extension == 'json':
        data = json.loads(file_content)
        for item in data:
            if 'name' in item and 'url' in item:
                output += f"{item['name']}: {item['url']}\n"
    if output:
        context.bot.send_document(chat_id=update.message.chat_id, filename='output.txt', document=output.encode('utf-8'), caption='Here is the converted TXT file.')
    else:
        update.message.reply_text('No valid name and URL pairs found in the file.')

def main() -> None:
    updater = Updater("6309773140:AAFaxUDW3IQ9fHa8jkUCcCT2-3oYV5wikso")
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.document, handle_document))
    updater.start_polling()
    updater.idle()

if name == 'main':
    main()
