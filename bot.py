from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hi! Send me a text or .txt file and I will replace "https" with ":https" and combine it with the name available before or above it without any space.')

def handle_document(update: Update, context: CallbackContext) -> None:
    file = context.bot.getFile(update.message.document.file_id)
    file.download('temp.txt')
    with open('temp.txt', 'r') as f:
        lines = f.readlines()
    new_lines = []
    for line in lines:
        if line.startswith('http'):
            new_lines[-1] = new_lines[-1].strip() + line.replace('https', ':https')
        else:
            new_lines.append(line)
    with open('temp.txt', 'w') as f:
        f.writelines(new_lines)
    update.message.reply_document(open('temp.txt', 'rb'))

def handle_text(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Please send me a text or .txt file.")

def main():
    updater = Updater("6309773140:AAFaxUDW3IQ9fHa8jkUCcCT2-3oYV5wikso")
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.document, handle_document))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
