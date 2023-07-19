from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from bs4 import BeautifulSoup

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hi! Please send me an HTML or .html file from your storage.', reply_markup=ForceReply(selective=True))

def convert_html_to_txt(update: Update, context: CallbackContext) -> None:
    file = context.bot.getFile(update.message.document.file_id)
    file.download('temp.html')
    with open('temp.html', 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
        text = soup.get_text()
        links = soup.find_all('a')
        with open('output.txt', 'w', encoding='utf-8') as f:
            f.write(text)
            f.write('\n\nLinks:\n')
            for link in links:
                name = link.text
                url = link.get('href')
                f.write(f'{name}: {url}\n')
    with open('output.txt', 'rb') as f:
        update.message.reply_document(f)

def combine_txt(update: Update, context: CallbackContext) -> None:
    file = context.bot.getFile(update.message.document.file_id)
    file.download('temp.txt')
    with open('temp.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        with open('output.txt', 'w', encoding='utf-8') as f:
            for line in lines:
                parts = line.split(':')
                if len(parts) == 2:
                    name = parts[0].strip()
                    url = parts[1].strip()
                    f.write(f'{name}:{url}\n')
    with open('output.txt', 'rb') as f:
        update.message.reply_document(f)

def main() -> None:
    updater = Updater("6309773140:AAFaxUDW3IQ9fHa8jkUCcCT2-3oYV5wikso")
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.document.file_extension("html"), convert_html_to_txt))
    dispatcher.add_handler(MessageHandler(Filters.document.file_extension("txt"), combine_txt))
    updater.start_polling()
    updater.idle()

if name == 'main':
    main()
