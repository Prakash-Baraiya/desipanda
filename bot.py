import telebot
import requests

bot = telebot.TeleBot('6309773140:AAFaxUDW3IQ9fHa8jkUCcCT2-3oYV5wikso')

@bot.message_handler(content_types=['document'])
def handle_document(message):
    file_id = message.document.file_id
    file = bot.get_file(file_id)
    file_path = file.file_path
    with open(file_path, 'rb') as f:
        html_content = f.read().decode('utf-8')

    txt_content = []
    for link in re.findall(r'<a href="(.*?)">(.*?)</a>', html_content):
        txt_content.append(f'{link[1]}:{link[0]}')

    with open('links.txt', 'w') as f:
        f.write('\n'.join(txt_content))

    bot.send_message(message.chat.id, 'Your links have been converted to a TXT file.')

bot.polling()

