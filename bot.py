import os
import telegram
from telegram.ext import Updater, CommandHandler

def convert_links_to_text(update, context):
    # Get the file ID from the message
    file_id = update.message.document.file_id

    # Get the file details using the file ID
    file_details = context.bot.get_file(file_id)

    # Download the file
    file_path = file_details.download()

    # Create a new file to store the converted links
    output_file_path = 'converted_links.txt'

    # Convert links in the file
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    converted_links = []
    for line in lines:
        line = line.strip()
        if line.startswith('http') or line.startswith('www'):
            name = line.split('/')[-1]
            converted_links.append(f'{name}:{line}')

    # Write the converted links to the output file
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write('\n'.join(converted_links))

    # Send the converted links file to the user
    context.bot.send_document(
        chat_id=update.effective_chat.id,
        document=open(output_file_path, 'rb')
    )

    # Delete the downloaded and converted files
    os.remove(file_path)
    os.remove(output_file_path)

def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Welcome! Please send me a text file to convert links to name:link format."
    )

def main():
    # Replace 'YOUR_TOKEN' with your Telegram bot token
    updater = Updater(token='6309773140:AAFaxUDW3IQ9fHa8jkUCcCT2-3oYV5wikso', use_context=True)
    dispatcher = updater.dispatcher

    # Register the command handlers
    start_handler = CommandHandler('start', start)
    convert_links_handler = CommandHandler('convertlinks', convert_links_to_text)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(convert_links_handler)

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

