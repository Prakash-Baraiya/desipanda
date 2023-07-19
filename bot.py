from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hi! Please send me a TXT file from your storage.', reply_markup=ForceReply(selective=True))

def handle_file(update: Update, context: CallbackContext) -> None:
    file = update.message.document.get_file()
    file_name = update.message.document.file_name
    file_ext = file_name.split('.')[-1]
    if file_ext != 'txt':
        update.message.reply_text('Invalid file type. Please send a TXT file.')
        return
    file_content = file.download_as_bytearray().decode('utf-8')
    lines = file_content.split('\n')
    result = []
    for line in lines:
        parts = line.split()
        if len(parts) == 2:
            name, url = parts
            result.append(f'{name}:{url}')
    update.message.reply_text('\n'.join(result))

def main() -> None:
    updater = Updater("6309773140:AAFaxUDW3IQ9fHa8jkUCcCT2-3oYV5wikso")
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.document, handle_file))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
