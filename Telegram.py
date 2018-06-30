"""
    README
    Dependencies
        python-telegram-bot
"""

"""
    Telegram Bot
"""
# Imports
import telegram
from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters



# Set up bot
def bot_activate():
    if False:
        bot = telegram.Bot(token='578916903:AAGoabI2IFRwP20pwm7NkgKz0XU5_3GWshg')
        updater = Updater(token='578916903:AAGoabI2IFRwP20pwm7NkgKz0XU5_3GWshg')
        dispatcher = updater.dispatcher
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
        print(bot.get_me())
    
    
    # Define bot response
    def greeting_f(bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="Hi there, I'm here for all your sauce-related needs")
    
    def unknown(bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")
        
    def message_response_f(bot,update):
        bot.send_message(chat_id=update.message.chat_id, text=update.message.text)
    
    # Define Command Keywords
    greetings_l = ['hi','hello','bonjour','yo','hey']
    
    command_handler_tuples = [
            (greetings_l,greeting_f)
            ]
    
    message_handler_tuples = [
            (Filters.command,unknown),
            (Filters.text,message_response_f)
            ]
    
    # Set up bot handler for commands
    for keywords_l,response_f in command_handler_tuples:
        for keyword in keywords_l:
            keyword_handler = CommandHandler(keyword,response_f)
            dispatcher.add_handler(keyword_handler)
    
    # Set up bot handler for messages
    for filters,response_f in message_handler_tuples:
        response_handler = MessageHandler(filters, response_f)
        dispatcher.add_handler(response_handler)
    
    
    # Start Bot
    updater.start_polling()

    # Stop Bot
    #updater.stop()
"""
    End of Telegram Bot
"""


