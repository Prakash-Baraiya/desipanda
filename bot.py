from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import json

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hi! Please send me an HTML, TXT or JSON file from your storage.', reply_markup=ForceReply(selective=True))

def handle_file(update: Update, context: CallbackContext) -> None:
    file = update.message.document.get_file()
    file_name = update.message.document.file_name
    file_ext = file_name.split('.')[-1]
    if file_ext not in ['html', 'txt', 'json']:
        update.message.reply_text('Invalid file type. Please send an HTML, TXT or JSON file.')
        return
    file_content = file.download_as_bytearray().decode('utf-8')
    if file_ext == 'html':
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(file_content, 'html.parser')
        links = soup.find_all('a')
        result = '\n'.join([f'{link.text}:{link.get("href")}' for link in links])
    elif file_ext == 'txt':
        result = file_content
    elif file_ext == 'json':
        data = json.loads(file_content)
        result = '\n'.join([f'{k}:{v}' for k,v in data.items()])
    update.message.reply_text(result)

def main() -> None:
    updater = Updater("6309773140:AAFaxUDW3IQ9fHa8jkUCcCT2-3oYV5wikso")
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.document, handle_file))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
