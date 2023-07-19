from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from bs4 import BeautifulSoup

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hi! Please send me an HTML file or .html file from your storage.', reply_markup=ForceReply(selective=True))

def convert_html_to_txt(update: Update, context: CallbackContext) -> None:
    file = context.bot.getFile(update.message.document.file_id)
    file.download('temp.html')
    with open('temp.html', 'r') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
        text = soup.get_text()
        with open('temp.txt', 'w') as f:
            f.write(text)
    with open('temp.txt', 'rb') as f:
        update.message.reply_document(f)

def process_txt_file(update: Update, context: CallbackContext) -> None:
    file = context.bot.getFile(update.message.document.file_id)
    file.download('temp.txt')
    with open('temp.txt', 'r') as f:
        lines = f.readlines()
        result = []
        for line in lines:
            parts = line.split()
            if len(parts) >= 2:
                name = parts[0]
                url = parts[-1]
                result.append(f'{name}: {url}')
        with open('result.txt', 'w') as f:
            f.write('\n'.join(result))
    with open('result.txt', 'rb') as f:
        update.message.reply_document(f)

def main() -> None:
    updater = Updater("6309773140:AAFaxUDW3IQ9fHa8jkUCcCT2-3oYV5wikso")
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.document.file_extension("html"), convert_html_to_txt))
    dispatcher.add_handler(MessageHandler(Filters.document.file_extension("txt"), process_txt_file))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
