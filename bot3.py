import json
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot_token = '6488165968:AAFyogItsIQm2VEsk_GWRsZAXf3ZNij-t6s'

def convert_json_to_txt(json_data):
    txt_content = ""
    for language, revisions in json_data.items():
        for revision, url in revisions.items():
            txt_content += f"{revision}:{url}\n"
    return txt_content

def handle_document(update: Update, context):
    # Assuming you have a downloads directory
    json_path = f"./downloads/{update.message.chat_id}_uploaded.json"

    # Save the uploaded JSON document
    update.message.document.get_file().download(json_path)

    # Load JSON from the uploaded file
    with open(json_path) as json_file:
        data = json.load(json_file)

    # Convert JSON to text
    txt_content = convert_json_to_txt(data)

    # Save the text content to a file
    txt_path = f"./downloads/{update.message.chat_id}_final.txt"
    with open(txt_path, 'w') as txt_file:
        txt_file.write(txt_content)

    # Send the text file to Telegram chat
    document = Document(txt_path)
    document.send(bot_token, update.message.chat_id)

# Set up the Telegram updater
updater = Updater(token=bot_token, use_context=True)
dispatcher = updater.dispatcher

# Register the document handler
dispatcher.add_handler(MessageHandler(Filters.document, handle_document))

# Start the bot
updater.start_polling()
updater.idle()
