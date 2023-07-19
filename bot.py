import os
import telebot
from bs4 import BeautifulSoup

bot = telebot.TeleBot("YOUR_BOT_TOKEN")

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Hi! I can convert HTML files to text files.")
    bot.send_message(message.chat.id, "To convert an HTML file, send me the file.")

@bot.message_handler(content_types=["document"])
def handle_document(message):
    file_name = message.document.file_name
    file_content = get_file_content(message.document.file_id)

    with open(file_name, "wb") as f:
        f.write(file_content)

    text_content = convert_html_to_text(file_name)

    bot.send_message(message.chat.id, f"Here is the converted text file: {file_name}: {text_content}")

def convert_html_to_text(file_name):
    text = ""
    with open(file_name, "r") as f:
        soup = BeautifulSoup(f, "html.parser")
        for tag in soup.find_all("a"):
            if tag.get("href") and tag.get("href").startswith("https://"):
                name = re.findall(r"(.+?)\.", tag["href"])[0]
                text += f"{name}:{tag['href']}\n"

    return text

if __name__ == "__main__":
    bot.polling()
                
