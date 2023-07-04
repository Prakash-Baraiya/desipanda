def main():
    # Replace 'YOUR_T' with your Telegram bot token
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

