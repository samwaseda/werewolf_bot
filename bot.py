import logging
from telegram import ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)
from datetime import datetime
import re
import pandas as pd
import difflib
import warnings
import numpy as np
from difflib import SequenceMatcher


with open('TOKEN', 'r') as f:
    TOKEN = f.readline().replace('\n', '')

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


class Master:
    def __init__(self):
        self.werewolf_dict = {}

    def create_key(self, update: Update, context: CallbackContext) -> str:
        logger.info("%s created new group", update.message.from_user.first_name)
        update.message.reply_text('How many people are participating?')
        return 'get_number_of_players'

    def get_number_of_players(self, update: Update, context: CallbackContext) -> str:
        logger.info("%s chose %s players", update.message.from_user.first_name, update.message.text)
        number_of_players = int(update.message.text)
        update.message.reply_text('How many people are participating?')
        return 'get_number_of_players'

def cancel(self, update: Update, context: CallbackContext) -> int:
    logger.info("%s canceled", update.message.from_user.first_name)
    return ConversationHandler.END

master = Master()


def main() -> None:
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    text_non_command = Filters.text & ~Filters.command
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', master.create_key),
        ],
        states={
            'get_number_of_players': [MessageHandler(text_non_command, master.get_number_of_players)],
        },
        fallbacks=[
            CommandHandler('cancel', cancel),
            CommandHandler('start', start),
        ],
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
