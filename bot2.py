from pyrogram import Client, filters
from pyrogram.types import Message, InputFile
import os
import re
import asyncio

# Replace 'YOUR_API_ID' and 'YOUR_API_HASH' with your actual values
API_ID = "11657097"
API_HASH = "7198384c0cc8cb877e4731d14e2dd7b8"
BOT_TOKEN = "6488165968:AAFyogItsIQm2VEsk_GWRsZAXf3ZNij-t6s"

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

async def read_and_decode_document(document):
    try:
        file_data = await app.download_media(document)
        return file_data if isinstance(file_data, str) else file_data.decode("utf-8")
    except Exception as e:
        print(f"Error reading and decoding document: {e}")
        return ""

def format_text(text):
    lines = text.split('\n')
    formatted_lines = []
    allowed_extensions = ['.m3u8', '.pdf', '.mpd', '.mp4', '.mkv', '.flv', '.rar', '.zip']
    for i, line in enumerate(lines):
        if re.match(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', line):
            if any(line.endswith(ext) for ext in allowed_extensions):
                name_line = lines[i-1]
                formatted_line = f'{name_line}:{line}'
                formatted_lines.append(formatted_line)
            else:
                continue
        elif i > 0 and re.match(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', lines[i-1]):
            continue
        else:
            continue
    return '\n'.join(formatted_lines)

@app.on_message(filters.command("start"))
async def start(_, message: Message):
    await message.reply_text('Welcome to your bot! Please upload a text file.')

@app.on_message(filters.document)
async def process_text_file(_, message: Message):
    document = message.document
    if document.mime_type == "text/plain":
        try:
            content = await read_and_decode_document(document)
            formatted_text = format_text(content)

            if formatted_text:
                with open('formatted_text.txt', 'w') as f:
                    f.write(formatted_text)
                with open('formatted_text.txt', 'rb') as f:
                    await app.send_document(chat_id=message.chat.id, document=InputFile(f), filename='formatted_text.txt')
                os.remove('formatted_text.txt')
            else:
                await message.reply_text("No valid links found in the document.")
        except Exception as e:
            print(f"Error reading and decoding document: {e}")
            await message.reply_text("Error reading and decoding the document.")
    else:
        await message.reply_text("Please upload a valid text file.")

if __name__ == "__main__":
    app.run()
