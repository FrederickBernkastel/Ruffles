"""
    README
    Dependencies
        python-telegram-bot
"""

"""
    Telegram Bot
        For cached messages, visit
            https://api.telegram.org/bot578916903:AAGoabI2IFRwP20pwm7NkgKz0XU5_3GWshg/getUpdates
"""
# Imports

from Entry import Entry
import telegram
from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import singlish
from Scraper import Scraper

# Constants definition
BOT_NAME = "@SaucePlzBot"
STICKER_SORRY = "CAADBAADQgADhFWxCPtLoArvRshSAg"

# Set up bot
def bot_activate():
    if True:
        bot = telegram.Bot(token='578916903:AAGoabI2IFRwP20pwm7NkgKz0XU5_3GWshg')
        updater = Updater(token='578916903:AAGoabI2IFRwP20pwm7NkgKz0XU5_3GWshg')
        dispatcher = updater.dispatcher
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
        print(bot.get_me())

    # Define bot responses
    def greeting_f(bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="Hi there %s, I'm here for all your sauce-related needs"%(update.message.from_user.first_name))
    
    def unknown(bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.",reply_to_message_id=update.message.message_id)
        bot.send_sticker(chat_id=update.message.chat_id,sticker=STICKER_SORRY)
        
    def message_response_f(bot,update):
        # Bot was directly referenced here
        if update.message.text[:len(BOT_NAME)] == BOT_NAME:
            query = update.message.text[len(BOT_NAME)+1:]
            query_l = query.split(" ")[0].lower()
            msg = update.message.text

            bot.send_message(chat_id=update.message.chat_id, text="Please hold on and let me check on that..")
            msg = msg.replace("SaucePlzBot ", "").replace("@", "")
            
            try:
                originalMessage = msg
                for item in singlish.singlish_l:
                    msg.replace(item[0], item[1])

                entry = Entry(msg)
                item = entry.start()


                scraper = Scraper(item, "")
                dictionary = scraper.scrape('p')

                textList = []
                # print(dictionary)
                for tempItem in dictionary:
                    if isinstance(tempItem, list):
                        for item2 in tempItem:
                            item2 = item2.replace("  ", "").replace("\n", " ").replace("\r", " ")
                            textList.append(item2)
                    else:
                        textList.append(tempItem)

                for tempItem in textList:
                    print(tempItem)

                # Greetings
                if query_l in greetings_l and len(query_l) < 2:
                    msg = "Hi there, I'm here for all your sauce-related needs"

                for tempItem in textList:
                    bot.send_message(chat_id=update.message.chat_id, text=tempItem)
            except ValueError:
                bot.send_message(chat_id=update.message.chat_id, text="Sorry I could not find anything that is related to : " + originalMessage)

            
    
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
bot_activate()
