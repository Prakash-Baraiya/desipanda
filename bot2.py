from pyrogram import Client, filters
from pyrogram.types import Message
import re
import asyncio

# Replace 'YOUR_API_ID' and 'YOUR_API_HASH' with your actual values
API_ID = "11657097"
API_HASH = "7198384c0cc8cb877e4731d14e2dd7b8"
BOT_TOKEN = "6488165968:AAFyogItsIQm2VEsk_GWRsZAXf3ZNij-t6s"

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(_, message: Message):
    await message.reply_text('Welcome to your bot! Please upload a text file.')

async def read_and_decode_document(document):
    try:
        file_data = await app.download_media(document)
        return file_data.decode("utf-8")
    except Exception as e:
        print(f"Error reading and decoding document: {e}")
        return ""

@app.on_message(filters.document)
async def process_text_file(_, message: Message):
    document = message.document
    if document.mime_type == "text/plain":
        content = await read_and_decode_document(document)
        if content:
            content_lines = content.split("\n")
            links = extract_urls_and_names(content_lines)
            output_text = format_output(links)
            if output_text:
                await message.reply_text(output_text)
            else:
                await message.reply_text("The processed text is empty or contains invalid characters.")
        else:
            await message.reply_text("Error reading and decoding the document.")
    else:
        await message.reply_text("Please upload a valid text file.")

def extract_urls_and_names(lines: list) -> list:
    # Use regex to find all URLs and corresponding names
    pattern = r'([^:\n]+)\s*:\s*(https?://[^\s]+)'
    matches = [re.findall(pattern, line) for line in lines]
    return [match for match_list in matches for match in match_list]

def format_output(urls_and_names: list) -> str:
    formatted_output = ""
    for name, url in urls_and_names:
        formatted_output += f"{name}\n{url}\n"
    return formatted_output.strip()  # Remove trailing whitespace and newlines

if __name__ == "__main__":
    app.run()
