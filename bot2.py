from pyrogram import Client, filters
from pyrogram.types import Message
import re  # Add this import statement

# Replace 'YOUR_API_ID' and 'YOUR_API_HASH' with your actual values
API_ID = "11657097"
API_HASH = "7198384c0cc8cb877e4731d14e2dd7b8"
BOT_TOKEN = "6488165968:AAFyogItsIQm2VEsk_GWRsZAXf3ZNij-t6s"

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
def start(_, message: Message):
    message.reply_text('Welcome to your bot! Please upload a text file.')

@app.on_message(filters.document)
def process_text_file(_, message: Message):
    document = message.document
    if document.mime_type == "text/plain":
        text = app.get_file(document.file_id).download_as_text()
        urls_and_names = extract_urls_and_names(text)
        output_text = format_output(urls_and_names)
        message.reply_text(output_text)
    else:
        message.reply_text("Please upload a valid text file.")

def extract_urls_and_names(text: str) -> list:
    # Use regex to find all URLs and corresponding names
    pattern = r'([^:\n]+)\s*:\s*(https?://[^\s]+)'
    matches = re.findall(pattern, text)
    return matches

def format_output(urls_and_names: list) -> str:
    formatted_output = ""
    for name, url in urls_and_names:
        formatted_output += f"{name}\n{url}\n"
    return formatted_output

if __name__ == "__main__":
    app.run()
    
