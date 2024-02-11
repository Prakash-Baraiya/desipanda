from pyrogram import Client, filters
from pyrogram.types import Message
import re

# Replace 'YOUR_API_ID' and 'YOUR_API_HASH' with your actual values
API_ID = "11657097"
API_HASH = "7198384c0cc8cb877e4731d14e2dd7b8"
BOT_TOKEN = "6488165968:AAFyogItsIQm2VEsk_GWRsZAXf3ZNij-t6s"

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(_, message: Message):
    await message.reply_text('Welcome to your bot! Please upload a text file.')

def process_content(content):
    links = []
    current_name = ""

    for line in content.split("\n"):
        if ":https" in line:
            parts = line.split(":https", 1)
            if len(parts) == 2:
                name, url = map(str.strip, parts)
                name = name.rstrip(':')  # Remove trailing ":" in name
                url_matches = re.findall(r'\bhttps?://\S+', url)
                
                if url_matches:
                    url = url_matches[0]
                    url = url.replace("https://", "")
                    url = re.sub(r'https://', 'https://', url)
                    url = url.replace("httpwww.", "www.")
                    url = re.sub(r'https?://', 'https://', url, count=1)
                    url = re.sub(r'/view\?usp=drivesdk$', '', url)

                    links.append((current_name.rstrip(':'), url))
                    current_name = ""  # Reset current_name for the next URL
                else:
                    current_name += line.strip()

    return links

@app.on_message(filters.document)
async def process_text_file(_, message: Message):
    document = message.document
    if document.mime_type == "text/plain":
        try:
            file_data = await app.download_media(document)
            content = file_data.decode("utf-8")
            links = process_content(content)

            if links:
                output_text = format_output(links)
                await message.reply_text(output_text)
            else:
                await message.reply_text("No valid links found in the document.")
        except Exception as e:
            print(f"Error reading and decoding document: {e}")
            await message.reply_text("Error reading and decoding the document.")
    else:
        await message.reply_text("Please upload a valid text file.")

def format_output(links: list) -> str:
    formatted_output = ""
    for name, url in links:
        formatted_output += f"{name}\n{url}\n"
    return formatted_output.strip()  # Remove trailing whitespace and newlines

if __name__ == "__main__":
    app.run()
