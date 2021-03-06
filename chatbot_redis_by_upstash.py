from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# import configparser
import logging
import redis

global redis1
import os
# import configparser
  
from flask import Flask
app = Flask(__name__)

@app.route("/")
# ....
def main():
    # Load your token and create an Updater for your Bot
    
    # config = configparser.ConfigParser()
    # config.read('config.ini')
    updater = Updater(token=(os.environ['ACCESS_TOKEN']), use_context=True)
    dispatcher = updater.dispatcher

    global redis1
    redis1 = redis.Redis(host=(os.environ['HOST']), password=(os.environ['PASSWORD']), port=(os.environ['REDISPORT']))
    # ...
    # You can set this logging module, so you will know when and why things do not work as expected
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    
    # register a dispatcher to handle message: here we register an echo dispatcher
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("add", add))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("trackWeight", trackWeight))
    dispatcher.add_handler(CommandHandler("retriveWeight", retriveWeight))
    dispatcher.add_handler(CommandHandler("location", location))
    
    # To start the bot:
    updater.start_polling()
    updater.idle()


def echo(update, context):
    reply_message = update.message.text.upper()
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text= reply_message)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Helping you helping you.')


def add(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /add is issued."""
    try: 
        global redis1
        logging.info(context.args[0])
        msg = context.args[0]   # /add keyword <-- this should store the keyword
        redis1.incr(msg)
        update.message.reply_text('You have said ' + msg +  ' for ' + redis1.get(msg).decode('UTF-8') + ' times.')
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /add <keyword>')


def trackWeight(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /add is issued."""
    try: 
        global redis1
        logging.info(context.args[0])
        weight = context.args[0]
        date =context.args[1]
        redis1.hset("weightRecord1", {date: weight})
        #msg = context.args[0]   # /add keyword <-- this should store the keyword
        update.message.reply_text('Date:'+date+' ,Your weight: ' + weight )
    except (IndexError, ValueError):
        update.message.reply_text('Usage: wrong parameter')


def retriveWeight(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /add is issued."""
    try: 
        global redis1
        if(context.args[0]=="all"):
            result1=redis1.hgetall("weightRecord1")
            update.message.reply_text('Your weight: ' +str(result1))
        else:
            date =context.args[0]
            result2=redis1.hget("weightRecord1", date)
            update.message.reply_text('Your weight: ' +str(result2) )
        
        #msg = context.args[0]   # /add keyword <-- this should store the keyword
    except (IndexError, ValueError):
        update.message.reply_text('Usage: wrong parameter')

def location(update: Update, context: CallbackContext) -> None:
    # 22.5235272  114.0001652
    try: 
        context.bot.send_location(chat_id=update.effective_chat.id, latitude=context.args[0], longitude=context.args[1], proximity_alert_radius=300)
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /location <latitude> <longitude>')

if __name__ == '__main__':
    main()