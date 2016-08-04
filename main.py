#Author Andrea Sessa, 2016

import os, logging
from telegram.ext import Updater, CommandHandler, Job
from twitter import *
from user import *

INTERVAL = 900 #15 mins

# Telegram TOKEN
TOKEN = "243594869:AAEDupnFR9Nj6Jq1zLf2B1C5SkgyawV-ovA"

# Twitter access data
# Consumer Key (API Key)
CONS_KEY = '9Y5DTmfoDDj9PqM9fJnNfWajW'
# Consumer Secret (API Secret)
CONS_SECRET = 'NgJipNL7M7RJ42y1w39vIVIhyP7Dw5WCXlUVpc34roxgZ8Ydu0'
# Access Token
ACCESS_TOKEN = '3078958186-bl50f5oXWKbxM1u8LCyOJ3nmjBgheYC5uhCUhOs'
# Access Token Secret
ACCESS_TOKEN_SECRET = 'vMozEQpJYhzdLejiWkZaGoElNfWbMda5qIE1nXZIrK7BR'

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Monitored users
users = [User('atm_informa'), User('TRENORD_treVA')]

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update, job_queue):
    chat_id = update.message.chat_id
    bot.sendMessage(update.message.chat_id, text='Hi! Use /add [username] to monitor a new user')
    if len(users) != 0:
        bot.sendMessage(update.message.chat_id, text='Starting monitoring for: ')
        for u in users:
            bot.sendMessage(update.message.chat_id, text=u.name)

        job = Job(getLastTweets, INTERVAL, repeat=True, context=chat_id)
        job_queue.put(job)

# Add a new twitter user to the monitored user list
def add(bot, update, args):
    chat_id = update.message.chat_id
    users.append(User(args[1]))

def help_handler(bot, update):
    chat_id = update.message.chat_id
    bot.sendMessage(chat_id, text='Use /start to start(or restart) the bot')
    bot.sendMessage(chat_id, text='Use /add [username] to start monitoring a new user')
    bot.sendMessage(chat_id, text='Use /help to get some help :)')

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def getLastTweets(bot, job):
    # Log into twitter
    t = Twitter(auth=OAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONS_KEY, CONS_SECRET))
    for u in users:
        tweets = list(reversed(t.statuses.user_timeline(screen_name=u.name)))
        for tweet in tweets:
            if not(tweet['id'] in u.last_tweets):
                bot.sendMessage(job.context, text=tweet['text'])
                u.last_tweets.append(tweet['id'])

def startTelegramBot():
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start, pass_job_queue=True))
    dp.add_handler(CommandHandler("add", add, pass_args=True))
    dp.add_handler(CommandHandler("help", help_handler))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

def main():
    startTelegramBot()

if __name__ == '__main__':
    main()
